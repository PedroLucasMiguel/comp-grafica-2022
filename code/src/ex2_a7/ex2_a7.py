import numpy as np
import cv2
from os import path
from matplotlib import pyplot as plt


def gausian_noise(img, dist):
    # Ruído gaussiano

    row, col = img.shape
    colors = []

    for i in range(0, 101, 5):
        colors.append(i)

    for i in range(row):
        for j in range(col):
            if abs(np.random.normal(0, 0.25)) <= dist/100:
                p_color = img[i, j] + colors[np.random.randint(0, len(colors))]
                img[i, j] = p_color if p_color <= 255 else 255


def run():
    img = cv2.imread(path.join("src", "images", "img_exercicio2.png"),
                     cv2.IMREAD_GRAYSCALE)

    gausian_noise(img, 10)

    cv2.imwrite(path.join("src", "images", "img_exercicio2_noise.png"), img)

    dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)

    dft_shift = np.fft.fftshift(dft)

    mag, phase = cv2.cartToPolar(dft_shift[:, :, 0], dft_shift[:, :, 1])

    spec = np.log(np.abs(mag))

    cv2.imwrite(path.join("src", "images", "img_exercicio2_noise_spec.png"),
                spec / np.max(spec) * 255)

    filter_gaussian = cv2.imread(path.join("src", "images", "filter_gaussian.png"),
                                 cv2.IMREAD_GRAYSCALE)
    filter_pass = cv2.imread(
        path.join("src", "images", "filter_pass.png"), cv2.IMREAD_GRAYSCALE)

    new_mag_gaussian = filter_gaussian / 255 * mag
    new_mag_pass = filter_pass / 255 * mag

    new_spec_gaussian = np.log(np.abs(new_mag_gaussian))
    new_spec_pass = np.log(np.abs(new_mag_pass))

    cv2.imwrite(path.join("src", "images", "new_spec_gaussian.png"),
                new_spec_gaussian / np.max(new_spec_gaussian) * 255)
    cv2.imwrite(path.join("src", "images", "new_spec_pass.png"),
                new_spec_pass / np.max(new_spec_pass) * 255)

    real_gaussian, imag_gaussian = cv2.polarToCart(
        np.float32(new_mag_gaussian), phase)
    real_pass, imag_pass = cv2.polarToCart(np.float32(new_mag_pass), phase)

    back_ishift_gaussian = np.fft.ifftshift(
        cv2.merge([real_gaussian, imag_gaussian]))
    back_ishift_pass = np.fft.ifftshift(cv2.merge([real_pass, imag_pass]))

    img_back_gaussian = cv2.idft(back_ishift_gaussian)
    img_back_pass = cv2.idft(back_ishift_pass)

    img_back_gaussian = cv2.magnitude(
        img_back_gaussian[:, :, 0], img_back_gaussian[:, :, 1])
    img_back_pass = cv2.magnitude(
        img_back_pass[:, :, 0], img_back_pass[:, :, 1])

    img_back_gaussian = cv2.normalize(
        img_back_gaussian, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    img_back_pass = cv2.normalize(
        img_back_pass, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    cv2.imwrite(path.join("src", "images", "new_img_gaussian.png"),
                img_back_gaussian)
    cv2.imwrite(path.join("src", "images", "new_img_pass.png"), img_back_pass)
