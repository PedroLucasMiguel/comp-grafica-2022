from hashlib import new
from matplotlib.font_manager import json_dump
import numpy as np
import cv2
from math import dist, floor, sqrt
from os import path
from matplotlib import pyplot as plt
import json

# ----------------------------------------- Métricas ----------------------------------------------------------

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
                if abs(int(i1[i][j]) - int(i2[i][j])) <= 10: # 10 = valor de tolerância
                    v.append(1)
                else:
                    v.append(0)
        
        v = sum(v)

        return v/(row * col)

# ----------------------------------------- Ruídos ----------------------------------------------------------
# Ruído sal e pimenta
def salt_and_peper_noise(img, dist):
    
    img_shape = img.shape

    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            if np.random.uniform(0, 1) <= dist/100:
                color = np.random.randint(0, 2)
                img[i, j] = (255 if color == 0 else 0)
         
    return img

# Ruído gaussiano
def gausian_noise(img, dist):

    row, col = img.shape
    colors = []

    for i in range(0, 101, 5):
        colors.append(i)

    for i in range(row):
        for j in range(col):
            if abs(np.random.normal(0, 0.25)) <= dist/100:
                p_color = img[i, j] + colors[np.random.randint(0, len(colors))]
                img[i, j] = p_color if p_color <= 255 else 255

    return img
# ----------------------------------------- Filtros ----------------------------------------------------------

def __do_convolution(img, kernel):
    g = np.zeros(shape=img.shape)

    for i1 in range(img.shape[0]):
        for j1 in range(img.shape[1]):
            s = 0
            for i2 in range(kernel.shape[0]):
                for j2 in range(kernel.shape[1]):
                    s = s + (kernel[i2][j2] * img[i1-i2][j1-j2])
                    
            g[i1][j1] = s

    return g

def mean_filter(img, kernel_size):
    kernel = []

    # Criando o kernel
    for i in range(kernel_size):
        kernel.append([])
        for j in range(kernel_size):
            kernel[i].append(1/(kernel_size*kernel_size))

    kernel = np.array(kernel, dtype=float)

    return __do_convolution(img, kernel)


def median_filter(img, kernel_size):

    new_img = np.zeros(shape=img.shape)

    # Calculando a mediana
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            '''
                Podemos ignorar o processo de zero padding neste caso,
                pois o  próprio python nos fornece uma abstração para acessar os elementos 
                MxN elementos, ignorando possíveis posições que não existam em uma matriz,
                retornando apenas os elementos existentes no intervalo. 
            '''
            aux = img[i:i + kernel_size, j:j + kernel_size] 
            aux = aux.flatten()
            aux.sort()

            new_img[i][j] = np.median(aux)

    return new_img

def gaussian_filter(img, kernel_size):

    pascal_values = np.zeros(shape=(kernel_size, kernel_size))

    # Calculando o triângulo de pascal
    for i in range (kernel_size):
        for j in range (0, i + 1):

            if(j == 0 or j == i):
                pascal_values[i][j] = 1
 
            else:
                pascal_values[i][j] = (pascal_values[i - 1][j - 1] + pascal_values[i - 1][j])
    
    v_sum = pascal_values[kernel_size-1].sum()

    kernel = np.zeros(shape=(kernel_size, kernel_size), dtype=float)

    # Preenchendo linha
    kernel[0, 0:kernel_size] = pascal_values[kernel_size-1][0:kernel_size]
    
    # Preenchendo coluna
    kernel[:, 0] = pascal_values[kernel_size-1][0:kernel_size]
    
    # Preencher o resto do kernel
    for i in range(1, kernel_size):
        for j in range(1, kernel_size):
            kernel[i][j] = (kernel[i-i][j] * kernel[i][j-j])
    
    for i in range(kernel_size):
        for j in range(kernel_size):
            kernel[i][j] = kernel[i][j] * (1/(v_sum*v_sum))
    
    return __do_convolution(img, kernel)

# ---------------------------- Calculando métricas ----------------------------------------------

