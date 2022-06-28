from turtle import right
import cv2
import numpy as np
from os import path
from matplotlib import pyplot as plt
from math import floor
from numba import njit

def __do_one_Otsu(img):

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

@njit
def __doOtsu(img):
    l = np.amax(img)
    qtd_pixels = img.shape[0] * img.shape[1]
    
    hist = []

    # Criando a tabela base do histograma
    for i in range(l+1):
        hist.insert(i, [i, 0.0])

    # Preenchendo tabela base
    for i in img:
        for j in i:
            hist[j][1] = hist[j][1] + 1

    # Normalizando histograma
    for i in range(l+1):
        hist[i][1] = float(hist[i][1]/qtd_pixels)
    
    # -------------------------------------------------------------
    v_final = -1
    k_fe = []

    # Começando o processo de Otsu para duas classes
    for k1 in range(0, 63):
        print(k1)
        p1 = 0
        for i in range(0, k1 + 1):
            p1 = p1 + (hist[i][1])

        # Calculando P2
        p2 = 0
        for i in range(k1 + 1, 63):
            p2 = p2 + (hist[i][1])

        if p1 < 1.e-6 or p2 < 1.e-6:
            continue

        # Calculando m1
        m1 = 0
        for i in range(0, k1 + 1):
            m1 = m1 + ((i * hist[i][1]) / p1)

        # Calculando m2
        m2 = 0
        for i in range(k1 + 1, l):
            m2 = m2 + ((i * hist[i][1]) / p2)

        for k2 in range(k1 + 1, 126):
            p3 = 0
            for i in range(k2 + 1, 126):
                p3 = p3 + (hist[i][1])
            if p3 < 1.e-6:
                continue

            m3 = 0
            for i in range(k2 + 1, l):
                m3 = m3 + ((i * hist[i][1]) / p3)
            
            for k3 in range(k2+1, 189):
                p4 = 0
                for i in range(k3 + 1, 189):
                    p4 = p4 + (hist[i][1])
                if p4 < 1.e-6:
                    continue

                m4 = 0
                for i in range(k3 + 1, l):
                    m4 = m4 + ((i * hist[i][1]) / p4)

                for k4 in range(k3+1, 256):
                    
                    p5 = 0
                    for i in range(k4 + 1, 256):
                        p5 = p5 + (hist[i][1])

                    if p5 < 1.e-6:
                        continue

                    m5 = 0
                    for i in range(k4 + 1, 256):
                        m5 = m5 + ((i * hist[i][1]) / p5)

                    # Calculando mt
                    mt = (p1*m1) + (p2*m2) + (p3*m3) + (p4*m4) + (p5*m5)

                    # Calculando variância
                    v = (p1*((m1-mt)**2)) + (p2*((m2-mt)**2)) + (p3*((m3-mt)**2)) + (p4*((m4-mt)**2)) + (p5*((m5-mt)**2))
                
                    if v > v_final:
                        if len(k_fe) == 0:
                            v_final = v
                            k_fe.append(k1)
                            k_fe.append(k2)
                            k_fe.append(k3)
                            k_fe.append(k4)
                    
                        else:
                            k_fe[0] = k1
                            k_fe[1] = k2
                            k_fe[2] = k3
                            k_fe[3] = k4
    
    print(v, k_fe)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > k_fe[3]:
                img[i][j] = 255
            elif img[i][j] <= k_fe[0] :
                img[i][j] = 0
            elif img[i][j] > k_fe[0]  and img[i][j] <= k_fe[1] :
                img[i][j] = 60
            elif img[i][j] > k_fe[1]  and img[i][j] <= k_fe[2] :
                img[i][j] = 130
            elif img[i][j] > k_fe[2]  and img[i][j] <= k_fe[3] :
                img[i][j] = 180


    '''
    img1 = np.zeros(shape=img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > k_fe[0]:
                img1[i][j] = 255
            else:
                img1[i][j] = 0

    img2 = np.zeros(shape=img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > k_fe[1]:
                img2[i][j] = 255
            else:
                img2[i][j] = 0

    img3 = np.zeros(shape=img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > k_fe[2]:
                img3[i][j] = 255
            else:
                img3[i][j] = 0

    img4 = np.zeros(shape=img.shape)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > k_fe[3]:
                img4[i][j] = 255
            else:
                img4[i][j] = 0
    
    return (img1, img2, img3, img4)
    '''

    return img
    
if __name__ == '__main__':
    
    img = cv2.imread(path.join('src', 'images', 'img_seg.jpg'), cv2.IMREAD_GRAYSCALE)

    cv2.imwrite(path.join('src', 'output', f'a_plz.png'), cv2.applyColorMap(__doOtsu(img), cv2.COLORMAP_JET) )
    #imgs = __doOtsu(img)
    #cv2.imwrite(path.join('src', 'output', f'1.png'), imgs[0])
    #cv2.imwrite(path.join('src', 'output', f'2.png'), imgs[1])
    #cv2.imwrite(path.join('src', 'output', f'3.png'), imgs[2])
    #cv2.imwrite(path.join('src', 'output', f'4.png'), imgs[3])
