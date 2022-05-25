import os
from ex5_s1 import ex5_s1
from ex6_s1 import ex6_s1
from ex7_s1 import ex7_s1
from ex8_s1 import ex8_s1
from ex3_s2 import ex3_s2

execute = {
    1 : ex5_s1.run, 
    2 : ex6_s1.run,
    3 : ex7_s1.run,
    4 : ex8_s1.run,
    5 : ex3_s2.run,
}

if __name__ == '__main__':
    stop = False
    i = 0
    
    os.system('cls' if os.name == 'nt' else 'clear')

    while not stop:
        print('\nResultados das atividades!\n')
        print('Escolha qual exercício deve ser executado:')
        print('[1] - Exercício 5 (Slide 1)')
        print('[2] - Exercício 6 (Slide 1)')
        print('[3] - Exercício 7 (Slide 1)')
        print('[4] - Exercício 8 (Slide 1)')
        print('[5] - Exercício 3 (Slide 2)')
        print('[6] - Sair')

        i = int(input('Resposta: '))

        if ( i < 0 or i > 6):
            print('Valor inválido')

        if (i == 6):
            stop = True
        
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print('\n-----------------Resultados---------------------\n')
            execute[i]()
            print('\n--------------Fim de resultados-----------------\n')
            input('Pressione ENTER para continuar...')
            os.system('cls' if os.name == 'nt' else 'clear')