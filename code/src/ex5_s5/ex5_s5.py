import numpy as np
import cv2
from math import sqrt
from os import path

def __calc_gamma_correction(f, c, y):
    return c*pow((f + 1), y)

def __do_gamma_correction(f, f_name):

    gamma_range = (
        0.04, 
        0.10, 
        0.20,
        0.40,
        0.67,
        1.0,
        1.5,
        2.5,
        5.0,
        10.0,
        25.0,
    )

    s = f.shape
    imgs = [] # Array que vai guardar as correções
    imgs_index = 0

    for g in gamma_range:
        imgs.append(np.array([])) # Adiciona um NP array que será a imagem corrigida para cada nível de gamma
        for i in range(s[0]):
            for j in range(s[1]):
                imgs[imgs_index] = np.append(imgs[imgs_index], f[i][j] + __calc_gamma_correction(f[i][j], 1, g))
        
        aux = imgs[imgs_index]
        aux = np.reshape(aux, f.shape)

        cv2.imwrite(path.join('src/output', f'{f_name}_{g}.jpg'), aux)
        imgs_index = imgs_index + 1

if __name__ == '__main__':
    __do_gamma_correction(cv2.imread(path.join('src/images', 'polem.bmp'), cv2.IMREAD_GRAYSCALE), 'polem')