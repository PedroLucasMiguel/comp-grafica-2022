import cv2
import numpy as np
from os import path
from math import floor, log2
import matplotlib.pyplot as plt

def __createHistogram(img, ax, title):

    # Calculando profundidade da imagem
    depth = floor(log2(np.amax(img))) + 1

    # Após receber a imagem (img) como parâmetro, constrói a imagem do histograma
    scale_max = pow(2, depth)

    ax.hist(img.ravel(), scale_max, [0, scale_max])

    ax.set_title(title)
    ax.set_xlabel("Níveis de cinza")
    ax.set_ylabel("Quantidade de Pixels")

# Função responsável pela equalização de histograma
def __equalizeHistogram(img):

    rows = np.amax(img)
    qtd_pixels = img.shape[0] * img.shape[1]
    
    hist = []

    for i in range(rows+1):
        hist.insert(i, [i, 0])

    # Criando a tabela base do histograma
    for i in img:
        for j in i:
            hist[j][1] = hist[j][1] + 1

    # Calculando probabilidade
    for i in range(rows+1):
        hist[i][1] = hist[i][1]/qtd_pixels

    # Calculando FDA
    for i in range(1, rows+1):
        hist[i][1] = hist[i-1][1] + hist[i][1]

    # Calculando os niveis de cinza equalizados
    for i in range(rows+1):
        hist[i][1] = round(hist[i][1] * rows)

    # Corrigindo imagem
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i][j] = hist[img[i][j]][1]


if __name__ == '__main__':
    imgs = ['img1.bmp', 'img2.bmp', 'img3.JPG']
    imgs_ei = ['img1-eI.jpg', 'img2-eI.jpg', 'img3-eI.jpg']

    for img_name in imgs:
        fig1, axs1 = plt.subplots(2, 2)
        fig1.set_size_inches(14, 10)
        print('Iniciando o processso para:', img_name)
        img = cv2.imread(path.join('src', 'images', img_name))
        axs1[0][0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        axs1[0][0].set_title('Imagem Original')
        __createHistogram(img[:, :, 0], axs1[0][1], 'Canal: B')
        __createHistogram(img[:, :, 1], axs1[1][0], 'Canal: G')
        __createHistogram(img[:, :, 2], axs1[1][1], 'Canal: R')
        fig1.savefig(path.join('src', 'output', f'{img_name.split(".")[0]}-original-BGR.jpg'))

        fig1, axs1 = plt.subplots(2, 2)
        fig1.set_size_inches(14, 10)
        print('Equalizando canal B')
        __equalizeHistogram(img[:, :, 0])
        print('Equalizando canal G')
        __equalizeHistogram(img[:, :, 1])
        print('Equalizando canal R')
        __equalizeHistogram(img[:, :, 2])
        axs1[0][0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        axs1[0][0].set_title('Imagem Após Equalização')
        __createHistogram(img[:, :, 0], axs1[0][1], 'Canal: B')
        __createHistogram(img[:, :, 1], axs1[1][0], 'Canal: G')
        __createHistogram(img[:, :, 2], axs1[1][1], 'Canal: R')
        fig1.savefig(path.join('src', 'output', f'{img_name.split(".")[0]}-BGR_Equalizado-BGR.jpg'))

    print('Criando histograma das imagens equalizadas no canal I')
    for img_name in imgs_ei:
        fig1, axs1 = plt.subplots(2, 2)
        fig1.set_size_inches(14, 10)
        img = cv2.imread(path.join('src', 'output', img_name))
        axs1[0][0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        axs1[0][0].set_title('Imagem HSI (I equalizado)')
        __createHistogram(img[:, :, 0], axs1[0][1], 'Canal: B')
        __createHistogram(img[:, :, 1], axs1[1][0], 'Canal: G')
        __createHistogram(img[:, :, 2], axs1[1][1], 'Canal: R')
        fig1.savefig(path.join('src', 'output', f'{img_name.split(".")[0]}-I_Equalizado-BGR.jpg'))

    print('Todos os resultados foram salvos em: output/')