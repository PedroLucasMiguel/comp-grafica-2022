
import cv2
import numpy as np
from os import path
from math import degrees, cos, radians, pi, acos

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


# Realiza a conversão BGR para HSI
def __bgr2hsi(img):
    
    # Cria a nova imagem
    hsi_img = np.zeros(shape=img.shape, dtype=float)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # Valores BGR são normalizados
            B = img[i][j][0]/255.0 
            G = img[i][j][1]/255.0
            R = img[i][j][2]/255.0

            H = 0.0
            S = 0.0
            I = 0.0

            n = 0.5 * ((R - G) + (R - B)) # Numerador
            d = np.sqrt(((R - G)**2) + (R - B) * (G - B)) # Denominador
            theta=acos(n/d)

            if d == 0:
                H = 0
            elif B <= G:
                H = theta
            else:
                H = 2 * pi - theta

            min_bgr = min(B, G ,R)
            sum = B + G + R

            if sum == 0:
                S = 0
            else:
                S = 1.0 - 3.0 * min_bgr/sum

            I = sum/3.0

            # Aplica os valores de H,S,I em cada um dos canais da nova imagem criada
            hsi_img[i][j][0] = H
            hsi_img[i][j][1] = S
            hsi_img[i][j][2] = I
            
    
    return hsi_img

def __hsi2bgr(img):

    img_bgr = np.zeros(shape=img.shape, dtype=int)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            # Lê os valores HSI da imagem de entrada
            H = img[i][j][0]
            S = img[i][j][1]
            I = img[i][j][2]

            R = 0
            G = 0
            B = 0
            
            H = degrees(H)

            # Começa o processo de conversão
            if 0 <= H <= 120 :
                B = I * (1 - S)
                R = I * (1 + (S * cos(radians(H)) / cos(radians(60) - radians(H))))
                G = I * 3 - (R + B)
            elif 120 < H <= 240:
                H -= 120
                R = I * (1 - S)
                G = I * (1 + (S * cos(radians(H)) / cos(radians(60) - radians(H))))
                B = 3 * I - (R + G)
            elif 0 < H <= 360:
                H -= 240
                G = I * (1 - S)
                B = I * (1 + (S * cos(radians(H)) / cos(radians(60) - radians(H))))
                R = I * 3 - (G + B)

            img_bgr[i][j][0] = np.clip(round(B * 255.0), 0, 255)
            img_bgr[i][j][1] = np.clip(round(G * 255.0), 0, 255)
            img_bgr[i][j][2] = np.clip(round(R * 255.0), 0, 255)

    return img_bgr

if __name__ == '__main__':

    imgs = ['img1.bmp', 'img2.bmp', 'img3.JPG']

    for img_name in imgs:
        print('Iniciando o processso para:', img_name)
        img = cv2.imread(path.join('src', 'images', img_name))
        hsi_img = __bgr2hsi(img)

        # Criando matriz adicional para realizar o processamento necessário no canal I
        aux = np.zeros(shape=(hsi_img.shape[0], hsi_img.shape[1]), dtype=int)

        for i in range(hsi_img.shape[0]):
            for j in range(hsi_img.shape[1]):
                aux[i][j] = int(hsi_img[i][j][2]*255)

        print('Equalizando histograma...')
        __equalizeHistogram(aux)

        for i in range(hsi_img.shape[0]):
            for j in range(hsi_img.shape[1]):
                hsi_img[i][j][2] = aux[i][j]/255
        
        print('Convertendo HSI -> BGR')
        cv2.imwrite(path.join('src', 'output', f"{img_name.split('.')[0]}-eI.jpg"), __hsi2bgr(hsi_img))