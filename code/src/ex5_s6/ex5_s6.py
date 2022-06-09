import numpy as np
import cv2
from math import floor, sqrt
from os import path
from matplotlib import pyplot as plt

# Código adaptado de: https://www.geeksforgeeks.org/add-a-salt-and-pepper-noise-to-an-image-with-python/#:~:text=Salt%2Dand%2Dpepper%20noise%20is,%2C%20bit%20transmission%20error%2C%20etc.&text=Below%20is%20the%20implementation%3A,Python
def salt_and_peper_noise(img, dist):
    
    img_shape = img.shape

    for i in range(img_shape[0]):
        for j in range(img_shape[1]):
            if np.random.uniform(0, 1) <= dist/100:
                color = np.random.randint(0, 2)
                img[i][j] = (255 if color == 0 else 0)
         
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
                p_color = img[i][j] + colors[np.random.randint(0, len(colors))]
                img[i][j] = p_color if p_color <= 255 else 255

    return img
# ---------------------------------------------------------------------------------------------------

def __zero_padding(img, padding_size):
    # Fazendo o padding da imagem
    padding_img = np.zeros((img.shape[0] + padding_size, img.shape[1] + padding_size))
    
    # Colocando a imagem dentro do padding
    for i in range(padding_size, padding_img.shape[0] - padding_size):
        for j in range(padding_size, padding_img.shape[1] - padding_size):
            padding_img[i][j] = img[i-padding_size][j-padding_size]
    
    return padding_img

def mean_filter(img, kernel_size):
    kernel = []

    # Criando o kernel
    for i in range(kernel_size):
        kernel.append([])
        for j in range(kernel_size):
            kernel[i].append(1/(kernel_size*kernel_size))

    kernel = np.array(kernel, dtype=float)
    print(kernel)

    # Realiza o zero padding na imagem
    padding_img = __zero_padding(img, kernel_size - 1)

    # Nova imagem
    new_img = np.zeros(shape=img.shape)

    # Aplica o processo de convolução!
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            new_img[i][j] =  (kernel * padding_img[i:i + kernel_size, j:j + kernel_size]).sum()

    return new_img

def median_filter(img, kernel_size):

    print(img)

    padding_img = __zero_padding(img, kernel_size - 1)

    print(padding_img)

    new_img = np.zeros(shape=img.shape)

    # Calculando a mediana
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            aux = img[i:i + kernel_size, j:j + kernel_size]
            aux = aux.flatten()
            aux.sort()

            new_img[i][j] = np.median(aux)

    return new_img

if __name__ == '__main__':
    img_a = cv2.imread(path.join('src/images', 'c.jpg'), cv2.IMREAD_GRAYSCALE)
    
    img_a_sp = salt_and_peper_noise(img_a, 10)

    cv2.imwrite(path.join('src/output', f'teste1.png'), img_a_sp)

    a = median_filter(img_a_sp, 3)

    print(a)

    cv2.imwrite(path.join('src/output', f'teste2.png'), a)

    pass