import cv2
import numpy as np
from os import path
from matplotlib import pyplot as plt

DEPTH = 8

# Função responsável por criar as imagens dos histogramas
def __createHistogram(img, img_name):
    # Após receber a imagem (img) como parâmetro, constrói a imagem do histograma
    scale_max = pow(2, DEPTH)

    plt.hist(img.ravel(), scale_max, [0, scale_max])
    plt.xlabel("Níveis de cinza")
    plt.ylabel("Quantidade de Pixels")
    plt.title(f'Histograma "{img_name}.jpg"')
    
    plt.savefig(path.join('output', f'{img_name}-h.jpg'))

    plt.cla()

    print(f'Histograma salvo em: ' + path.join('output', f'{img_name}-h.jpg'))


def __equalizeHistogram(img, img_name):

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

    # Calculando os niveis de cinza equalizados
    for i in range(rows):
        hist[i][1] = round(hist[i][1] * rows-1)

    # Corrigindo imagem
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] = hist[img[i][j]][1]

    # Salva imagem equalizada
    cv2.imwrite(path.join('output', f'{img_name}-eh.jpg'), img)

    print(f'Imagem equalizada salva em: ' + path.join('output', f'{img_name}-eh.jpg'))

    # Cria histograma
    __createHistogram(img, img_name)


def run():
    img1 = cv2.imread(path.join('images', 'frutas.bmp'), cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(path.join('images', 'mammogram.bmp'), cv2.IMREAD_GRAYSCALE)
    img3 = cv2.imread(path.join('images', 'Moon.tif'), cv2.IMREAD_GRAYSCALE)
    img4 = cv2.imread(path.join('images', 'polem.bmp'), cv2.IMREAD_GRAYSCALE)

    __createHistogram(img1, 'frutas-original')
    __equalizeHistogram(img1, 'frutas-equalizado')

    __createHistogram(img2, 'mammogram-original')
    __equalizeHistogram(img2, 'mammogram-equalizado')

    __createHistogram(img3, 'Moon-original')
    __equalizeHistogram(img3, 'Moon-equalizado')

    __createHistogram(img4, 'polem-original')
    __equalizeHistogram(img4, 'polem-equalizado')