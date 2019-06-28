from console import Console
from processo import Processo


class App(object):
  def __init__(self):
    self.console = Console()
    self.quantum = 0
    self.linhaDoTempo = 0
    self.fatiasUsadas = 0
    self.totalDeFatias = 0
    self.quantidadeDeProcessos = 0
    self.filaDeExecucao = []
    self.filaDeProcessos = []
    self.acao = ''
    self.cores = {'Executando': '\033[1;41m', 'Pronto': '\033[1;42m', 'Não alocado': '\033[1;100m'}

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
      self.console.quebraDeLinha(2)
      self.executarAcao()
    self.mostrarResultados()
    self.console.quebraDeLinha(3)
    self.mostrarTabela()
    self.console.quebraDeLinha(3)

  def verificarListaDeExecucao(self):
    for processo in self.filaDeProcessos:
      if processo.status() == 'Não Alocado' and self.linhaDoTempo >= processo.inicio:
        processo.entrarNaMemoria()
        self.filaDeExecucao.append(processo)

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

  def mostrarExecucao(self):
    for index, processo in enumerate(self.filaDeExecucao):
      faltando = processo.necessario - processo.processado
      self.console.mostrar(f'{index+1} -> {processo.titulo} | ', n='')
      self.console.mostrar(f'Necessario -> {processo.necessario} | ', n='', t='')
      self.console.mostrar(f'Processado -> {processo.processado} | ', n='', t='')
      self.console.mostrar(f'Faltando -> {faltando} | ', n='', t='')
      self.console.mostrar(f'Status -> {processo.status()}', t='')

  def mostrarTabela(self):
    if self.totalDeFatias < 15:
      tamanhoDaFatia = 5 * ' '
    elif self.totalDeFatias < 25:
      tamanhoDaFatia = 3 * ' '
    else:
      tamanhoDaFatia = 2 * ' '
    for processo in self.filaDeProcessos:
      self.console.mostrar(f'{processo.titulo} -> ', n='\033[0;0m')
      for estado in processo.historico:
        self.console.mostrar(f'|{self.cores[estado]}{tamanhoDaFatia}', n='\033[0;0m', t='')
      self.console.quebraDeLinha(2)

  def mostrarResultados(self):
    tempoMedioDeEspera = 0
    tempoMedioDeExecucao = 0
    for processo in self.filaDeProcessos:
      tempoDeExecucao = len(processo.historico) - processo.inicio
      tempoDeEspera = tempoDeExecucao - processo.necessario
      tempoMedioDeExecucao += tempoDeExecucao
      tempoMedioDeEspera += tempoDeEspera
      self.console.quebraDeLinha(2)
      self.console.mostrar(f'Resultados do processo {processo.titulo}')
      self.console.linha(13)
      self.console.mostrar(f'Tempo de espera   -> {tempoDeEspera}')
      self.console.mostrar(f'Tempo de execução -> {tempoDeExecucao}')
      self.console.linha(13)
    tempoMedioDeEspera /= len(self.filaDeProcessos)
    tempoMedioDeExecucao /= len(self.filaDeProcessos)
    self.console.quebraDeLinha(2)
    self.console.linha(19)
    self.console.mostrar(f'Tempo médio de espera   -> {tempoMedioDeEspera :.4} fatias')
    self.console.mostrar(f'Tempo médio de execução -> {tempoMedioDeExecucao :.4} fatias')
    self.console.linha(19)


if __name__ == '__main__':
  App().run()
