from app.console import Console
from app.entrada import Entrada
from app.processo import Processo


CORES = {
    'pronto': '\033[1;42m',
    'executando': '\033[1;41m',
    'nao alocado': '\033[1;100m',
    'troca de contexto': '\033[1;43m'
}


class App(object):
    def __init__(self):
        self.dados_de_entrada = Entrada()

        self.fatias_usadas = 0
        self.fatias_executadas = 0
        self.total_de_fatias = 0

        self.processos = []
        self.fila_de_execucao = []

        self.acao = ''

    def run(self):
        self.dados_de_entrada.carregar()

        self.criar_lista_de_processos()
        self.verificar_fila_de_execucao()

        for fatia_de_tempo in range(self.total_de_fatias):
            self.executar()
            self.registrar_como_pronto()
            self.verificar_fila_de_execucao()

            quantum = self.dados_de_entrada.quantum
            remover_da_fila = self.acao == 'remover da fila de execucao'

            if remover_da_fila or self.fatias_usadas >= quantum:
                self.executar_acao()
                self.fatias_usadas = 0

        self.mostrar_resultados()
        self.mostrar_tabela()

    def executar(self):
        primeiro_da_fila = self.fila_de_execucao[0]
        primeiro_da_fila.run()

        if primeiro_da_fila.estado() == 'pronto':
            self.acao = 'mover para o fim da fila de execucao'
        elif primeiro_da_fila.estado() == 'finalizado':
            self.acao = 'remover da fila de execucao'
        else:
            return None

        self.fatias_usadas += 1
        self.fatias_executadas += 1

    def executar_acao(self):
        self.mostrar_execucao()

        primeiro_da_fila = self.fila_de_execucao[0]
        fazer_troca_de_contexto = False

        tamanho_da_fila = len(self.fila_de_execucao)
        if tamanho_da_fila > 1:
            fazer_troca_de_contexto = True
        if self.acao == 'mover para o fim da fila de execucao':
            self.fila_de_execucao.append(primeiro_da_fila)
            self.fila_de_execucao.pop(0)
        elif self.acao == 'remover da fila de execucao':
            self.fila_de_execucao.pop(0)
        else:
            return None

        if fazer_troca_de_contexto:
            primeiro_da_fila = self.fila_de_execucao[0]
            fatias_gastas_na_troca_de_contexto = self.dados_de_entrada.contexto

            for fatia in range(fatias_gastas_na_troca_de_contexto):
                self.fatias_executadas += 1
                primeiro_da_fila.registrar(estado='troca de contexto')

                self.registrar_como_pronto()
                self.verificar_fila_de_execucao()

    def verificar_fila_de_execucao(self):
        for processo in self.processos:
            iniciar_processo = self.fatias_executadas >= processo.inicio

            if processo.estado() == 'nao alocado' and iniciar_processo:
                processo.entrar_na_memoria()
                self.fila_de_execucao.append(processo)

    def registrar_como_pronto(self, inicio=1):
        for i in range(inicio, len(self.fila_de_execucao)):
            self.fila_de_execucao[i].registrar('pronto')

    def criar_lista_de_processos(self):
        for dados_do_processo in self.dados_de_entrada.processos:
            processo = Processo(dados_do_processo)

            self.total_de_fatias += processo.fatias
            self.processos.append(processo)

    def mostrar_execucao(self):
        def obter_espacos(valor):
            return (2 - len(f'{valor}')) * ' '

        Console.quebrar_linha(vezes=1)

        for i, processo in enumerate(self.fila_de_execucao):
            faltando = processo.fatias - processo.processado
            n = ' | '

            Console.mostrar(f'{i+1} -> {processo.nome}', n=n)

            espacos = obter_espacos(faltando)
            Console.mostrar(f'Faltando -> {espacos}{faltando}', n=n, t='')

            espacos = obter_espacos(processo.processado)
            Console.mostrar(
                f'Processado -> {espacos}{processo.processado}', n=n, t='')

            espacos = obter_espacos(processo.fatias)
            Console.mostrar(
                f'Necessario -> {espacos}{processo.fatias}', n=n, t='')

            estado = processo.estado()
            if i == 0 and estado != 'finalizado':
                estado = 'executou'

            Console.mostrar(f'Estado -> {estado}', t='')

    def mostrar_tabela(self):
        Console.quebrar_linha(2)

        n = '\033[0;0m'

        if self.fatias_executadas < 27:
            tamanho_da_fatia_em_tela = 3 * ' '
        elif self.fatias_executadas < 43:
            tamanho_da_fatia_em_tela = 2 * ' '
        else:
            tamanho_da_fatia_em_tela = 1 * ' '

        for processo in self.processos:
            Console.mostrar(f'{processo.nome} -> ', n=n, t='   ')

            for estado in processo.historico:
                representacao = f'{CORES[estado]}{tamanho_da_fatia_em_tela}'
                Console.mostrar(f'|{representacao}', n=n, t='')

            Console.quebrar_linha(2)

    def mostrar_resultados(self):
        media_de_espera = 0
        media_em_memoria = 0

        for processo in self.processos:
            fatias_gastas = len(processo.historico)
            fatias_gastas_em_memoria = fatias_gastas - processo.inicio
            fatias_em_espera = fatias_gastas_em_memoria - processo.fatias

            media_de_espera += fatias_em_espera
            media_em_memoria += fatias_gastas_em_memoria

            Console.quebrar_linha(2)
            Console.mostrar(f'Resultados do processo {processo.nome}')
            Console.adicionar_separador(13)
            Console.mostrar(f'Tempo de espera   -> {fatias_em_espera}')
            Console.mostrar(f'Tempo de execução -> {fatias_gastas_em_memoria}')
            Console.adicionar_separador(13)

        quantidade_de_processos = len(self.processos)
        media_de_espera /= quantidade_de_processos
        media_em_memoria /= quantidade_de_processos

        Console.quebrar_linha(2)
        Console.adicionar_separador(19)
        Console.mostrar(
            f'Tempo médio de espera   -> {media_de_espera :.2f} fatias')
        Console.mostrar(
            f'Tempo médio de execução -> {media_em_memoria :.2f} fatias')
        Console.adicionar_separador(19)
