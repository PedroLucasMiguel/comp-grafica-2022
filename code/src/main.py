import os
from ex1_s10 import ex1_s10
from ex2_s10 import ex2_s10

execute = {
    1 : ex1_s10.run, 
    2 : ex2_s10.run,
}

if __name__ == '__main__':
    stop = False
    i = 0
    
    os.system('cls' if os.name == 'nt' else 'clear')

    while not stop:
        print('\nResultados das atividades!\n')
        print('Escolha qual exercício deve ser executado:')
        print('[1] - Exercício 1')
        print('[2] - Exercício 2')
        print('[3] - Sair')

        i = int(input('Resposta: '))

        if ( i < 0 or i > 3):
            print('Valor inválido')

        if (i == 3):
            stop = True
        
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('\n-----------------Resultados---------------------\n')
            execute[i]()
            print('Imagens salvas em: output')
            print('\n--------------Fim de resultados-----------------\n')
            input('Pressione ENTER para continuar...')
            os.system('cls' if os.name == 'nt' else 'clear')