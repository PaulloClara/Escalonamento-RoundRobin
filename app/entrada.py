from sys import argv as argumentos
from json import load as carregar_json

from app.console import Console


class Entrada(object):
    def __init__(self):
        self.quantum = 0
        self.contexto = 0
        self.processos = []

    def carregar(self):
        def obter_caminho_do_arquivo():
            for i, arg in enumerate(argumentos):
                if arg == '--arquivo':
                    return argumentos[i + 1]

            return None

        arquivo = obter_caminho_do_arquivo()
        if arquivo:
            self.carregar_via_arquivo(caminho_do_arquivo=arquivo)
        else:
            self.carregar_via_console()

    def carregar_via_arquivo(self, caminho_do_arquivo):
        with open(caminho_do_arquivo, mode='r') as arquivo:
            entradas = carregar_json(arquivo)

        self.quantum = entradas['quantum']
        self.contexto = entradas['contexto']

        self.processos = entradas['processos']

    def carregar_via_console(self):
        Console.quebrar_linha(vezes=1)

        self.quantum = int(Console.obter('De quanto é o quantum ?'))
        self.contexto = int(Console.obter(
            'Qual o custo da troca de contexto ?'))

        quantidade_de_processos = int(
            Console.obter('Qual a quantidade de processos ?'))

        for i in range(quantidade_de_processos):
            Console.adicionar_separador(tamanho=22)

            nome = Console.obter(
                f'Qual o nome do processo {i + 1} ?').upper()
            inicio = int(Console.obter(
                f'Em que fatia de tempo "{nome}" entra na memoria ?'))
            fatias = int(Console.obter(
                f'Quantas fatias de tempo "{nome}" irá precisar ?',
                linhas=0))

            Console.adicionar_separador(tamanho=22)
            Console.quebrar_linha(vezes=2)

            self.processos.append({
                'nome': nome,
                'inicio': inicio,
                'fatias': fatias
            })
