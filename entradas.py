class Entradas(object):
    def __init__(self, console):
        self.__console = console
        self.quantum = 0
        self.trocaDeContexto = 0
        self.tituloDosProcessos = []
        self.dicionarioDeDicionariosDeProcessos = {}

    def processarArquivo(self):
        self.quantum = int(self.__console.obter().split(': ')[1])
        self.trocaDeContexto = int(self.__console.obter().split(': ')[1])
        self.__console.obter()  # Discartando linha
        self.tituloDosProcessos = self.__console.obter().upper().split(' ')
        listaDeEntradaNaMemoria = self.__console.obter().split(' ')
        self.__console.obter()  # Discartando linha
        self.__console.obter()  # Discartando linha
        listaDeTimeSlicesNecessarios = self.__console.obter().split(' ')
        for i in range(len(self.tituloDosProcessos)):
            tituloDoProcesso = self.tituloDosProcessos[i]
            entradaNaMemoria = int(listaDeEntradaNaMemoria[i])
            tempoNecessario = int(listaDeTimeSlicesNecessarios[i])
            self.dicionarioDeDicionariosDeProcessos[tituloDoProcesso] = {
                'entrada': entradaNaMemoria,
                'necessario': tempoNecessario
            }

    def processarManual(self):
        self.quantum = self.__console.obter(
            'Quanto vale o quantum?', tipo='int')
        self.trocaDeContexto = self.__console.obter(
            'Quanto vale a troca de contexto?', tipo='int')
        quantidadeDeProcessos = self.__console.obter(
            'Quantidade de processos', tipo='int')
        for i in range(quantidadeDeProcessos):
            tituloDoProcesso = self.__console.obter(
                f'Titulo do processo {i+1}').upper()
            self.tituloDosProcessos.append(tituloDoProcesso)
        for i in range(quantidadeDeProcessos):
            tituloDoProcesso = self.tituloDosProcessos[i]
            self.__console.linha(22)
            entradaNaMemoria = self.__console.obter(
                f'Em qual fatia de tempo "{tituloDoProcesso}" entra na memoria?', tipo='int')
            tempoNecessario = self.__console.obter(
                f'Quantas fatias de tempo "{tituloDoProcesso}" irá precisar?', tipo='int', n=0)
            self.__console.linha(22)
            self.__console.quebraDeLinha(2)
            self.dicionarioDeDicionariosDeProcessos[tituloDoProcesso] = {
                'entrada': entradaNaMemoria,
                'necessario': tempoNecessario
            }
