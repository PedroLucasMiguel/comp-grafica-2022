import cv2
import numpy as np
from math import sqrt

# Making this global because it can be used in some recursive implementations
grid = [
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
    ]

s1_boundaries = ((0, 5), (0, 4))
s2_boundaries = ((6, 9), (0, 4))


def calcdistance(type='de'):

    stops1 = False
    stops2 = False

    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    r = 0

    while not stops1:
        x1 = int(input('Digite a coordenada X do ponto 1 (partindo de 0): '))
        y1 = int(input('Digite a coordenada y do ponto 1 (partindo de 0): '))

        if x1 > s1_boundaries[0][1] or y1 > s1_boundaries[1][1]:
            print('O ponto indicado não pertence a S1')

        else:
            stops1 = True

    while not stops2:
        x2 = int(input('Digite a coordenada X do ponto 2 (partindo de 0): '))
        y2 = int(input('Digite a coordenada y do ponto 2 (partindo de 0): '))

        if x2 > s2_boundaries[0][1] or y2 > s2_boundaries[1][1]:
            print('O ponto indicado não pertence a S2')

        else:
            stops2 = True

    if type == 'de':
        r = sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))

    elif type == 'd4':
        r = abs(x1 - x2) + abs(y1 - y2)

    elif type == 'd8':
        r = max(abs(x1 - x2), abs(y1 - y2))

    print(f'\n Resultado: {type} = {r}')


# Isso ficou terrível....
# Podemos procurar uma forma de implementar isso usando recursão provavelmente
def neighborhood(neighborhood_type=4):

    # procurando vizinhança partindo de s1
    for i in range(s1_boundaries[1][1]):
        for j in range(s1_boundaries[0][0], s1_boundaries[0][1] + 1):
            if grid[i][j] == 1:
                if j - 1 >= 0 and i - 1 >= 0:

                    if neighborhood_type == 8:
                        if grid[i - 1][j - 1] == 1 and s2_boundaries[0][0] <= j - 1 <= s2_boundaries[0][1]:
                            print(f"8(1) i{i} j{j}")
                            return True

                        if grid[i + 1][j - 1] == 1 and s2_boundaries[0][0] <= j - 1 <= s2_boundaries[0][1]:
                            print(f"8(2) i{i} j{j}")
                            return True

                        if grid[i - 1][j + 1] == 1 and s2_boundaries[0][0] <= j + 1 <= s2_boundaries[0][1]:
                            print(f"8(3) i{i} j{j}")
                            return True

                    if grid[i][j - 1] == 1 and s2_boundaries[0][0] <= j - 1 <= s2_boundaries[0][1]:
                        print(f"4(1) i{i} j{j}")
                        return True

                    elif grid[i - 1][j] == 1 and s2_boundaries[0][0] <= j <= s2_boundaries[0][1]:
                        print(f"4(2) i{i} j{j}")
                        return True

                if neighborhood_type == 8:
                    if grid[i + 1][j + 1] == 1 and s2_boundaries[0][0] <= j + 1 <= s2_boundaries[0][1]:
                        print(f"8(4) i{i} j{j}")
                        return True

                if grid[i][j + 1] == 1 and s2_boundaries[0][0] <= j + 1 <= s2_boundaries[0][1]:
                    print(f"4(3) i{i} j{j}")
                    return True

                elif grid[i + 1][j] == 1 and s2_boundaries[0][0] <= j <= s2_boundaries[0][1]:
                    print(f"4(4) i{i} j{j}")
                    return True


def createimage(size, squares_per_row, square_start_color, color_increment):
    i = numpy.array([])
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
    cv2.imwrite(f'{squares_per_row}.bmp', i)

    print(f"Profundidade: L = 2^{total_squares} = {pow(2, total_squares)}")
    print(
        f"Taxa de amostragem: {size}")  # https://www.sorocaba.unesp.br/Home/Graduacao/EngenhariaAmbiental/antonio/imagens.pdf

    return i


if __name__ == '__main__':
    i = createimage(size=256, squares_per_row=8, square_start_color=0, color_increment=5)
    #print(neighborhood(8))
    #calcdistance('d8')
