import os
import subprocess
import glob

videodir = "/root/PycharmProjects/VideoCapsuleNetUpd/UCF101_Frames/dataSet/fightData/"

outdir_clips = "/root/PycharmProjects/VideoCapsuleNetUpd/UCF101_Frames/frames/"
if not os.path.isdir(outdir_clips):
    os.makedirs(outdir_clips)
clip_length = 6  # seconds


# utils
def hou_min_sec(millis):
    millis = int(millis)
    seconds = int((millis / 1000) % 60)
    minutes = int((millis / (60 * 1000)) % 60)
    hours = int((millis / (60 * 60 * 1000)) % 60)
    return "%d:%d:%d" % (hours, minutes, seconds)


videonames = glob.glob(videodir + '*')
videonames = [os.path.basename(v).split('.')[0] for v in videonames]

for video_id in videonames:

    videofile = glob.glob(os.path.join(videodir, video_id + '*'))[0]

    clips_dir = os.path.join(outdir_clips, video_id)
    if not os.path.isdir(clips_dir):
        os.makedirs(clips_dir)

        ffmpeg_command = 'ffmpeg -ss {} -i {} -vf scale=160:120 -t {} {}/frame_%d.jpg'.format(0, videofile, clip_length,
                                                                            clips_dir)

        subprocess.call(ffmpeg_command, shell=True)
