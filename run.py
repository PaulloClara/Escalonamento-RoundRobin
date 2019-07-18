# Paulo Ricardo
# Josivan Cardoso

from console import Console
from processo import Processo
from entradas import Entradas


class App(object):
  def __init__(self):
    self.console = Console()
    self.entradas = Entradas(self.console)
    self.linhaDoTempo = 0
    self.fatiasUsadas = 0
    self.totalDeFatias = 0
    self.filaDeExecucao = []
    self.listaDeProcessos = []
    self.acao = ''
    self.cores = {
      'Executando': '\033[1;41m',
      'Pronto': '\033[1;42m',
      'Não alocado': '\033[1;100m',
      'Troca de Contexto': '\033[1;43m'
    }

  def run(self):
    if ('arquivo' in self.console.obter()):
      self.entradas.processarArquivo()
    else:
      self.entradas.processarManual()
    self.criarListaDeProcessos()
    self.verificarListaDeExecucao()
    for fatia in range(self.totalDeFatias):
      self.calcularAcao()
      self.registrarVolta()
      self.verificarListaDeExecucao()
      if self.fatiasUsadas != self.entradas.quantum:
        continue
      self.fatiasUsadas = 0
      self.console.quebraDeLinha(2)
      self.executarAcao()
    self.mostrarResultados()
    self.console.quebraDeLinha(3)
    self.mostrarTabela()
    self.console.quebraDeLinha(3)

  def verificarListaDeExecucao(self):
    for processo in self.listaDeProcessos:
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
      self.fatiasUsadas = self.entradas.quantum
    self.linhaDoTempo += 1

  def executarAcao(self):
    self.mostrarExecucao()
    test = False
    if len(self.filaDeExecucao) > 1:
      test = True
    if self.acao == 'Mover para o fim da fila':
      self.filaDeExecucao.append(self.filaDeExecucao[0])
      self.filaDeExecucao.pop(0)
    else:
      self.filaDeExecucao.pop(0)
    if test:
      for i in range(self.entradas.trocaDeContexto):
        self.filaDeExecucao[0].registrar('Troca de Contexto')
        self.registrarVolta()
    self.linhaDoTempo += self.entradas.trocaDeContexto

  def registrarVolta(self, estado='Pronto'):
    for index in range(1, len(self.filaDeExecucao)):
      self.filaDeExecucao[index].registrar(estado)

  # Inits
  def criarListaDeProcessos(self):
    for tituloDoProcesso in self.entradas.tituloDosProcessos:
      processo = self.entradas.dicionarioDeDicionariosDeProcessos[tituloDoProcesso]
      objetoProcesso = Processo(tituloDoProcesso, processo['entrada'], processo['necessario'])
      self.totalDeFatias += objetoProcesso.necessario
      self.listaDeProcessos.append(objetoProcesso)

  def mostrarExecucao(self):
    for index, processo in enumerate(self.filaDeExecucao):
      faltando = processo.necessario - processo.processado
      self.console.mostrar(f'{index+1} -> {processo.titulo} | ', n='')
      self.console.mostrar(f'Necessario -> {processo.necessario} | ', n='', t='')
      self.console.mostrar(f'Processado -> {processo.processado} | ', n='', t='')
      self.console.mostrar(f'Faltando -> {faltando} | ', n='', t='')
      self.console.mostrar(f'Status -> {processo.status()}', t='')

  def mostrarTabela(self):
    if self.linhaDoTempo < 27:
      tamanhoDaFatia = 3 * ' '
    elif self.linhaDoTempo < 43:
      tamanhoDaFatia = 2 * ' '
    else:
      tamanhoDaFatia = 1 * ' '
    for processo in self.listaDeProcessos:
      self.console.mostrar(f'{processo.titulo} -> ', n='\033[0;0m', t='   ')
      for estado in processo.historico:
        self.console.mostrar(f'|{self.cores[estado]}{tamanhoDaFatia}', n='\033[0;0m', t='')
      self.console.quebraDeLinha(2)

  def mostrarResultados(self):
    tempoMedioDeEspera = 0
    tempoMedioDeExecucao = 0
    for processo in self.listaDeProcessos:
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
    tempoMedioDeEspera /= len(self.listaDeProcessos)
    tempoMedioDeExecucao /= len(self.listaDeProcessos)
    self.console.quebraDeLinha(2)
    self.console.linha(19)
    self.console.mostrar(f'Tempo médio de espera   -> {tempoMedioDeEspera :.4} fatias')
    self.console.mostrar(f'Tempo médio de execução -> {tempoMedioDeExecucao :.4} fatias')
    self.console.linha(19)


if __name__ == '__main__':
  App().run()
