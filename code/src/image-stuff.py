import numpy
from PIL import Image
import numpy as np


def createimage(size, squares_per_row, square_start_color, color_increment_offset):
    i = numpy.array([])
    current_color = square_start_color
    total_squares = squares_per_row * squares_per_row
    gradient = []
    gradient_index = 0
    gradient_offset = 0

    for a in range(total_squares):
        current_color = current_color + color_increment_offset
        gradient.append(current_color)
        print(gradient[a])

    if squares_per_row != 1:
        square_size = int(size / squares_per_row)

        for s in range(squares_per_row):
            for k in range(square_size):
                for y in range(squares_per_row):
                    for x in range(square_size):
                        i = np.append(i, gradient[gradient_index])
                    gradient_index = gradient_index + 1
                gradient_index = gradient_offset
            gradient_offset = gradient_offset + squares_per_row - 1


    else:
        for x in range(size):
            for y in range(size):
                i = np.append(i, current_color)

    i = np.reshape(i, (size, size))
    i = Image.fromarray(i)
    i = i.convert('L')
    i.save('teste.bmp', 'bmp')


if __name__ == '__main__':
        #createimage(256, 1, 150)
    createimage(256, 4, 120, 10)
