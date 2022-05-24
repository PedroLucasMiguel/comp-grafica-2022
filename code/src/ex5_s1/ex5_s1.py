import cv2
import numpy as np
from os import path
from math import log2, floor

# Função que cria as imagens solicitadas
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
        for s in range(squares_per_row): # Para cada linha de quadrados
            for y in range(square_size): # De tamanho "square_size"
                for y_row in range(squares_per_row): # Desenhe "square_per_row" quadrados
                    for x in range(square_size): # De tamanho "square size"
                        i = np.append(i, gradient[gradient_index])
                    gradient_index = gradient_index + 1
                gradient_index = gradient_offset  
            gradient_offset = gradient_offset + squares_per_row

    else:
        for x in range(size):
            for y in range(size):
                i = np.append(i, square_start_color)

    i = np.reshape(i, (size, size))
    cv2.imwrite(path.join('code/src/output', f'{squares_per_row}.bmp'), i)

    return f'{squares_per_row}.bmp'

# Resolve a segunda parte do exercício
def parttwo(imgName):
    
    # Lendo imagem
    img  = cv2.imread(path.join('code/src/output', imgName), cv2.IMREAD_GRAYSCALE)

    higher_pixel_value = 0

    # Encontrando o pixel de maior valor
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if (img[i][j] > higher_pixel_value):
                higher_pixel_value = img[i][j]

    depth = floor(log2(higher_pixel_value)) + 1 # Calculando a profundidade

    print(f'Pixel de maior valor: {higher_pixel_value}\nProfundidade: {depth}\n')
    print(f"Taxa de amostragem:\nTotal de pixels: {img.shape[0] * img.shape[1]}\nOrganizados em uma matriz: {img.shape}\n\n")

if __name__ == '__main__':
    parttwo(createimage(256, 1, 200, -10))
    parttwo(createimage(256, 2, 60, 50))
    parttwo(createimage(256, 4, 60, 10))