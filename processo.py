from console import Console


class Processo(object):
  def __init__(self, titulo, inicio, necessario):
    self.titulo = titulo
    self.inicio = inicio
    self.necessario = necessario
    self.processado = 0
    self.historico = []
    self.ativo = False
    self.finalizado = False
    for fatia in range(self.inicio):
      self.registrar('Não alocado')

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
