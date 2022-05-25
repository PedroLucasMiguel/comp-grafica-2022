import numpy as np


'''
    Este módulo fornece métodos para contar quantos grupos
    de pixels existem em um espaço combinado de duas formas retangulares.
    Assume-se que as formas não estão sobrepostas.
'''


def __create_grid(shape1, shape2):
    '''
        Cria uma nova grade ou forma que seja a união das duas formas fornecidas.
        Para isso, primeiro é criada uma grade zerada com um tamanho que engloba
        ambas as formas e, em seguida, cada pixel de cada forma é verificado e copiado para esta grade.
        Essa estratégia leva em consideração que ambas as formas
        podem estarem qualquer lugar em um espaço 2D,
        não necessariamente em contato, mas não podem estar sobrepostos.
    '''
    output = np.zeros((
        shape1["sizeY"]
        + shape2["sizeY"]
        + (shape2["offsetY"] - (shape1["sizeY"] + shape1["offsetY"]) if shape1["offsetY"] <
           shape2["offsetY"] else shape1["offsetY"] - (shape2["sizeY"] + shape2["offsetY"])),
        shape1["sizeX"]
        + shape2["sizeX"]
        + (shape2["offsetX"] - (shape1["sizeX"] + shape1["offsetX"]) if shape1["offsetX"] <
           shape2["offsetX"] else shape1["offsetX"] - (shape2["sizeX"] + shape2["offsetX"]))))

    out_offsetX = min(shape1["offsetX"], shape2["offsetX"])
    out_offsetY = min(shape1["offsetY"], shape2["offsetY"])

    for j in range(shape1["offsetX"], shape1["offsetX"] + shape1["sizeX"]):
        for i in range(shape1["offsetY"], shape1["offsetY"] + shape1["sizeY"]):
            output[i - out_offsetY][j - out_offsetX] = shape1["grid"][i -
                                                                      shape1["offsetY"]][j - shape1["offsetX"]]
    for j in range(shape2["offsetX"], shape2["offsetX"] + shape2["sizeX"]):
        for i in range(shape2["offsetY"], shape2["offsetY"] + shape2["sizeY"]):
            output[i - out_offsetY][j - out_offsetX] = shape2["grid"][i -
                                                                      shape2["offsetY"]][j - shape2["offsetX"]]

    return output


def __check_neighbourhood_4(grid, i, j, value):
    '''
        Verifica todos os 4 vizinhos da célula atual recursivamente.
        Se houver um vizinho com valor 1, significa que ainda não foi verificado.
        Como tal, ele recebe o valor atual do ID do grupo e
        a recursão é chamada para cada um de seus vizinhos.
    '''
    if (grid[i][j] != 1):
        return False

    grid[i][j] = value
    for k in range(0, 2):
        x = i + 1 if k else i - 1
        y = j + 1 if k else j - 1
        if x < len(grid) and x > -1:
            __check_neighbourhood_4(grid, x, j, value)
        if y < len(grid[0]) and y > -1:
            __check_neighbourhood_4(grid, i, y, value)

    return True


def __check_neighbourhood_8(grid, i, j, value):
    '''
        Verifica todos os 8 vizinhos da célula atual recursivamente.
        Se houver um vizinho com valor 1, significa que ainda não foi verificado.
        Como tal, ele recebe o valor atual do ID do grupo e
        a recursão é chamada para cada um de seus vizinhos.
    '''
    if (grid[i][j] != 1):
        return False

    grid[i][j] = value
    for k in range(0, 2):
        for l in range(0, 2):
            x = i + 1 if k else i - 1
            y = j + 1 if l else j - 1
            if x < len(grid) and x > -1 and y < len(grid[0]) and y > -1:
                __check_neighbourhood_8(grid, x, y, value)
        x = i + 1 if k else i - 1
        y = j + 1 if k else j - 1
        if x < len(grid) and x > -1:
            __check_neighbourhood_8(grid, x, j, value)
        if y < len(grid[0]) and y > -1:
            __check_neighbourhood_8(grid, i, y, value)

    return True


def __count_connected(shape1, shape2, check_neighbourhood_fn):
    '''
        Crie uma grade combinada das duas formas e chame
        o check_neighbourhood_fn para cada pixel na grade.
        Os grupos são rotulados com o valor de n_groups e
        o resultado é encontrado subtraindo 1 de n_groups no final.
    '''
    n_groups = 1

    grid = __create_grid(shape1, shape2)

    for j in range(0, len(grid[0])):
        for i in range(0, len(grid)):
            n_groups += 1 if check_neighbourhood_fn(
                grid, i, j, pow(2, n_groups)) else 0

    return n_groups - 1


def count_connected_4(shape1, shape2):
    '''
        Conta quantos grupos de pixels na combinação do
        espaço das duas formas existem com vizinhança-4.
    '''
    return __count_connected(shape1, shape2, __check_neighbourhood_4)


def count_connected_8(shape1, shape2):
    '''
        Conta quantos grupos de pixels na combinação do
        espaço das duas formas existem com vizinhança-8.
    '''
    return __count_connected(shape1, shape2, __check_neighbourhood_8)

def run():
    s1 = {
        "grid": [
            [0, 1, 0, 0, 0, 1],
            [1, 0, 0, 1, 0, 0],
            [1, 0, 1, 1, 0, 1],
            [1, 0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0, 0]
        ],
        "sizeX": 6,
        "sizeY": 5,
        "offsetX": 0,
        "offsetY": 0
    }

    s2 = {
        "grid": [
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [1, 1, 0, 1],
            [0, 0, 1, 0],
            [1, 0, 0, 0]
        ],
        "sizeX": 4,
        "sizeY": 5,
        "offsetX": 6,
        "offsetY": 0
    }

    print(f'Conectividade 4: {count_connected_4(s1, s2)}')
    print(f'Conectividade 8: {count_connected_8(s1, s2)}')