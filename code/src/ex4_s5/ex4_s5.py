from random import randrange
import cv2
import numpy as np
from os import path
from matplotlib import pyplot as plt

DEPTH = 8

def createHistogram(img, img_name):

    scale_max = pow(2, DEPTH)

    plt.hist(img.ravel(), scale_max, [0, scale_max])
    plt.xlabel("Níveis de cinza")
    plt.ylabel("Quantidade de Pixels")
    
    plt.savefig(path.join('src/output', f'{img_name}-h.png'))

    plt.cla()

    print('Histograma salvo em: ' + path.join('src/output', f'{img_name}-h.png'))


def equalizeHistogram(img, img_name):

    rows = pow(2, DEPTH)
    qtd_pixels = img.shape[0] * img.shape[1]
    
    hist = []

    for i in range(rows):
        hist.insert(i, [i, 0])

    # Criando a tabela base do histograma
    for i in img:
        for j in i:
            hist[j][1] = hist[j][1] + 1

    # Calculando probabilidade
    for i in range(rows):
        hist[i][1] = hist[i][1]/qtd_pixels

    # Calculando FDA
    for i in range(0, rows-1, 1):
        hist[i+1][1] = hist[i][1] + hist[i+1][1]

    # Calculando os níveis de cinza equalizados
    for i in range(rows):
        hist[i][1] = round(hist[i][1] * rows-1)

    # Corrigindo imagem
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] = hist[img[i][j]][1]

    cv2.imwrite(path.join('src/output', f'{img_name}-eh.png'), img)

    createHistogram(img, img_name)


if __name__ == '__main__':
    img1 = cv2.imread(path.join('src/images', 'frutas.bmp'), cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(path.join('src/images', 'mammogram.bmp'), cv2.IMREAD_GRAYSCALE)
    img3 = cv2.imread(path.join('src/images', 'Moon.tif'), cv2.IMREAD_GRAYSCALE)
    img4 = cv2.imread(path.join('src/images', 'polem.bmp'), cv2.IMREAD_GRAYSCALE)
    createHistogram(img1, 'frutas-original')
    equalizeHistogram(img1, 'frutas-equalizado')

    createHistogram(img2, 'mammogram-original')
    equalizeHistogram(img2, 'mammogram-equalizado')

    createHistogram(img3, 'Moon-original')
    equalizeHistogram(img3, 'Moon-equalizado')

    createHistogram(img4, 'polem-original')
    equalizeHistogram(img4, 'polem-equalizado')