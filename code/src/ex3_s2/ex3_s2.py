import random
import numpy as np
import cv2
from math import sqrt
from os import path
import csv

# Código retirado de: https://www.geeksforgeeks.org/add-a-salt-and-pepper-noise-to-an-image-with-python/#:~:text=Salt%2Dand%2Dpepper%20noise%20is,%2C%20bit%20transmission%20error%2C%20etc.&text=Below%20is%20the%20implementation%3A,Python
def salt_and_peper_noise(img):
 
    # Getting the dimensions of the image
    row , col = img.shape
     
    # Randomly pick some pixels in the
    # image for coloring them white
    # Pick a random number between 300 and 10000
    number_of_pixels = random.randint(300, 10000)
    for i in range(number_of_pixels):
       
        # Pick a random y coordinate
        y_coord=random.randint(0, row - 1)
         
        # Pick a random x coordinate
        x_coord=random.randint(0, col - 1)
         
        # Color that pixel to white
        img[y_coord][x_coord] = 255
         
    # Randomly pick some pixels in
    # the image for coloring them black
    # Pick a random number between 300 and 10000
    number_of_pixels = random.randint(300 , 10000)
    for i in range(number_of_pixels):
       
        # Pick a random y coordinate
        y_coord=random.randint(0, row - 1)
         
        # Pick a random x coordinate
        x_coord=random.randint(0, col - 1)
         
        # Color that pixel to black
        img[y_coord][x_coord] = 0
         
    return img

# Ruído uniforme
def uniform_noise(o_img):
    row, col = o_img.shape

    colors = []

    for i in range(100, 201, 10):
        colors.append(i)

    for i in range(row):
        for j in range(col):
            for c in range(len(colors)):
                if np.random.uniform(0, 1) <= 0.01:
                    o_img[i][j] = colors[c]
                    break
    
    return o_img

# Ruído gaussiano
def gausian_noise(o_img):
    row, col = o_img.shape

    colors = []

    for i in range(0, 101, 10):
        colors.append(i)

    for i in range(row):
        for j in range(col):
            for c in range(len(colors)):
                if np.random.normal() <= 0.00000001:
                    o_img[i][j] = o_img[i][j] + colors[c]
                    break
    
    return o_img

# ------------------------------------------------------------------------------------------

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
                if int(i1[i][j]) - int(i2[i][j]) <= 25.5: # 25.5 valor de tolerância
                    v.append(1)
                else:
                    v.append(0)
        
        v = sum(v)

        return v/(row * col)


# Aplicando os ruidos nas imagens
def apply_noises():
    img_a = cv2.imread(path.join('code/src/images', 'a.jpg'), cv2.IMREAD_GRAYSCALE)
    img_b = cv2.imread(path.join('code/src/images', 'b.jpg'), cv2.IMREAD_GRAYSCALE)
    img_c = cv2.imread(path.join('code/src/images', 'c.jpg'), cv2.IMREAD_GRAYSCALE)

    # Sal e pimenta
    cv2.imwrite(path.join('code/src/output', 'a_sp.jpg'), salt_and_peper_noise(img_a))
    cv2.imwrite(path.join('code/src/output', 'b_sp.jpg'), salt_and_peper_noise(img_b))
    cv2.imwrite(path.join('code/src/output', 'c_sp.jpg'), salt_and_peper_noise(img_c))

    # Uniforme
    cv2.imwrite(path.join('code/src/output', 'a_u.jpg'), uniform_noise(img_a))
    cv2.imwrite(path.join('code/src/output', 'b_u.jpg'), uniform_noise(img_b))
    cv2.imwrite(path.join('code/src/output', 'c_u.jpg'), uniform_noise(img_c))

    # Gaussiando
    cv2.imwrite(path.join('code/src/output', 'a_g.jpg'), gausian_noise(img_a))
    cv2.imwrite(path.join('code/src/output', 'b_g.jpg'), gausian_noise(img_b))
    cv2.imwrite(path.join('code/src/output', 'c_g.jpg'), gausian_noise(img_c))

