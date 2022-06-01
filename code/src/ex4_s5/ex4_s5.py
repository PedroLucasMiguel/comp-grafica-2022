from random import randrange
import cv2
import numpy as np
from os import path
from matplotlib import pyplot as plt

DEPTH = 8


def createHistogram(img, ax):
    '''
        Assumimos que todas as imagens a serem enviadas para esta função
        estão convertidas para grayscale com profundidade 8.
    '''

    # Criando a tabela base do histograma
    '''
    rows = pow(2, DEPTH)
    hist = []

    for i in range(rows):
        hist.insert(i, [i, 0])

    for i in img:
        for j in i:
            hist[j][1] = hist[j][1] + 1

    np_hist = np.array(hist)
    '''

    scale_max = pow(2, DEPTH)

    ax.hist(img.ravel(), scale_max, [0, scale_max])
    ax.set_xlabel("Níveis de cinza")
    ax.set_ylabel("Quantidade de Pixels")

    '''
    # TODO -  Para fazer isso funcionar corretamente, eu preciei criar um dicionario
    # e convertar o mesmo para um array depois. Não entendi o porque isso aconteceu
    # mas as somas do np sempre quebravam alguma coisa
    hist = {}
    rows = pow(2, DEPTH)
    for i in range(rows):
        hist[i] = 0

    # Preenchendo a tabela com o histograma da imagem
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            hist[img[i][j]] = hist[img[i][j]] + 1

    data = hist.items()
    l = list(data)
    hist = np.array(l)

        #Formato final do histograma:
            #nível de cinza | quantidade de pixels

    plt.hist(hist, rows, [0, rows])
    
    plt.show()
    '''


def equalizeHistogram(img, ax_img, ax_hist):

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

    img_np = np.array(img)

    ax_img.imshow(img_np, cmap='gray')

    createHistogram(img, ax_hist)


if __name__ == '__main__':
    img1 = cv2.imread(path.join('src', 'images', 'frutas.bmp'),
                      cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(
        path.join('src', 'images', 'mammogram.bmp'), cv2.IMREAD_GRAYSCALE)
    img3 = cv2.imread(path.join('src', 'images', 'Moon.tif'),
                      cv2.IMREAD_GRAYSCALE)
    img4 = cv2.imread(path.join('src', 'images', 'polem.bmp'),
                      cv2.IMREAD_GRAYSCALE)

    fig, axs = plt.subplots(4, 4)

    fig.set_size_inches(20, 15)
    fig.set_dpi(300)

    axs[0][0].imshow(img1, cmap='gray')
    createHistogram(img1, axs[0][1])
    equalizeHistogram(img1, axs[0][2], axs[0][3])

    axs[1][0].imshow(img2, cmap='gray')
    createHistogram(img2, axs[1][1])
    equalizeHistogram(img2, axs[1][2], axs[1][3])

    axs[2][0].imshow(img3, cmap='gray')
    createHistogram(img3, axs[2][1])
    equalizeHistogram(img3, axs[2][2], axs[2][3])

    axs[3][0].imshow(img4, cmap='gray')
    createHistogram(img4, axs[3][1])
    equalizeHistogram(img4, axs[3][2], axs[3][3])

    fig.savefig(path.join('src', 'images', 'ex4_s5.png'))
