from ex5_s1.ex5_s1 import createimage
from ex7_s1.ex7_s1 import count_connected_4, count_connected_8
from ex8_s1.ex8_s1 import calcdistance
from ex3_s2.ex3_s2 import apply_noises, calcerrors

import cv2
import numpy as np
import os

s1 = {
    "grid": [
        [0, 1, 0, 0, 0, 1],
        [1, 0, 0, 1, 0, 0],
        [1, 0, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0]
    ],
    "sizeX": 6,
    "sizeY": 5,
    "offsetX": 0,
    "offsetY": 0
}

s2 = {
    "grid": [
        [0, 0, 0, 0],
        [0, 0, 1, 0],
        [1, 1, 0, 1],
        [0, 0, 1, 0],
        [1, 0, 0, 0]
    ],
    "sizeX": 4,
    "sizeY": 5,
    "offsetX": 6,
    "offsetY": 0
}

if __name__ == '__main__':

    '''
    #i = createimage(size=256, squares_per_row=8, square_start_color=0, color_increment=5)
    grid = [
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0],
        [1, 0, 1, 1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0]
    ]

    s1_boundaries = ((0, 5), (0, 4))
    s2_boundaries = ((6, 9), (0, 4))
    '''

    # print(os.listdir('code/src/images'))

    # apply_noises()
    # calcerrors()

    print(count_connected_8(s1, s2))

    pass
