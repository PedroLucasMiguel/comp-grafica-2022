import cv2
from cv2 import equalizeHist
import numpy as np
from os import path
from matplotlib import pyplot as plt
from math import floor, log2

def __doOtsu(img):

    l = np.amax(img)
    qtd_pixels = img.shape[0] * img.shape[1]
    
    hist = []

    # Criando a tabela base do histograma
    for i in range(l+1):
        hist.insert(i, [i, 0])

    # Preenchendo tabela base
    for i in img:
        for j in i:
            hist[j][1] = hist[j][1] + 1

    # Normalizando histograma
    for i in range(l+1):
        hist[i][1] = hist[i][1]/qtd_pixels


    v_final = -1
    k_final = 0

    # Começando o processo de Otsu para duas classes
    # FIX-ME: Expandir para 4 classes
    for k in range(0, l):
        
        p1 = 0
        for i in range(0, k + 1):
            p1 = p1 + (hist[i][1])

        # Calculando P2
        p2 = 1 - p1

        if p1 < 1.e-6 or p2 < 1.e-6:
            continue

        #print(f'P1: {p1} || P2: {p2}')

        # Calculando m1
        m1 = 0
        for i in range(0, k + 1):
            m1 = m1 + ((i * hist[i][1]) / p1)

        # Calculando m2
        m2 = 0
        for i in range(k + 1, l):
            m2 = m2 + ((i * hist[i][1]) / p2)

        # Calculando mt
        mt = (p1*m1) + (p2*m2)

        # Calculando variância
        v = (p1*((m1-mt)**2)) + (p2*((m2-mt)**2))
    
        if v > v_final:
            v_final = v
            k_final = k

    print(v_final, k_final)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > k_final:
                img[i][j] = 255
            else:
                img[i][j] = 0
            
    cv2.imwrite(path.join('src', 'output', f'a_plz.png'), img)


if __name__ == '__main__':
    
    img = cv2.imread(path.join('src', 'images', 'img_seg.jpg'), cv2.IMREAD_GRAYSCALE)
    
    __doOtsu(img)