def calcerrors():
    img_a = cv2.imread(path.join('code/src/images', 'a.jpg'), cv2.IMREAD_GRAYSCALE)
    img_b = cv2.imread(path.join('code/src/images', 'b.jpg'), cv2.IMREAD_GRAYSCALE)
    img_c = cv2.imread(path.join('code/src/images', 'c.jpg'), cv2.IMREAD_GRAYSCALE)

    # Sal e pimenta
    img_a_sp = cv2.imread(path.join('code/src/output', 'a_sp.jpg'), cv2.IMREAD_GRAYSCALE)
    img_b_sp = cv2.imread(path.join('code/src/output', 'b_sp.jpg'), cv2.IMREAD_GRAYSCALE)
    img_c_sp = cv2.imread(path.join('code/src/output', 'c_sp.jpg'), cv2.IMREAD_GRAYSCALE)

    # Uniforme
    img_a_u = cv2.imread(path.join('code/src/output', 'a_u.jpg'), cv2.IMREAD_GRAYSCALE)
    img_b_u = cv2.imread(path.join('code/src/output', 'b_u.jpg'), cv2.IMREAD_GRAYSCALE)
    img_c_u = cv2.imread(path.join('code/src/output', 'c_u.jpg'), cv2.IMREAD_GRAYSCALE)

    # Gaussiano
    img_a_g = cv2.imread(path.join('code/src/output', 'a_g.jpg'), cv2.IMREAD_GRAYSCALE)
    img_b_g = cv2.imread(path.join('code/src/output', 'b_g.jpg'), cv2.IMREAD_GRAYSCALE)
    img_c_g = cv2.imread(path.join('code/src/output', 'c_g.jpg'), cv2.IMREAD_GRAYSCALE)


    with open(path.join('code/src/output', 'results.txt'), 'w', newline='') as f:

        f.writelines(['Imagem | ', 'Erro máximo | ', 'Erro médio absoluto | ', 'Erro médio quadrático | ', 'Raiz do erro médio quadrático | ', 'Coeficiente de Jaccard | \n\n'])
        
        f.writelines([
            'A (Sal e pimenta) ',
            f'| {max_error(img_a, img_a_sp)} ',
            f'| {mean_absolute_error(img_a, img_a_sp)} ',
            f'| {mean_square_error(img_a, img_a_sp)} ',
            f'| {root_mean_square_error(img_a, img_a_sp)} ',
            f'| {jaccard(img_a, img_a_sp)} \n\n'
        ])

        f.writelines([
            'A (Uniforme) ',
            f'| {max_error(img_a, img_a_u)} ',
            f'| {mean_absolute_error(img_a, img_a_u)} ',
            f'| {mean_square_error(img_a, img_a_u)} ',
            f'| {root_mean_square_error(img_a, img_a_u)} ',
            f'| {jaccard(img_a, img_a_u)} \n\n'
        ])

        f.writelines([
            'A (Gausiano) ',
            f'| {max_error(img_a, img_a_g)} ',
            f'| {mean_absolute_error(img_a, img_a_g)} ',
            f'| {mean_square_error(img_a, img_a_g)} ',
            f'| {root_mean_square_error(img_a, img_a_g)} ',
            f'| {jaccard(img_a, img_a_g)} \n\n'
        ])

        f.write('-'*120 + '\n\n')

        f.writelines([
            'B (Sal e pimenta) ',
            f'| {max_error(img_b, img_b_sp)} ',
            f'| {mean_absolute_error(img_b, img_b_sp)} ',
            f'| {mean_square_error(img_b, img_b_sp)} ',
            f'| {root_mean_square_error(img_b, img_b_sp)} ',
            f'| {jaccard(img_b, img_b_sp)} \n\n'
        ])

        f.writelines([
            'B (Uniforme) ',
            f'| {max_error(img_b, img_b_u)} ',
            f'| {mean_absolute_error(img_b, img_b_u)} ',
            f'| {mean_square_error(img_b, img_b_u)} ',
            f'| {root_mean_square_error(img_b, img_b_u)} ',
            f'| {jaccard(img_b, img_b_u)} \n\n'
        ])

        f.writelines([
            'B (Gaussiano) ',
            f'| {max_error(img_b, img_b_g)} ',
            f'| {mean_absolute_error(img_b, img_b_g)} ',
            f'| {mean_square_error(img_b, img_b_g)} ',
            f'| {root_mean_square_error(img_b, img_b_g)} ',
            f'| {jaccard(img_b, img_b_g)} \n\n'
        ])

        f.write('-'*120 + '\n\n')

        f.writelines([
            'C (Sal e pimenta) ',
            f'| {max_error(img_c, img_c_sp)} ',
            f'| {mean_absolute_error(img_c, img_c_sp)} ',
            f'| {mean_square_error(img_c, img_c_sp)} ',
            f'| {root_mean_square_error(img_c, img_c_sp)} ',
            f'| {jaccard(img_c, img_c_sp)} \n\n'
        ])

        f.writelines([
            'C (Uniforme) ',
            f'| {max_error(img_c, img_c_u)} ',
            f'| {mean_absolute_error(img_c, img_c_u)} ',
            f'| {mean_square_error(img_c, img_c_u)} ',
            f'| {root_mean_square_error(img_c, img_c_u)} ',
            f'| {jaccard(img_c, img_c_u)} \n\n'
        ])

        f.writelines([
            'C (Gaussiano) ',
            f'| {max_error(img_c, img_c_g)} ',
            f'| {mean_absolute_error(img_c, img_c_g)} ',
            f'| {mean_square_error(img_c, img_c_g)} ',
            f'| {root_mean_square_error(img_c, img_c_g)} ',
            f'| {jaccard(img_c, img_c_g)} \n\n'
        ])

        print("Arquivo de saída com os resultados: " + path.join('code/src/output', 'results.txt'))

if __name__ == '__main__':
    apply_noises()
    calcerrors()
