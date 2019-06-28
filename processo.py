from console import Console


class Processo(object):
  def __init__(self):
    self.__console = Console()
    self.titulo = ''
    self.inicio = 0
    self.necessario = 0
    self.processado = 0
    self.historico = []
    self.ativo = False
    self.finalizado = False

  def status(self):
    msg = 'Pronto'
    if self.finalizado:
      msg = 'Finalizado'
    elif not self.ativo:
      msg = 'Não Alocado'
    return msg

  def run(self):
    self.processado += 1
    self.registrar('Executando')
    if self.necessario - self.processado <= 0:
      self.finalizado = True

  def registrar(self, estado='Finalizado'):
    self.historico.append(estado)

  def entrarNaMemoria(self):
    self.ativo = True

  def init(self, titulo):
    self.__console.linha(21)
    self.titulo = titulo
    self.inicio = self.__console.obter('Em qual tempo ele ira entrar na memoria?', tipo='int')
    self.necessario = self.__console.obter('Tempo necessario', tipo='int')
    self.__console.linha(21)
    for fatia in range(self.inicio):
      self.registrar('Não alocado')
