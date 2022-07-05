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
    # Valor do limiar: 220
    img_limiarized = __limiarization(img, 220)
    out = np.zeros(img_limiarized.shape)
    for i in range(out.shape[0]):
        for j in range(out.shape[1]):
            if img_limiarized[i][j] > 0:
                out[i][j] = 255
    cv.imwrite(path.join("src", "images", "Img4_limiarized.bmp"), out)
    # Elemento estruturante quadrado de lado 7
    structuring_element = {"mask": np.ones((7, 7), np.uint), "center": (3, 3)}
    img_opened = __dilation(
        __erosion(img_limiarized, structuring_element), structuring_element)
    for i in range(img_opened.shape[0]):
        for j in range(img_opened.shape[1]):
            if img_opened[i][j] > 0:
                img_opened[i][j] = 255
    cv.imwrite(path.join("src", "images", "Img4_opened.bmp"), img_opened)


if __name__ == "__main__":
    run()
