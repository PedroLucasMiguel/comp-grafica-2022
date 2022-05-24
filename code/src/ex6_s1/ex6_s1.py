'''
    Este módulo fornece métodos para verificar se shape1 e shape2 possuem grupos de pixels conexos.
    Assume-se que ambas as formas são retangulares e podem ser definidas em qualquer lugar em um espaço 2D.
    Para fins de otimização, também assume-se que as formas não se sobrepõem.
'''


def __is_inside(point, corner):
    '''
        Verifica se point está dentro da forma dada.
        Como foi estabelecido anteriormente que a forma é um quadrado,
        só é necessário verificar se o ponto está entre o
        canto superior esquerdo e inferior direito nos eixos x e y.
    '''
    x, y = point
    '''
        corner[0] => superior esquerdo
        corner[1] => inferior direito
    '''
    py1, px1 = corner[0]
    py2, px2 = corner[1]
    return x >= px1 and x < px2 and y >= py1 and y < py2


def __check_neighbours(points, shape):
    '''
        Verifica possíveis vizinhos em shape seguindo uma lista de pontos.
        Nestes pontos espera-se que os pontos tenham sido validados para estarem dentro da forma.
    '''
    for y, x in points:
        if shape["grid"][y - shape["offsetY"]][x - shape["offsetX"]]:
            return True
    return False


def __check_neighbours_4(point, shape, orientation):
    '''
        Cria uma lista de possíveis vizinhos a serem verificados.
        Aqui é aplicada uma estratégia de otimização de apenas checar
        para possíveis coordenadas que podem estar fora da forma de referência.
        Em vizinhança-4 só pode haver 1 possibilidade.

        A orientação não é usada neste caso, mas o parâmetro
        é mantido para manter a simetria entre as duas funções.

        TODO: move __is_inside in here to keep symetry.
    '''
    return __check_neighbours([point], shape)


def __check_neighbours_8(point, shape, orientation):
    '''
        Cria uma lista de possíveis vizinhos a serem verificados.
        Aqui é aplicada uma estratégia de otimização de apenas checar
        para possíveis coordenadas que podem estar fora da forma de referência.
        Em vizinhança-8 existem 3 possibilidades.

        TODO: move __is_inside in here to be called for every point created.
    '''
    y, x = point
    points = []
    for i in range(-1, 2):
        '''
            orientation 0 é horizontal e 1 é vertical.
        '''
        if orientation:
            points.append((y, x + i))
        else:
            points.append((y + i, x))
    return __check_neighbours(points, shape)


def __check_connectivity(shape1, shape2, neighbourhood_fn):
    '''
        Como se assume que as formas são retangulares, é possível verificar
        conectividade verificando apenas as bordas das formas.
        Além disso, como é verificado apenas para vizinhança-4 e 8,
        então é desnecessário verificar as bordas de ambas as formas.
        Como tal, shape1 é tomada como a forma de referência.
        Para otimizar ainda mais essa verificação de conectividade,
        é utilizada uma estratégia de retorno rápido.
        O que significa que o código irá parar assim que o
        primeiro vizinho confirmado for encontrado.
    '''
    s2_corners = [
        (shape2["offsetX"], shape2["offsetY"]),
        (shape2["offsetX"] + shape2["sizeX"],
         shape2["offsetY"] + shape2["sizeY"])
    ]
    for i in range(len(shape1["grid"][0])):
        if shape1["grid"][0][i] and __is_inside((-1, i), s2_corners) and neighbourhood_fn((-1, i), shape2, 0):
            return True
    for i in range(len(shape1["grid"])):
        if shape1["grid"][i][len(shape1["grid"][0]) - 1] and __is_inside((i, len(shape1["grid"][0])), s2_corners) and neighbourhood_fn((i, len(shape1["grid"][0])), shape2, 1):
            return True
    for i in range(len(shape1["grid"][0])):
        if shape1["grid"][len(shape1["grid"]) - 1][i] and __is_inside((len(shape1["grid"]), i), s2_corners) and neighbourhood_fn((len(shape1["grid"]), i), shape2, 0):
            return True
    for i in range(len(shape1["grid"])):
        if shape1["grid"][i][0] and __is_inside((i, -1), s2_corners) and neighbourhood_fn((i, -1), shape2, 1):
            return True
    return False


def check_connectivity_4(shape1, shape2):
    '''
        Checa conectividade com vizinhança-4
    '''
    return __check_connectivity(shape1, shape2, __check_neighbours_4)


def check_connectivity_8(shape1, shape2):
    '''
        Checa conectividade com vizinhança-8
    '''
    return __check_connectivity(shape1, shape2, __check_neighbours_8)


'''
    Código utilizado para testes durante o desenvolvimento
'''
if __name__ == "__main__":
    s1, s2, s3, s4 = ({
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
    }, {
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
    }, {
        "grid": [
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 0, 1, 0],
            [1, 0, 0, 0]
        ],
        "sizeX": 4,
        "sizeY": 5,
        "offsetX": 6,
        "offsetY": 0
    }, {
        "grid": [
            [0, 0, 0, 0],
            [0, 0, 1, 0],
            [1, 1, 0, 1],
            [0, 0, 1, 0],
            [1, 0, 0, 0]
        ],
        "sizeX": 4,
        "sizeY": 5,
        "offsetX": 7,
        "offsetY": 0
    })
    print(check_connectivity_4(s1, s2))  # expect True
    print(check_connectivity_4(s1, s3))  # expect False
    print(check_connectivity_4(s1, s4))  # expect False
    print(check_connectivity_8(s1, s2))  # expect True
    print(check_connectivity_8(s1, s3))  # expect True
    print(check_connectivity_8(s1, s4))  # expect False
