import numpy
from PIL import Image
import numpy as np


# This is a terrible implementation
# Probably we can do something better using recursion, but i'm too tired for that
def neighborhood(neighborhood_type=4):
    grid = [
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
    ]

    s1_boundaries = ((0, 5), (0, 4))
    s2_boundaries = ((6, 9), (0, 4))

    # Searching neighborhood from s1
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

        # Creating the color gradient
        for a in range(total_squares):
            aux_color = aux_color + color_increment
            gradient.append(aux_color)

        # Creating the image on the array
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
    pil_image = Image.fromarray(i)
    pil_image = pil_image.convert('L')
    pil_image.save(f'{squares_per_row}.bmp', 'bmp')

    print(f"Profundidade: L = 2^{total_squares} = {pow(2, total_squares)}")
    print(
        f"Taxa de amostragem: {size}")  # https://www.sorocaba.unesp.br/Home/Graduacao/EngenhariaAmbiental/antonio/imagens.pdf

    return i


if __name__ == '__main__':
    #i = createimage(size=256, squares_per_row=4, square_start_color=50, color_increment=10)

    print(neighborhood(8))
