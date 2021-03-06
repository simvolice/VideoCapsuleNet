import cv2
import math
import numpy as np


def draw_box(image, box, color, thickness=1):
    b = np.array(box).astype(int)
    cv2.rectangle(image, (b[0], b[1]), (b[2], b[3]), color, thickness, cv2.LINE_AA)


def main():
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    image = cv2.imread("/root/PycharmProjects/VideoCapsuleNetUpd/UCF101_Frames/frames/l-jxh8gpxuY_1420/frame_1.jpg")
    h, w, d = image.shape

    draw_box(image, [47,   1, 160, 116], (0, 255, 0))

    cv2.imshow('Image', image)
    key = cv2.waitKey()
    if (key == ord('q')) or (key == 27):
        return False


main()