import numpy as np
import tensorflow as tf
from caps_network import Caps3d
import config
from skvideo.io import vread, vwrite
from scipy.misc import imresize


def inference(video_name):
    gpu_config = tf.compat.v1.ConfigProto()
    gpu_config.gpu_options.allow_growth = True

    capsnet = Caps3d()
    with tf.compat.v1.Session(graph=capsnet.graph, config=gpu_config) as sess:
        tf.compat.v1.global_variables_initializer().run()
        capsnet.load(sess, config.save_file_name % (config.start_at_epoch - 1))

        video = vread(video_name)

        n_frames = video.shape[0]
        crop_size = (112, 112)

        # assumes a given aspect ratio of (240, 320). If given a cropped video, then no resizing occurs
        if video.shape[1] != 112 and video.shape[2] != 112:
            h, w = 120, 160

            video_res = np.zeros((n_frames, 120, 160, 3))

            for f in range(n_frames):
                video_res[f] = imresize(video[f], (120, 160))
        else:
            h, w = 112, 112
            video_res = video

        # crops video to 112x112
        margin_h = h - crop_size[0]
        h_crop_start = int(margin_h / 2)
        margin_w = w - crop_size[1]
        w_crop_start = int(margin_w / 2)
        video_cropped = video_res[:, h_crop_start:h_crop_start + crop_size[0], w_crop_start:w_crop_start + crop_size[1],:]

        print('Saving Cropped Video')
        vwrite('cropped.avi', video_cropped)

        video_cropped = video_cropped / 255.

        f_skip = config.frame_skip

        for i in range(0, n_frames, 8 * f_skip):
            # if frames are skipped (subsampled) during training, they should also be skipped at test time
            # creates a batch of video clips
            x_batch = [[] for i in range(f_skip)]
            predictions = []
            for k in range(f_skip * 8):
                if i + k >= n_frames:
                    x_batch[k % f_skip].append(np.zeros_like(video_cropped[-1]))
                else:
                    x_batch[k % f_skip].append(video_cropped[i + k])
            x_batch = [np.stack(x, axis=0) for x in x_batch]

            pred = sess.run(capsnet.digit_preds,
                            feed_dict={capsnet.x_input: x_batch, capsnet.y_input: np.ones((f_skip,), np.int32) * -1,
                                       capsnet.m: 0.9, capsnet.is_train: False})

            predictions.append(pred)
            predictions = np.concatenate(predictions, axis=0)
            predictions = predictions.reshape((-1, config.n_classes))
            print(predictions)
            fin_pred = np.mean(predictions, axis=0)
            print("Pred after np.mean", fin_pred)
            fin_pred = np.argmax(fin_pred)
            print("Pred after np.argmax", fin_pred)


inference('test.avi')
