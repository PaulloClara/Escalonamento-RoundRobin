from console import Console


class Processo(object):
  def __init__(self):
    self.__console = Console()
    self.__titulo = ''
    self.__inicio = 0
    self.__necessario = 0
    self.__processado = 0
    self.__ativo = False
    self.__finalizado = False
    self.__historico = []

  def status(self):
    msg = 'Pronto'
    if self.__necessario - self.__processado <= 0:
      self.__finalizado = True
      msg = 'Finalizado'
    if not self.__ativo:
      msg = 'Não Alocado'
    return msg

  def run(self):
    self.__processado += 1
    self.registrar('Executando')

  def registrar(self, estado='Finalizado'):
    self.__historico.append(estado)

  def entrarNaMemoria(self):
    self.__ativo = True

  def obterHistorico(self):
    return self.__historico

  def obterInicio(self):
    return self.__inicio

  def obterTitulo(self):
    return self.__titulo

  def obterEstado(self):
    return self.__ativo

  def obterProcessado(self):
    return self.__processado

  def obterTempoNecessario(self):
    return self.__necessario

  def init(self):
    self.__console.linha(21)
    self.__titulo = self.__console.obter('Titulo do processo')
    self.__inicio = self.__console.obter('Em qual tempo ele ira entrar na memoria?', tipo='int')
    self.__necessario = self.__console.obter('Tempo necessario', tipo='int')
    self.__console.linha(21)
    for fatia in range(self.__inicio):
      self.registrar('Não alocado')
