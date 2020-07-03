import shutil
import os
outdir_clips = "/root/PycharmProjects/VideoCapsuleNet/UCF101_Frames/backup/frames/"

allFrameDirs = os.listdir(outdir_clips)

for dirClip in allFrameDirs:
    shutil.copyfile(os.path.join(outdir_clips, dirClip, "frame_1.jpg"), os.path.join(outdir_clips, dirClip, "frame_0.jpg"))
    print("copy...")