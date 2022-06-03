import os
from ex4_s4 import ex4_s4
from ex4_s5 import ex4_s5
from ex5_s5 import ex5_s5

execute = {
    1 : ex4_s4.run, 
    2 : ex4_s5.run,
    3 : ex5_s5.run,
}

if __name__ == '__main__':
    stop = False
    i = 0
    
    os.system('cls' if os.name == 'nt' else 'clear')

    while not stop:
        print('\nResultados das atividades!\n')
        print('Escolha qual exercício deve ser executado:')
        print('[1] - Exercício 4 (Slide 4)')
        print('[2] - Exercício 4 (Slide 5)')
        print('[3] - Exercício 5 (Slide 5)')
        print('[4] - Sair')

        i = int(input('Resposta: '))

        if ( i < 0 or i > 4):
            print('Valor inválido')

        if (i == 4):
            stop = True
        
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('\n-----------------Resultados---------------------\n')
            execute[i]()
            print('\n--------------Fim de resultados-----------------\n')
            input('Pressione ENTER para continuar...')
            os.system('cls' if os.name == 'nt' else 'clear')