import os
from ex5_s6 import ex5_s6

if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n-----------------Resultados---------------------\n')
    ex5_s6.run()
    print('\n--------------Fim de resultados-----------------\n')
    input('Pressione ENTER para finalizar...')
    os.system('cls' if os.name == 'nt' else 'clear')