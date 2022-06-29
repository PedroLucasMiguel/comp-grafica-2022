import cv2
import numpy as np
from os import path
from numba import njit

@njit
def __calcNormalizedHistogram(img):
    l = np.amax(img) # Encontra o nível de cinza mais alto
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

    return hist

@njit
def __doOtsu(img):
    hist = __calcNormalizedHistogram(img)
    l = np.amax(img) + 1 # Definindo quantidade de níveis de cinza

    v_max = -1 # Variável que guarda a maior variância
    all_k = [] # Lista que guarda todos os valores de K

    print('Aguarde... O processo pode demorar um pouco.')

    # Calculando possibilidades de K1
    for k1 in range(0, l):
        print(f'Processando.... {k1}/{l-1}')
        
        # Calculando a porcentagem w0
        w0 = 0.0
        for w0a in range(0, k1):
            w0 = w0 + hist[w0a][1]

        # Passa para a próxima iteração se w0 for igual a zero
        if w0 < 1.e-6:
            continue
        
        # Calcula a média u0
        u0 = 0
        for u0a in range(0, k1):
            u0 = u0 + (u0a * hist[u0a][1])/w0

        '''
            O Processo descrito para K1 é análogo aos processos
            de K2 até K4.
        '''

        # k2
        for k2 in range(k1 + 1, l):
            w1 = 0
            for w1a in range(k1, k2):
                w1 = w1 + hist[w1a][1]

            if w1 < 1.e-6:
                continue

            u1 = 0
            for u1a in range(k1, k2):
                u1 = u1 + (u1a * hist[u1a][1])/w1

            # k3
            for k3 in range(k2 + 1, l):
                w2 = 0
                for w2a in range(k2, k3):
                    w2 = w2 + hist[w2a][1]

                if w2 < 1.e-6:
                    continue

                u2 = 0
                for u2a in range(k2, k3):
                    u2 = u2 + (u2a * hist[u2a][1])/w2

                # k4
                for k4 in range(k3 + 1, l):
                    w3 = 0
                    for w3a in range(k3, k4):
                        w3 = w3 + hist[w3a][1]

                    if w3 < 1.e-6:
                        continue

                    u3 = 0
                    for u3a in range(k3, k4):
                        u3 = u3 + (u3a * hist[u3a][1])/w3

                    w4 = 0
                    for w4a in range(k4, l):
                        w4 = w4 + hist[w4a][1]
                    
                    if w4 < 1.e-6:
                        continue

                    u4 = 0
                    for u4a in range(k4, l):
                        u4 = u4 + (u4a * hist[u4a][1])/w4

                    # Calculando a média geral
                    u = (w0 * u0) + (w1 * u1) + (w2 * u2) + (w3 * u3) + (w4 * u4)
                    
                    # Calculando a variância
                    v = (w0*((u-u0)**2)) + (w1*((u-u1)**2)) + (w2*((u-u2)**2)) + (w3*((u-u3)**2)) + (w4*((u-u4)**2))
                    
                    # Verifica se a variância obtida é maior do que a armazenda
                    if v > v_max:
                        v_max = v # Salva a nova variância

                        # Salva os valores de K
                        if len(all_k) == 0:
                            all_k.append(k1)
                            all_k.append(k2)
                            all_k.append(k3)
                            all_k.append(k4)
                        
                        else:
                            all_k[0] = k1
                            all_k[1] = k2
                            all_k[2] = k3
                            all_k[3] = k4

    # Esse método de mostrar os resultados é requerido pelo @njit
    print('\nValores de K:')
    print(all_k)

    print('\nVariancia final:')
    print(v_max)

    img_colored = np.zeros(shape=img.shape, dtype=np.uint8)
    img_k1 = np.zeros(shape=img.shape, dtype=np.uint8)
    img_k2 = np.zeros(shape=img.shape, dtype=np.uint8)
    img_k3 = np.zeros(shape=img.shape, dtype=np.uint8)
    img_k4 = np.zeros(shape=img.shape, dtype=np.uint8)

    # Criando filtro com K1
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > all_k[0]:
                img_k1[i][j] = 255
            else:
                img_k1[i][j] = 0
    
    # Criando filtro com K2
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > all_k[1]:
                img_k2[i][j] = 255
            else:
                img_k2[i][j] = 0

    # Criando filtro com K3
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > all_k[2]:
                img_k3[i][j] = 255
            else:
                img_k3[i][j] = 0

    # Criando filtro com K4
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > all_k[3]:
                img_k4[i][j] = 255
            else:
                img_k4[i][j] = 0

    # Criando imagem com os filtros coloridos
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] > all_k[3]:
                img_colored[i][j] = 255
            elif img[i][j] <= all_k[0] :
                img_colored[i][j] = 0
            elif img[i][j] > all_k[0]  and img[i][j] <= all_k[1] :
                img_colored[i][j] = 60
            elif img[i][j] > all_k[1]  and img[i][j] <= all_k[2] :
                img_colored[i][j] = 130
            elif img[i][j] > all_k[2]  and img[i][j] <= all_k[3] :
                img_colored[i][j] = 180

    return (img_colored, (img_k1, all_k[0]) , (img_k2, all_k[1]), (img_k3, all_k[2]), (img_k4, all_k[3]))
    
def run():
    
    img = cv2.imread(path.join('images', 'img_seg.jpg'), cv2.IMREAD_GRAYSCALE)

    imgs = __doOtsu(img)

    # Salvando mascaras coloridas
    cv2.imwrite(path.join('output', f'masks_colored.png'), cv2.applyColorMap(imgs[0], cv2.COLORMAP_JET))

    # Salvando as mascaras puras
    for i in range(1, len(imgs)):
        cv2.imwrite(path.join('output', f'mask_k_{imgs[i][1]}.png'), imgs[i][0])
    
    img_seg_k1 = np.zeros(shape=img.shape, dtype=np.uint8)
    img_seg_k2 = np.zeros(shape=img.shape, dtype=np.uint8)
    img_seg_k3 = np.zeros(shape=img.shape, dtype=np.uint8)
    img_seg_k4 = np.zeros(shape=img.shape, dtype=np.uint8)
    
    # Salvando imagens segmentadas
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if imgs[1][0][i][j] == 0:
                img_seg_k1[i][j] = img[i][j]
            else:
                img_seg_k1[i][j] = 0
    
    cv2.imwrite(path.join('output', f'seg_k_{imgs[1][1]}.png'), img_seg_k1)
    
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if imgs[2][0][i][j] == 0:
                img_seg_k2[i][j] = img[i][j]
            else:
                img_seg_k2[i][j] = 0

    cv2.imwrite(path.join('output', f'seg_k_{imgs[2][1]}.png'), img_seg_k2)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if imgs[3][0][i][j] == 0:
                img_seg_k3[i][j] = img[i][j]
            else:
                img_seg_k3[i][j] = 0

    cv2.imwrite(path.join('output', f'seg_k_{imgs[3][1]}.png'), img_seg_k3)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if imgs[4][0][i][j] == 0:
                img_seg_k4[i][j] = img[i][j]
            else:
                img_seg_k4[i][j] = 0

    cv2.imwrite(path.join('output', f'seg_k_{imgs[4][1]}.png'), img_seg_k4)

    print('\nImagens salvas em: output')

    
