class Console(object):
    @staticmethod
    def obter(mensagem='', linhas=1):
        valor = ''

        while not valor:
            if mensagem:
                valor = input(f'\t{mensagem}\n\t> ')

                if linhas:
                    Console.quebrar_linha(vezes=linhas)
            else:
                valor = input()

        return valor.lower()

    @staticmethod
    def mostrar(mensagem, n='\n', t='\t'):
        print(f'{t}{mensagem}', end=n)

    @staticmethod
    def adicionar_separador(tamanho):
        print(f'\t{"=-" * tamanho}=')

    @staticmethod
    def quebrar_linha(vezes=1):
        print('\n' * vezes, end='')
