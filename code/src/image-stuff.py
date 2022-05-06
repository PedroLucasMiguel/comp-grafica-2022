import numpy
from PIL import Image
import numpy as np

START_COLOR = 180


def createimage(size, squares_per_row):
    i = numpy.array([])

    if squares_per_row != 1:
        square_size = size / squares_per_row

        for x in range(size):
            if x < square_size - 1:
                for y in range(size):
                    if y < square_size:
                        i = np.append(i, START_COLOR)
                    else:
                        i = np.append(i, START_COLOR + 10)
            else:
                for y in range(size):
                    if y < square_size:
                        i = np.append(i, START_COLOR + 20)
                    else:
                        i = np.append(i, START_COLOR + 30)

    else:
        for x in range(size):
            for y in range(size):
                i = np.append(i, START_COLOR)

    i = np.reshape(i, (size, size))
    i = Image.fromarray(i)
    i = i.convert('L')
    i.save('teste.bmp', 'bmp')


if __name__ == '__main__':
        createimage(256, 2)
