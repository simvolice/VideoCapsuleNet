import shutil
import os

outdir_clips = "/root/PycharmProjects/VideoCapsuleNetUpd/UCF101_Frames/frames/"

allFrameDirs = os.listdir(outdir_clips)


def insertZeroFrame():
    for dirClip in allFrameDirs:
        shutil.copyfile(os.path.join(outdir_clips, dirClip, "frame_1.jpg"),
                        os.path.join(outdir_clips, dirClip, "frame_0.jpg"))
        print("copy...")


def deleteFramesOutOfRange():
    for dirClip in allFrameDirs:
        for deleteFilesNumber in range(40, len(os.listdir(os.path.join(outdir_clips, dirClip)))):
            os.remove(os.path.join(outdir_clips, dirClip, "frame_{}.jpg".format(deleteFilesNumber)))
            print("delete...")


#insertZeroFrame()
deleteFramesOutOfRange()