import random
import numpy as np
import cv2
from math import sqrt
from os import path

# Code from: https://www.geeksforgeeks.org/add-a-salt-and-pepper-noise-to-an-image-with-python/#:~:text=Salt%2Dand%2Dpepper%20noise%20is,%2C%20bit%20transmission%20error%2C%20etc.&text=Below%20is%20the%20implementation%3A,Python
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

def gausian_noise(o_img):
    row, col = o_img.shape

    colors = []

    for i in range(100, 201, 10):
        colors.append(i)

    for i in range(row):
        for j in range(col):
            for c in range(len(colors)):
                if np.random.normal() <= 0.01:
                    o_img[i][j] = colors[c]
                    break
    
    return o_img

# ------------------------------------------------------------------------------------------

def max_error(i1, i2):

    if (i1.shape != i2.shape):
        print("Tamanhos de imagens diferentes!")
    
    else:
        v = []
        row, col = i1.shape

        print(row, col)

        for i in range(row):
            for j in range(col):
                v.append(abs(int(i1[i][j]) - int(i2[i][j])))
    

        return max(v)

def mean_absolute_error(i1, i2):

    if (i1.shape != i2.shape):
        print("Tamanhos de imagens diferentes!")
    
    else:
        v = []
        row, col = i1.shape

        print(row, col)

        for i in range(row):
            for j in range(col):
                v.append(abs(int(i1[i][j]) - int(i2[i][j])))
        
        v = sum(v)

        return v/(row * col)


def mean_square_error(i1, i2):

    if (i1.shape != i2.shape):
        print("Tamanhos de imagens diferentes!")
    
    else:
        v = []
        row, col = i1.shape

        print(row, col)

        for i in range(row):
            for j in range(col):
                v.append(pow(int(i1[i][j]) - int(i2[i][j]), 2))
        
        v = sum(v)

        return v/(row * col)

def root_mean_square_error(i1, i2):

    if (i1.shape != i2.shape):
        print("Tamanhos de imagens diferentes!")
    
    else:
        v = []
        row, col = i1.shape

        print(row, col)

        for i in range(row):
            for j in range(col):
                v.append(pow(int(i1[i][j]) - int(i2[i][j]), 2))
        
        v = sum(v)

        return sqrt(v/(row * col))

def jaccard(i1, i2):

    if (i1.shape != i2.shape):
        print("Tamanhos de imagens diferentes!")
    
    else:
        v = []
        row, col = i1.shape

        print(row, col)

        for i in range(row):
            for j in range(col):
                if int(i1[i][j]) - int(i2[i][j]) <= 25.5:
                    v.append(1)
                else:
                    v.append(0)
        
        v = sum(v)

        return v/(row * col)


def apply_noises():
    img_a = cv2.imread(path.join('code/src/images', 'a.jpg'), cv2.IMREAD_GRAYSCALE)
    img_b = cv2.imread(path.join('code/src/images', 'b.jpg'), cv2.IMREAD_GRAYSCALE)
    img_c = cv2.imread(path.join('code/src/images', 'c.jpg'), cv2.IMREAD_GRAYSCALE)

    # Salt and peper
    cv2.imwrite(path.join('code/src/output', 'a_sp.jpg'), salt_and_peper_noise(img_a))
    cv2.imwrite(path.join('code/src/output', 'b_sp.jpg'), salt_and_peper_noise(img_b))
    cv2.imwrite(path.join('code/src/output', 'c_sp.jpg'), salt_and_peper_noise(img_c))

    # Uniform
    cv2.imwrite(path.join('code/src/output', 'a_u.jpg'), uniform_noise(img_a))
    cv2.imwrite(path.join('code/src/output', 'b_u.jpg'), uniform_noise(img_b))
    cv2.imwrite(path.join('code/src/output', 'c_u.jpg'), uniform_noise(img_c))

    # Gaussian
    cv2.imwrite(path.join('code/src/output', 'a_g.jpg'), gausian_noise(img_a))
    cv2.imwrite(path.join('code/src/output', 'b_g.jpg'), gausian_noise(img_b))
    cv2.imwrite(path.join('code/src/output', 'c_g.jpg'), gausian_noise(img_c))


def calcerrors():
    img_a = cv2.imread(path.join('code/src/images', 'a.jpg'), cv2.IMREAD_GRAYSCALE)
    #img_b = cv2.imread(path.join('code/src/images', 'b.jpg'), cv2.IMREAD_GRAYSCALE)
    #img_c = cv2.imread(path.join('code/src/images', 'c.jpg'), cv2.IMREAD_GRAYSCALE)
    img_teste = cv2.imread(path.join('code/src/images', 'teste.jpg'), cv2.IMREAD_GRAYSCALE)

    # Salte and peper
    img_a_sp = cv2.imread(path.join('code/src/output', 'a_sp.jpg'), cv2.IMREAD_GRAYSCALE)
    #img_b_sp = cv2.imread(path.join('code/src/output', 'b_sp.jpg'), cv2.IMREAD_GRAYSCALE)
    #img_c_sp = cv2.imread(path.join('code/src/output', 'c_sp.jpg'), cv2.IMREAD_GRAYSCALE)
    img_teste_sp = cv2.imread(path.join('code/src/output', 'teste_sp.jpg'), cv2.IMREAD_GRAYSCALE)

    # Uniform
    img_a_u = cv2.imread(path.join('code/src/output', 'a_u.jpg'), cv2.IMREAD_GRAYSCALE)
    #img_b_u = cv2.imread(path.join('code/src/output', 'b_u.jpg'), cv2.IMREAD_GRAYSCALE)
    #img_c_u = cv2.imread(path.join('code/src/output', 'c_u.jpg'), cv2.IMREAD_GRAYSCALE)

    img_a_g = cv2.imread(path.join('code/src/output', 'a_g.jpg'), cv2.IMREAD_GRAYSCALE)
    #img_b_g = cv2.imread(path.join('code/src/output', 'b_g.jpg'), cv2.IMREAD_GRAYSCALE)
    #img_c_g = cv2.imread(path.join('code/src/output', 'c_g.jpg'), cv2.IMREAD_GRAYSCALE)
    img_teste_g = cv2.imread(path.join('code/src/output', 'teste_g.jpg'), cv2.IMREAD_GRAYSCALE)

    print(jaccard(img_teste, img_teste_g))