from math import sqrt

from numpy import AxisError

def calcdistance(s1, s2, type='de'):

    stops1 = False
    stops2 = False

    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    r = 0

    while not stops1:
        y1 = int(input('Digite a coordenada da linha do ponto 1 (partindo de '  + str(s1['offsetY']) + '): '))
        x1 = int(input('Digite a coordenada da coluna do ponto 1 (partindo de ' + str(s1['offsetX']) + '): '))

        # Verifica se os valores inseridos estão dentro de S1
        if s1['offsetX'] <= x1 <= (s1['sizeX']-1 + s1['offsetX']) and s1['offsetY'] <= y1 <= (s1['sizeY']-1 + s1['offsetY']):
            if s1['grid'][y1 - s1['offsetX']][x1 - s1['offsetY']] == 1:
                stops1 = True
            else:
                print('\nERRO: O numero escolhido deve ser igual a 1 \n')
        else:
            print('\nERRO: O ponto indicado não pertence a S1 \n')

    while not stops2:
        y2 = int(input('Digite a coordenada da linha do ponto 2 (partindo de '  + str(s2['offsetY']) + '): '))
        x2 = int(input('Digite a coordenada da coluna do ponto 2 (partindo de ' + str(s2['offsetX']) + '): '))
        
        # Verifica se os valores inseridos estão dentro de S2
        if  s2['offsetX'] <= x2 <= (s2['sizeX']-1 + s2['offsetX']) and s2['offsetY'] <= y2 <= (s2['sizeY']-1 + s2['offsetY']):
            if s2['grid'][y2 - s2['offsetY']][x2 - s2['offsetX']] == 1:
                stops2 = True
            else:
                print(f'\nERRO: O numero escolhido deve ser igual a 1 ' + str(s2['grid'][x2 - s2['offsetX']][y2 - s2['offsetY']+1]))
        else:
            print('O ponto indicado não pertence a S2')

    # Realiza o cálculo da distância
    if type == 'de':
        r = sqrt(pow((x1 - x2), 2) + pow((y1 - y2), 2))

    elif type == 'd4':
        r = abs(x1 - x2) + abs(y1 - y2)

    elif type == 'd8':
        r = max(abs(x1 - x2), abs(y1 - y2))

    print(f'\nResultado: {type} = {r}\n')

if __name__ == '__main__':

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

    q = False
    i = 0

    while not q:
        print('Escolha uma opcao:')
        print('[0] - DE')
        print('[1] - D4')
        print('[2] - D8')
        print('[3] - Sair')
        i = int(input('Resposta: '))

        if i < 0 or i > 3:
            print('Opcao invalida\n')
        
        else:
            if i == 0:
                calcdistance(s1, s2, 'de')

            elif i == 1:
                calcdistance(s1, s2, 'd4')
            
            elif i == 2:
                calcdistance(s1, s2, 'd8')
            
            elif i == 3:
                q = True
        
