import cv2 as cv
from os import path
import numpy as np
from numba import njit


@njit
def __check_matrix_equality(m1, m2):
    for i in range(m1.shape[0]):
        for j in range(m1.shape[1]):
            if m1[i, j] != m2[i, j]:
                return False
    return True


def erosion(img, element):
    result = np.zeros(img.shape, np.uint)
    for i in range(element["center"][0], img.shape[0] - element["center"][0]):
        for j in range(element["center"][1], img.shape[1] - element["center"][1]):
            if img[i, j] == 1 and __check_matrix_equality(img[i-element["center"][0]:i+element["center"][0]+1, j-element["center"][1]:j+element["center"][1]+1], element["mask"]):
                result[i, j] = 1
    return result


def dilation(img, element):
    result = np.zeros(img.shape, np.uint)
    for i in range(element["center"][0], img.shape[0] - element["center"][0]):
        for j in range(element["center"][1], img.shape[1] - element["center"][1]):
            if img[i][j] > 0:
                result[i-element["center"][0]:i+element["center"][0]+1, j -
                       element["center"][1]:j+element["center"][1]+1] = element["mask"]
    return result


def run():
    img = cv.imread(path.join("src", "images", "Img3.bmp"),
                    cv.IMREAD_GRAYSCALE)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i, j] > 0:
                img[i, j] = 1
    structuring_element = {"mask": np.ones(
        (13, 13), np.uint), "center": (6, 6)}
    img_eroded = erosion(img, structuring_element)
    for i in range(img_eroded.shape[0]):
        for j in range(img_eroded.shape[1]):
            if img_eroded[i, j] > 0:
                img_eroded[i, j] = 255
    cv.imwrite(path.join("src", "images", "Img3_eroded.bmp"), img_eroded)
    img_dilated = dilation(img_eroded, structuring_element)
    for i in range(img_dilated.shape[0]):
        for j in range(img_dilated.shape[1]):
            if img_dilated[i, j] > 0:
                img_dilated[i, j] = 255
    cv.imwrite(path.join("src", "images", "Img3_dilated.bmp"), img_dilated)


if __name__ == "__main__":
    run()