def run():

    image_names = ['a', 'b', 'c']

    image_filters = {
        'mean' : mean_filter,
        'median': median_filter,
        'gaus' : gaussian_filter,
    }

    kernels_sizes = [3, 5]

    original_images = []
    images_with_noise = {}
    images_with_filter = {}

    dist_sp = 0
    dist_gaus = 0
    stop = False
    
    while not stop:
        print('Digite o valor da distribuição para o ruído "Sal e Pimenta" em %')
        dist_sp = float(input('Resposta: '))

        if dist_sp <= 0 or dist_sp > 100:
            print('\nERRO: Use distribuições entre 0-100%\n')
        
        else:
            stop = True

    stop = False

    while not stop:
        print('Digite o valor da distribuição para o ruído "Gaussiano" em %')
        dist_gaus = float(input('Resposta: '))

        if dist_gaus <= 0 or dist_gaus > 100:
            print('\nERRO: Use distribuições entre 0-100%\n')
        
        else:
            stop = True

    print('\nIniciando....')

    for i in range(len(image_names)):

        print(f'Aplicando ruídos na imagem "{image_names[i]}.jpg"')

        original_images.append(cv2.imread(path.join('images', f'{image_names[i]}.jpg'), cv2.IMREAD_GRAYSCALE)) # Salvando as imagens originais

        images_with_noise[image_names[i]] = [] # Criando os arrays que terão as imagens com ruído

        # Sal e pimenta
        images_with_noise[image_names[i]].append(salt_and_peper_noise(original_images[i].copy(), dist_sp))
        cv2.imwrite(path.join('output', f'{image_names[i]}_sp_{dist_sp}.png'), images_with_noise[image_names[i]][0])

        # Gaussiano
        images_with_noise[image_names[i]].append(gausian_noise(original_images[i].copy(), dist_gaus))
        cv2.imwrite(path.join('output', f'{image_names[i]}_gaus_{dist_gaus}.png'), images_with_noise[image_names[i]][1])

    # Criando imagens corrigidas
    for i in image_names:
        images_with_filter[i] = {} # 1° Chave: nome simples da imagem
        for f in image_filters.keys():
            images_with_filter[i][f] = [] # 2° Chave: Filtro da imagem
            print(f'Aplicando filtro "{f}" nas imagens "{i}"')
            for k in kernels_sizes:
                aux = image_filters[f](images_with_noise[i][0], k)
                cv2.imwrite(path.join('output', f'{i}(f)_sp_{f}_{k}.png'), img=aux)
                images_with_filter[i][f].append(aux)

                aux = image_filters[f](images_with_noise[i][1], k)
                cv2.imwrite(path.join('output', f'{i}(f)_gaus_{f}_{k}.png'), img=aux)
                images_with_filter[i][f].append(aux)

    quick_translate = {
        0: '(Sal e Pimenta) k = 3',
        1: '(Sal e Pimenta) k = 5',
        2: '(Gaussiano) k = 3',
        3: '(Gaussiano) k = 5'
    }

    print('Gerando arquivo com as métricas de erro...')

    # Calculando os erros e exportando para um arquivo         
    with open(path.join('output', 'results.txt'), 'w', newline='') as f:
        
        f.writelines(['Imagem | ', 'Erro maximo | ', 'Erro medio absoluto | ', 'Erro medio quadratico | ', 'Raiz do erro medio quadratico | ', 'Coeficiente de Jaccard | \n\n'])
        
        for o_image in range(len(original_images)):

            if o_image != 0:
                f.write(('-'*130) + '\n\n')
            
            for filter in images_with_filter[image_names[o_image]].keys():
                for f_image in range(len(images_with_filter[image_names[o_image]][filter])):
                    f.writelines([
                        f'{image_names[o_image]} {quick_translate[f_image]} ({filter}) ',
                        f'| {max_error(original_images[o_image], images_with_filter[image_names[o_image]][filter][f_image])} ',
                        f'| {mean_absolute_error(original_images[o_image], images_with_filter[image_names[o_image]][filter][f_image])} ',
                        f'| {mean_square_error(original_images[o_image], images_with_filter[image_names[o_image]][filter][f_image])} ',
                        f'| {root_mean_square_error(original_images[o_image], images_with_filter[image_names[o_image]][filter][f_image])} ',
                        f'| {jaccard(original_images[o_image], images_with_filter[image_names[o_image]][filter][f_image])} \n\n'
                    ])                

    print("Os arquivos de saída se encontram em: output")

    pass