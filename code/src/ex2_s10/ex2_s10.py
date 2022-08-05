from genericpath import isfile
import cv2
import numpy as np
from os import path
from math import floor, log2
import matplotlib.pyplot as plt

# Responsável pela criação de histogramas
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

def __deviation(img):
    
    n = img.shape[0] * img.shape[1]
    s = 0.0

    # Calculando a média
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            s = s + img[i][j]

    s = s/n

    d = 0

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            d = d + ((img[i][j] - s)**2)

    return d/n


def run():
    imgs = ['img1.bmp', 'img2.bmp', 'img3.JPG']
    imgs_ei = ['img1-eI.jpg', 'img2-eI.jpg', 'img3-eI.jpg']

    stop = False
    i = 0

    while not stop:
        print('Escolha a imagem:')
        print('[0] - img1.bmp')
        print('[1] - img2.bmp')
        print('[2] - img3.JPG\n')
        print('[3] - Sair')
        i = int(input('Resposta: '))

        if i < 0 or i > 3:
            print('Valor inválido!')
        
        elif i == 3:
            stop = True

        else:
            print('\n\nIniciando o processso para:', imgs[i])
            img = cv2.imread(path.join('images', imgs[i]))

            # Criando os histogramas para a imagem original
            fig1, axs1 = plt.subplots(2, 2)
            fig1.set_size_inches(14, 10)
            axs1[0][0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            axs1[0][0].set_title('Imagem Original')
            __createHistogram(img[:, :, 0], axs1[0][1], 'Canal: B')
            __createHistogram(img[:, :, 1], axs1[1][0], 'Canal: G')
            __createHistogram(img[:, :, 2], axs1[1][1], 'Canal: R')
            fig1.savefig(path.join('output', f'{imgs[i].split(".")[0]}-original-BGR.jpg'))

            # Equalizando a imagem
            print('Equalizando os canais B-G-R da figura:', imgs[i])
            print('Equalizando canal B')
            __equalizeHistogram(img[:, :, 0])
            print('Equalizando canal G')
            __equalizeHistogram(img[:, :, 1])
            print('Equalizando canal R')
            __equalizeHistogram(img[:, :, 2])

            # Calculando variância
            print(f"\nVariância em B: {__deviation(img[:, :, 0])}")
            print(f"Variância em G: {__deviation(img[:, :, 1])}")
            print(f"Variância em R: {__deviation(img[:, :, 2])}\n")

            # Plota a imagem equalizada
            fig1, axs1 = plt.subplots(2, 2)
            fig1.set_size_inches(14, 10)
            axs1[0][0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            axs1[0][0].set_title('Imagem Após Equalização dos Três Canais')
            __createHistogram(img[:, :, 0], axs1[0][1], 'Canal: B')
            __createHistogram(img[:, :, 1], axs1[1][0], 'Canal: G')
            __createHistogram(img[:, :, 2], axs1[1][1], 'Canal: R')
            fig1.savefig(path.join('output', f'{imgs[i].split(".")[0]}-BGR_Equalizado-BGR.jpg'))

            # Caso as imagens equalizadas no canal I já tenham sido geradas, cria o histograma das mesmas
            if path.isfile(path.join('output', imgs_ei[i])):
                img = cv2.imread(path.join('output', imgs_ei[i]))
                
                # Criando o plot
                print('Criando histograma das imagens equalizadas no canal I')
                fig1, axs1 = plt.subplots(2, 2)
                fig1.set_size_inches(14, 10)
                axs1[0][0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                axs1[0][0].set_title('Imagem HSI (I equalizado)')
                __createHistogram(img[:, :, 0], axs1[0][1], 'Canal: B')
                __createHistogram(img[:, :, 1], axs1[1][0], 'Canal: G')
                __createHistogram(img[:, :, 2], axs1[1][1], 'Canal: R')
                fig1.savefig(path.join('output', f'{imgs_ei[i].split(".")[0]}-I_Equalizado-BGR.jpg'))

                # Calculando variância
                print(f"\nVariância em B: {__deviation(img[:, :, 0])}")
                print(f"Variância em G: {__deviation(img[:, :, 1])}")
                print(f"Variância em R: {__deviation(img[:, :, 2])}\n")

                print('Todos os resultados foram salvos em: output/')
                input('Pressine ENTER para continuar')
            
            else:
                print('\nERRO! ARQUIVO DE EQUALIZAÇÃO NO CANAL I NÃO ESTA PRESENTE NA PASTA output/!')
                print('Execute o Exercício 10 e tente novamente')
                stop = True