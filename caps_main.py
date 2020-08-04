import tensorflow as tf
import config
from caps_network import Caps3d
from load_ucf101_dataCopy import UCF101TrainDataGenDet as TrainDataGen


def get_num_params():
    # prints out the number of trainable  parameters in the TensorFlow graph
    total_parameters = 0
    for variable in tf.compat.v1.trainable_variables():
        shape = variable.get_shape()
        variable_parameters = 1
        for dim in shape:
            variable_parameters *= dim
        total_parameters += variable_parameters
    print('Num of parameters:', total_parameters)


def train_network(gpu_config):
    capsnet = Caps3d()

    with tf.compat.v1.Session(graph=capsnet.graph, config=gpu_config) as sess:
        tf.compat.v1.global_variables_initializer().run()

        get_num_params()
        if config.start_at_epoch <= 1:
            config.clear_output()
        else:
            capsnet.load(sess, config.save_file_name % (config.start_at_epoch - 1))
            print('Loading from epoch %d.' % (config.start_at_epoch - 1))

        n_eps_after_acc, best_loss = -1, 100000
        print('Training on UCF101')
        for ep in range(config.start_at_epoch, config.n_epochs + 1):
            print(20 * '*', 'epoch', ep, 20 * '*')
            nan_tries = 0
            while nan_tries < 3:
                # trains network for one epoch
                data_gen = TrainDataGen(config.wait_for_data, frame_skip=config.frame_skip)
                margin_loss, seg_loss, acc = capsnet.train(sess, data_gen)

                if margin_loss < 0 or acc < 0:
                    nan_tries += 1
                    # capsnet.load(sess, config.save_file_name % 20)  # loads in the previous epoch
                    # while data_gen.has_data():
                    #     data_gen.get_batch(config.batch_size)
                else:
                    config.write_output('CL: %.4f. SL: %.4f. Acc: %.4f\n' % (margin_loss, seg_loss, acc))
                    break
            if nan_tries == 3:
                print('Network cannot be trained. Too many NaN issues.')
                exit()

            if ep % config.save_every_n_epochs == 0:
                try:
                    capsnet.save(sess, config.save_file_name % ep)
                    config.write_output('Saved Network\n')
                except:
                    print('Failed to save network!!!')

            # increments the margin
            if ep % config.n_eps_for_m == 0:
                capsnet.cur_m += config.m_delta
                capsnet.cur_m = min(capsnet.cur_m, 0.9)

            # only validates after a certain number of epochs and when the training accuracy is greater than a threshold
            # this is mainly used to save time, since validation takes about 10 minutes
            if (acc >= config.acc_for_eval or n_eps_after_acc >= 0) and ep >= config.n_eps_until_eval:
                n_eps_after_acc += 1

            # validates the network
            if (acc >= config.acc_for_eval and n_eps_after_acc % config.n_eps_for_eval == 0) or ep == config.n_epochs:
                # data_gen = TestDataGen(config.wait_for_data, frame_skip=1)
                # margin_loss, seg_loss, accuracy, _ = capsnet.eval(sess, data_gen, validation=True)
                #
                # config.write_output('Validation\tCL: %.4f. SL: %.4f. Acc: %.4f.\n' %
                #                     (margin_loss, seg_loss, accuracy))
                #
                # # saves the network when validation loss in minimized
                # t_loss = margin_loss + seg_loss
                # if t_loss < best_loss:
                #     best_loss = t_loss
                try:
                    capsnet.save(sess, config.save_file_name % ep)
                    config.write_output('Saved Network\n')
                except:
                    print('Failed to save network!!!')

        # calculate final test accuracy, f-mAP, and v-mAP
        # iou()


def main():
    gpu_config = tf.compat.v1.ConfigProto(allow_soft_placement=True)
    gpu_config.gpu_options.allow_growth = True

    # trains the network with the given gpu configuration
    train_network(gpu_config)


main()
