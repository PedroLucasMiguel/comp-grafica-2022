import numpy
from PIL import Image
import numpy as np


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

    return i


if __name__ == '__main__':
    createimage(size=256, squares_per_row=2, square_start_color=180, color_increment=10)
