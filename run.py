from processo import Processo


class App(object):
  def __init__(self):
    self.quantum = 0
    self.filaDeProcessos = []
    self.filaDeExecucao = []
    self.linhaDoTempo = 0
    self.acao = ''

  def run(self):
    self.quantum = int(input('\n\tQuanto vale o Quantum?\n> '))
    self.criarListaDeProcessos()
    self.verificarListaDeExecucao()
    while len(self.filaDeExecucao):
      self.calcularAcao()
      self.verificarListaDeExecucao()
      self.executarAcao()

  def calcularAcao(self):
    resto = self.filaDeExecucao[0].run(self.quantum)
    if self.filaDeExecucao[0].status() == 'Pronto':
      self.acao = 'Mover para o fim da fila'
    else:
      self.acao = 'Remover da fila'
    self.linhaDoTempo += self.quantum - resto

  def executarAcao(self):
    for processo in self.filaDeExecucao:
      print(f'{processo.obterTitulo()} {processo.status()} {processo.obterProcessado()}')
    print('')
    if self.acao == 'Mover para o fim da fila':
      self.filaDeExecucao.append(self.filaDeExecucao[0])
      self.filaDeExecucao.pop(0)
    else:
      self.filaDeExecucao.pop(0)

  def verificarListaDeExecucao(self):
    for index in range(len(self.filaDeProcessos)):
      processo = self.filaDeProcessos[index]
      if processo.status() == 'Não Alocado' and processo.obterInicio() <= self.linhaDoTempo:
        processo.entrarNaMemoria()
        self.filaDeExecucao.append(processo)
        self.filaDeProcessos[index] = processo

  def criarListaDeProcessos(self):
    for i in range(int(input('\n\tNumero de processos\n> '))):
      print('\n\n')
      self.filaDeProcessos.append(Processo())
      self.filaDeProcessos[-1].init()



if __name__ == '__main__':
  App().run()
