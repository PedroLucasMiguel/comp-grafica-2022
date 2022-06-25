import cv2
import numpy as np
from os import path
from matplotlib import pyplot as plt

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

    # ------------------- Otsu --------------------------
    v_final = -1
    k_f = [] # tresholds

    # Começando o processo de Otsu para duas classes
    # FIX-ME: Expandir para 4 classes
    for k1 in range(0, l):
        print(k1)
        p1 = 0
        for i in range(0, k1 + 1):
            p1 = p1 + (hist[i][1])

        # Calculando P2
        p2 = 1 - p1
        
        if p1 < 1.e-6 or p2 < 1.e-6: # Checagem para evitar divisão por 0
            continue

        # Calculando m1
        m1 = 0
        for i in range(0, k1 + 1):
            m1 = m1 + ((i * hist[i][1]) / p1)

        # Calculando m2
        m2 = 0
        for i in range(k1 + 1, l):
            m2 = m2 + ((i * hist[i][1]) / p2)

        # Calculando para o 2° treshold
        for k2 in range(k1, l):
            #print('b')
            p3 = 1 - p2

            if p3 < 1.e-6:
                print('fuck....')
                continue

            m3 = 0
            for i in range(k2 + 1, l):
                m3 = m3 + ((i * hist[i][1]) / p3)

            # Calculando para o 3° treshold
            for k3 in range(k2, l):
                #print('c')
                p4 = 1 - p3

                if p4 < 1.e-6:
                    continue

                m4 = 0
                for i in range(k3 + 1, l):
                    m4 = m4 + ((i * hist[i][1]) / p4)

                # Calculando para o 4° treshold
                for k4 in range(k3, l):
                    p5 = 1 - p4

                    if p5 < 1.e-6:
                        continue

                    m5 = 0
                    for i in range(k4 + 1, l):
                        m5 = m5 + ((i * hist[i][1]) / p5)

                    # Calculando mt
                    mt = (p1*m1) + (p2*m2) + (p3*m3) + (p4*m4) + (p5*m5)

                    # Calculando variância
                    v = (p1*((m1-mt)**2)) + (p2*((m2-mt)**2)) + (p3*((m3-mt)**2)) + (p4*((m4-mt)**2)) + (p5*((m5-mt)**2))
                    #print(v)
                    if v > v_final:
                        k_f.insert(0, k1)
                        k_f.insert(1, k2)
                        k_f.insert(2, k3)
                        k_f.insert(3, k4)

    print(v_final, k_f)
    '''
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > k_final:
                img[i][j] = 255
            else:
                img[i][j] = 0
    '''
    
    cv2.imwrite(path.join('src', 'output', f'a_plz.png'), img)


if __name__ == '__main__':
    
    img = cv2.imread(path.join('src', 'output', 'help_me.png'), cv2.IMREAD_GRAYSCALE)

    __doOtsu(img)

    #cv2.imwrite(path.join('src', 'output', 'img_seg_r.png'), img)

    #cv2.imwrite(path.join('src', 'output', 'img_seg_gs.png'), img)
