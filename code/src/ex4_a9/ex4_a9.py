from numba import njit
import cv2 as cv
from os import path
import numpy as np
import sys

sys.path.insert(0, "..")

# autopep8: off
from ex3_a9 import ex3_a9

# autopep8: on


def __limiarization(img, threshold):
    result = np.zeros(img.shape, np.uint)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] < threshold:
                result[i][j] = 1
    return result


def run():
    img = cv.imread(path.join("src", "images", "Img4.bmp"),
                    cv.IMREAD_GRAYSCALE)
    img_limiarized = __limiarization(img, 220)
    for i in range(img_limiarized.shape[0]):
        for j in range(img_limiarized.shape[1]):
            if img_limiarized[i][j] > 0:
                img_limiarized[i][j] = 255
    cv.imwrite(path.join("src", "images", "Img4_limiarized.bmp"), img_limiarized)
    structuring_element = {"mask": np.ones((9, 9), np.uint), "center": (4, 4)}
    img_opened = ex3_a9.dilation(
        ex3_a9.erosion(img_limiarized, structuring_element), structuring_element)
    for i in range(img_opened.shape[0]):
        for j in range(img_opened.shape[1]):
            if img_opened[i][j] > 0:
                img_opened[i][j] = 255
    cv.imwrite(path.join("src", "images", "Img4_opened.bmp"), img_opened)


if __name__ == "__main__":
    run()
