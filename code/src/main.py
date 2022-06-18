import os
from ex2_a7 import ex2_a7


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    ex2_a7.run()
    print('\n-----------------Resultados escritos na pasta images---------------------\n')
    input('Pressione ENTER para finalizar...')
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    main()
