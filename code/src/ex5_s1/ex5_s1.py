import cv2
import numpy as np
from os import path

def createimage(size, squares_per_row, square_start_color, color_increment):
    i = np.array([])
    total_squares = squares_per_row * squares_per_row
    gradient = []
    gradient_index = 0
    gradient_offset = 0

    if squares_per_row != 1:
        square_size = int(size / squares_per_row)

        aux_color = square_start_color

        # Criando o gradiente de cores
        for a in range(total_squares):
            aux_color = aux_color + color_increment
            gradient.append(aux_color)

        # Criando a imagem partindo do vetor
        for s in range(squares_per_row):
            for y in range(square_size):
                for y_row in range(squares_per_row):
                    for x in range(square_size):
                        i = np.append(i, gradient[gradient_index])
                    gradient_index = gradient_index + 1
                gradient_index = gradient_offset
            gradient_offset = gradient_offset + squares_per_row - 1

    else:
        for x in range(size):
            for y in range(size):
                i = np.append(i, square_start_color)

    i = np.reshape(i, (size, size))
    cv2.imwrite(path.join('code/src/output', f'{squares_per_row}.bmp'), i)

    print(f"Profundidade: L = 2^{total_squares} = {pow(2, total_squares)}")
    print(
        f"Taxa de amostragem: {size}")  # https://www.sorocaba.unesp.br/Home/Graduacao/EngenhariaAmbiental/antonio/imagens.pdf

    return i