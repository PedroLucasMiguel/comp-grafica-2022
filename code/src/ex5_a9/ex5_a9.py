from numba import njit
import cv2 as cv
from os import path
import numpy as np


@njit
def __check_matrix_equality(m1, m2):
    for i in range(m1.shape[0]):
        for j in range(m1.shape[1]):
            if m1[i, j] != m2[i, j]:
                return False
    return True


def __erosion(img, element):
    result = np.zeros(img.shape, np.uint)
    for i in range(element["center"][0], img.shape[0] - element["center"][0]):
        if i == 80:
            pass
        for j in range(element["center"][1], img.shape[1] - element["center"][1]):
            if j == 24:
                pass
            if img[i, j] > 0 and __check_matrix_equality(img[i-element["center"][0]:i+element["center"][0]+1, j-element["center"][1]:j+element["center"][1]+1], element["mask"]):
                result[i, j] = 1
    return result


def __dilation(img, element):
    result = np.zeros(img.shape, np.uint)
    for i in range(element["center"][0], img.shape[0] - element["center"][0]):
        for j in range(element["center"][1], img.shape[1] - element["center"][1]):
            if img[i][j] > 0:
                result[i-element["center"][0]:i+element["center"][0]+1, j -
                       element["center"][1]:j+element["center"][1]+1] = element["mask"]
    return result


def run():
    img = cv.imread(path.join("src", "images", "img2.bmp"),
                    cv.IMREAD_GRAYSCALE)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > 0:
                img[i][j] = 1
    # Elemento estruturante de lado 5
    structuring_element_opened = {"mask": np.ones((5, 5)), "center": (2, 2)}
    img_opened = __dilation(
        __erosion(img, structuring_element_opened), structuring_element_opened)
    out = np.zeros(img_opened.shape)
    for i in range(img_opened.shape[0]):
        for j in range(img_opened.shape[1]):
            if img_opened[i][j] > 0:
                out[i][j] = 255
    cv.imwrite(path.join("src", "images", "img2_opened.bmp"), out)
    # Elemento estruturante de lado 3
    structuring_element_closed = {"mask": np.ones((3, 3)), "center": (1, 1)}
    img_closed = __erosion(__dilation(
        img_opened, structuring_element_closed), structuring_element_closed)
    out = np.zeros(img_closed.shape, np.uint)
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            if img_closed[i][j] > 0:
                out[i][j] = 255
    cv.imwrite(path.join("src", "images", "img2_closed.bmp"), out)


if __name__ == "__main__":
    run()
