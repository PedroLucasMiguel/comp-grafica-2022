from random import randrange
import cv2
import numpy as np
from os import path
from matplotlib import pyplot as plt

DEPTH = 8

def createHistogram(img, img_name):
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

    plt.hist(img.ravel(), scale_max, [0, scale_max])
    plt.xlabel("Níveis de cinza")
    plt.ylabel("Quantidade de Pixels")
    
    plt.savefig(path.join('src/output', f'{img_name}-h.png'))

    plt.cla()

    print('Histograma salvo em: ' + path.join('src/output', f'{img_name}-h.png'))

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

    img_np = np.array(img)

    cv2.imwrite(path.join('src/output', f'{img_name}-eh.png'), img_np)

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