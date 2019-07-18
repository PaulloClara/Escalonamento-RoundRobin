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
    self.__console.obter() # Discartando linha
    self.tituloDosProcessos = self.__console.obter().upper().split(' ')
    listaDeEntradaNaMemoria = self.__console.obter().split(' ')
    self.__console.obter() # Discartando linha
    self.__console.obter() # Discartando linha
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
    """
      def criarListaDeProcessos(self):
        self.console.linha(21)
        self.quantidadeDeProcessos = self.console.obter('Numero de processos', tipo='int')
        self.console.linha(21)
        for index in range(self.quantidadeDeProcessos):
          self.console.quebraDeLinha(3)
          self.console.linha(21)
          titulo = self.console.obter(f'Titulo do Processo {index}')
          processo = Processo()
          processo.init(titulo)
          self.totalDeFatias += processo.necessario
          self.filaDeProcessos.append(processo)

      def obterQuantum(self):
        self.console.linha(21)
        self.quantum = self.console.obter('Quanto vale o Quantum?', tipo='int')
        self.console.linha(21)



            self.__console.linha(21)
            self.titulo = titulo
            self.inicio = self.__console.obter('Em qual tempo ele ira entrar na memoria?', tipo='int')
            self.necessario = self.__console.obter('Tempo necessario', tipo='int')
            self.__console.linha(21)
            for fatia in range(self.inicio):
              self.registrar('Não alocado')

    """
