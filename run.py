from processo import Processo


class App(object):
  def __init__(self):
    self.quantum = 0
    self.fatiasUsadas = 0
    self.totalDeFatias = 0
    self.filaDeProcessos = []
    self.filaDeExecucao = []
    self.linhaDoTempo = 0
    self.acao = ''

  def run(self):
    self.obterQuantum()
    self.criarListaDeProcessos()
    self.verificarListaDeExecucao()
    for fatia in range(self.totalDeFatias):
      self.calcularAcao()
      self.registrarVolta()
      self.verificarListaDeExecucao()
      if self.fatiasUsadas != self.quantum:
        continue
      self.fatiasUsadas = 0
      self.executarAcao()

    self.mostrarGrafico()

  def verificarListaDeExecucao(self):
    for index in range(len(self.filaDeProcessos)):
      processo = self.filaDeProcessos[index]
      if processo.status() == 'Não Alocado' and processo.obterInicio() <= self.linhaDoTempo:
        processo.entrarNaMemoria()
        self.filaDeExecucao.append(processo)
        self.filaDeProcessos[index] = processo

  def calcularAcao(self):
    self.filaDeExecucao[0].run()
    if self.filaDeExecucao[0].status() == 'Pronto':
      self.acao = 'Mover para o fim da fila'
      self.fatiasUsadas += 1
    else:
      self.acao = 'Remover da fila'
      self.fatiasUsadas = self.quantum
    self.linhaDoTempo += 1

  def executarAcao(self):
    self.mostrarExecucao()
    if self.acao == 'Mover para o fim da fila':
      self.filaDeExecucao.append(self.filaDeExecucao[0])
      self.filaDeExecucao.pop(0)
    else:
      self.filaDeExecucao.pop(0)

  def registrarVolta(self):
    for index in range(1, len(self.filaDeExecucao)):
      self.filaDeExecucao[index].registrar('Pronto')

  def criarListaDeProcessos(self):
    print('\n\n\t=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    numeroDeProcessos = int(input('\tNumero de processos\n\t> '))
    print('\n\t=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    for i in range(numeroDeProcessos):
      self.filaDeProcessos.append(Processo())
      self.filaDeProcessos[-1].init()
      self.totalDeFatias += self.filaDeProcessos[-1].obterTempoNecessario()

  def obterQuantum(self):
    print('\n\n\t=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')
    self.quantum = int(input('\tQuanto vale o Quantum?\n\t> '))
    print('\n\t=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=')

  def mostrarExecucao(self):
    print('\n')
    for index, processo in enumerate(self.filaDeExecucao):
      faltando = processo.obterTempoNecessario() - processo.obterProcessado()
      print(f'\t{index+1} -> {processo.obterTitulo()} | ', end='')
      print(f'Necessario -> {processo.obterTempoNecessario()} | ', end='')
      print(f'Processado -> {processo.obterProcessado()} | ', end='')
      print(f'Faltando -> {faltando} | ', end='')
      print(f'Status -> {processo.status()}')

  def mostrarGrafico(self):
    for processo in self.filaDeProcessos:
      print('')
      print(processo.obterTitulo())
      print(processo.obterHistorico())


if __name__ == '__main__':
  App().run()
