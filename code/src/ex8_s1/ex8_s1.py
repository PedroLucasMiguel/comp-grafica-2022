from math import sqrt

def calcdistance(s1, s2, type='de'):

    stops1 = False
    stops2 = False

    x1 = 0
    x2 = 0
    y1 = 0
    y2 = 0
    r = 0

    while not stops1:
        x1 = int(input('Digite a coordenada X do ponto 1 (partindo de 0): '))
        y1 = int(input('Digite a coordenada y do ponto 1 (partindo de 0): '))

        if s1['offsetX'] <= x1 <= (s1['sizeX']-1 + s1['offsetX']) and s1['offsetY'] <= y1 <= (s1['sizeY']-1 + s1['offsetY']):
            stops1 = True
            
        else:
            print('O ponto indicado não pertence a S1')

    while not stops2:
        x2 = int(input('Digite a coordenada X do ponto 2 (partindo de 0): '))
        y2 = int(input('Digite a coordenada y do ponto 2 (partindo de 0): '))

        if  s2['offsetX'] <= x2 <= (s2['sizeX']-1 + s2['offsetX']) and s2['offsetY'] <= y2 <= (s2['sizeY']-1 + s2['offsetY']):
            stops2 = True

        else:
            print('O ponto indicado não pertence a S2')

    if type == 'de':
        r = sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))

    elif type == 'd4':
        r = abs(x1 - x2) + abs(y1 - y2)

    elif type == 'd8':
        r = max(abs(x1 - x2), abs(y1 - y2))

    print(f'\nResultado: {type} = {r}')