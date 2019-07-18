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
    self.fatiasDeTempoUsadas = 0
    self.totalDeFatiasDeTempoNecessarias = 0
    self.filaDeExecucao = []
    self.listaDeProcessos = []
    self.acao = ''

  def run(self):
    tipoDeEntrada = self.console.obter()
    if ('arquivo' in tipoDeEntrada):
      self.entradas.processarArquivo()
    else:
      self.entradas.processarManual()
    self.criarListaDeProcessos()
    self.verificarFilaDeExecucao()
    for fatiaDeTempo in range(self.totalDeFatiasDeTempoNecessarias):
      self.executar()
      self.registrar()
      self.verificarFilaDeExecucao()
      fatiasDeTempoEsgotadas = self.fatiasDeTempoUsadas >= self.entradas.quantum
      if self.acao == 'remover da fila de execucao' or fatiasDeTempoEsgotadas:
        self.executarAcao()
        self.fatiasDeTempoUsadas = 0
    self.mostrarResultados()
    self.mostrarTabela()

  def executar(self):
    primeiroDaFila = self.filaDeExecucao[0]
    primeiroDaFila.run()
    if primeiroDaFila.status() == 'pronto':
      self.acao = 'mover para o fim da fila de execucao'
    elif primeiroDaFila.status() == 'finalizado':
      self.acao = 'remover da fila de execucao'
    else:
      return
    self.linhaDoTempo += 1
    self.fatiasDeTempoUsadas += 1

  def executarAcao(self):
    self.mostrarExecucao()
    primeiroDaFila = self.filaDeExecucao[0]
    fazerTrocaDeContexto = False
    tamanhoDaFilaDeExecucao = len(self.filaDeExecucao)
    if tamanhoDaFilaDeExecucao > 1:
      fazerTrocaDeContexto = True
    if self.acao == 'mover para o fim da fila de execucao':
      self.filaDeExecucao.append(primeiroDaFila)
      self.filaDeExecucao.pop(0)
    elif self.acao == 'remover da fila de execucao':
      self.filaDeExecucao.pop(0)
    else:
      return
    if fazerTrocaDeContexto:
      primeiroDaFila = self.filaDeExecucao[0]
      quantidadeDeFatiasGastasNaTrocaDeContexto = self.entradas.trocaDeContexto
      for fatia in range(quantidadeDeFatiasGastasNaTrocaDeContexto):
        primeiroDaFila.registrar('troca de contexto')
        self.registrar()
      self.linhaDoTempo += quantidadeDeFatiasGastasNaTrocaDeContexto

  def verificarFilaDeExecucao(self):
    for processo in self.listaDeProcessos:
      if processo.status() == 'nao alocado' and self.linhaDoTempo >= processo.inicio:
        processo.entrarNaMemoria()
        self.filaDeExecucao.append(processo)

  def registrar(self, estado='pronto'):
    for i in range(1, len(self.filaDeExecucao)):
      self.filaDeExecucao[i].registrar(estado)

  def criarListaDeProcessos(self):
    for tituloDoProcesso in self.entradas.tituloDosProcessos:
      processo = self.entradas.dicionarioDeDicionariosDeProcessos[tituloDoProcesso]
      objetoProcesso = Processo(tituloDoProcesso, processo['entrada'], processo['necessario'])
      self.totalDeFatiasDeTempoNecessarias += objetoProcesso.necessario
      self.listaDeProcessos.append(objetoProcesso)

  def mostrarExecucao(self):
    self.console.quebraDeLinha(1)
    for i, processo in enumerate(self.filaDeExecucao):
      fatiasDeTempoFaltando = processo.necessario - processo.processado
      self.console.mostrar(f'{i+1} -> {processo.titulo}', n=' | ')
      self.console.mostrar(f'Faltando -> {fatiasDeTempoFaltando}', n=' | ', t='')
      self.console.mostrar(f'Processado -> {processo.processado}', n=' | ', t='')
      self.console.mostrar(f'Necessario -> {processo.necessario}', n=' | ', t='')
      status = processo.status()
      if i == 0 and status != 'finalizado':
        status = 'executou'
      self.console.mostrar(f'Status -> {status}', t='')

  def mostrarTabela(self):
    self.console.quebraDeLinha(2)
    cores = {
      'executando': '\033[1;41m',
      'pronto': '\033[1;42m',
      'nao alocado': '\033[1;100m',
      'troca de contexto': '\033[1;43m'
    }
    if self.linhaDoTempo < 27:
      tamanhoDaFatia = 3 * ' '
    elif self.linhaDoTempo < 43:
      tamanhoDaFatia = 2 * ' '
    else:
      tamanhoDaFatia = 1 * ' '
    for processo in self.listaDeProcessos:
      self.console.mostrar(f'{processo.titulo} -> ', n='\033[0;0m', t='   ')
      for estado in processo.historico:
        self.console.mostrar(f'|{cores[estado]}{tamanhoDaFatia}', n='\033[0;0m', t='')
      self.console.quebraDeLinha(2)

  def mostrarResultados(self):
    tempoMedioDeEspera = 0
    tempoMedioDeExecucao = 0
    for processo in self.listaDeProcessos:
      totalDeFatiasDeTempoUsadasParaFinalizar = len(processo.historico)
      tempoDeExecucao = totalDeFatiasDeTempoUsadasParaFinalizar - processo.inicio
      tempoDeEspera = tempoDeExecucao - processo.necessario
      tempoMedioDeExecucao += tempoDeExecucao
      tempoMedioDeEspera += tempoDeEspera
      self.console.quebraDeLinha(2)
      self.console.mostrar(f'Resultados do processo {processo.titulo}')
      self.console.linha(13)
      self.console.mostrar(f'Tempo de espera   -> {tempoDeEspera}')
      self.console.mostrar(f'Tempo de execução -> {tempoDeExecucao}')
      self.console.linha(13)
    quantidadeDeProcessos = len(self.listaDeProcessos)
    tempoMedioDeEspera /= quantidadeDeProcessos
    tempoMedioDeExecucao /= quantidadeDeProcessos
    self.console.quebraDeLinha(2)
    self.console.linha(19)
    self.console.mostrar(f'Tempo médio de espera   -> {tempoMedioDeEspera :.4} fatias')
    self.console.mostrar(f'Tempo médio de execução -> {tempoMedioDeExecucao :.4} fatias')
    self.console.linha(19)


if __name__ == '__main__':
  App().run()
