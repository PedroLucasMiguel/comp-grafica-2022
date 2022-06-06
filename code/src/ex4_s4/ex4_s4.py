import random
import numpy as np
import cv2
from math import sqrt
from os import path
import os

# Erro Máximo
def max_error(i1, i2):

    if (i1.shape != i2.shape):
        print("Tamanhos de imagens diferentes!")
    
    else:
        v = []
        row, col = i1.shape

        for i in range(row):
            for j in range(col):
                v.append(abs(int(i1[i][j]) - int(i2[i][j])))
    

        return max(v)

# Erro médio absoluto
def mean_absolute_error(i1, i2):

    if (i1.shape != i2.shape):
        print("Tamanhos de imagens diferentes!")
    
    else:
        v = []
        row, col = i1.shape

        for i in range(row):
            for j in range(col):
                v.append(abs(int(i1[i][j]) - int(i2[i][j])))
        
        v = sum(v)

        return v/(row * col)


# Erro médio quadrático
def mean_square_error(i1, i2):

    if (i1.shape != i2.shape):
        print("Tamanhos de imagens diferentes!")
    
    else:
        v = []
        row, col = i1.shape

        for i in range(row):
            for j in range(col):
                v.append(pow(int(i1[i][j]) - int(i2[i][j]), 2))
        
        v = sum(v)

        return v/(row * col)

# Raiz do erro médio quadrático
def root_mean_square_error(i1, i2):

    if (i1.shape != i2.shape):
        print("Tamanhos de imagens diferentes!")
    
    else:
        v = []
        row, col = i1.shape

        for i in range(row):
            for j in range(col):
                v.append(pow(int(i1[i][j]) - int(i2[i][j]), 2))
        
        v = sum(v)

        return sqrt(v/(row * col))

# Coeficiente de jaccard
def jaccard(i1, i2):

    if (i1.shape != i2.shape):
        print("Tamanhos de imagens diferentes!")
    
    else:
        v = []
        row, col = i1.shape

        for i in range(row):
            for j in range(col):
                if abs(int(i1[i][j]) - int(i2[i][j])) <= 25.5: # 25.5 = valor de tolerância
                    v.append(1)
                else:
                    v.append(0)
        
        v = sum(v)

        return v/(row * col)

# -----------------------------------------------------------------------------------------------

# Calculo de correção gamma
def __calc_gamma_correction(f, y):
    return pow((f/255), 1/y)*255

# Realiza o processo de correção
def __do_gamma_correction(f, f_name):
    s = f.shape
    i = np.array([])
    i2 = np.array([])

    for y in range(s[0]):
        for x in range(s[1]):
            i = np.append(i, __calc_gamma_correction(f[y][x], 0.4))
            i2 = np.append(i2, __calc_gamma_correction(f[y][x], 0.04))
    
    i = np.reshape(i, f.shape)
    i2 = np.reshape(i2, f.shape)
    cv2.imwrite(path.join('output', f'{f_name}_gc4.jpg'), i)
    cv2.imwrite(path.join('output', f'{f_name}_gc04.jpg'), i2)

def gamma_correction():
    print('Aplicando correcao gama...')
    file_names = ['a', 'b', 'c']
    image_types = ['sp', 'u', 'g']

    for f_name in file_names:
        for types in image_types:
            print(f'Processando: {f_name}_{types}.jpg')
            __do_gamma_correction(cv2.imread(path.join(f'images', f'{f_name}_{types}.jpg'), cv2.IMREAD_GRAYSCALE), f'{f_name}_{types}')


# -----------------------------------------------------------------------------------------------

def calcerrors():

    file_names = ['a', 'b', 'c']

    image_types = ['sp', 'u', 'g']

    y_value = ['gc4', 'gc04']

    original_images = []

    all_gamma_images = []

    # Abrindo todas as imagens originais e colocando no vetor
    for f_name in file_names:
        original_images.append(cv2.imread(path.join('images', f'{f_name}.jpg'), cv2.IMREAD_GRAYSCALE))
    
    # Criando os dicionarios com todas as imagens "corrigidas"
    for f_index in range(len(file_names)):
        all_gamma_images.append({})
        for types in image_types:
            for y in y_value:
                all_gamma_images[f_index][f'{file_names[f_index]}_{types}_{y}.jpg'] = cv2.imread(path.join('output', f'{file_names[f_index]}_{types}_{y}.jpg'), cv2.IMREAD_GRAYSCALE)

    
    print('Gerando arquivo de saída....')
    with open(path.join('output', 'results.txt'), 'w', newline='') as f:
        
        f.writelines(['Imagem | ', 'Erro maximo | ', 'Erro medio absoluto | ', 'Erro medio quadratico | ', 'Raiz do erro medio quadratico | ', 'Coeficiente de Jaccard | \n\n'])
        
        for o_image in range(len(file_names)):

            if o_image != 0:
                f.write(('-'*130) + '\n\n')

            for g_image in all_gamma_images[o_image].keys():
                f.writelines([
                    f'{g_image} ',
                    f'| {max_error(original_images[o_image], all_gamma_images[o_image][g_image])} ',
                    f'| {mean_absolute_error(original_images[o_image], all_gamma_images[o_image][g_image])} ',
                    f'| {mean_square_error(original_images[o_image], all_gamma_images[o_image][g_image])} ',
                    f'| {root_mean_square_error(original_images[o_image], all_gamma_images[o_image][g_image])} ',
                    f'| {jaccard(original_images[o_image], all_gamma_images[o_image][g_image])} \n\n'
                ])

                

    print("Arquivo de saída com os resultados: " + path.join('output', 'results.txt'))

def run():
    gamma_correction()
    calcerrors()
