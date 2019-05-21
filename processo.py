class Processo(object):
  def __init__(self):
    self.__titulo = ''
    self.__inicio = 0
    self.__necessario = 0
    self.__processado = 0
    self.__ativo = False
    self.__finalizado = False

  def status(self):
    msg = 'Pronto'
    if self.__necessario - self.__processado <= 0:
      self.__finalizado = True
      msg = 'Finalizado'
    if not self.__ativo:
      msg = 'Não Alocado'
    return msg

  def run(self, quantum):
    resto = self.__processado + quantum - self.__necessario
    if resto >= 0:
      self.__processado += quantum - resto
      return resto
    else:
      self.__processado += quantum
      return 0

  def entrarNaMemoria(self):
    self.__ativo = True

  def obterInicio(self):
    return self.__inicio

  def obterTitulo(self):
    return self.__titulo

  def obterProcessado(self):
    return self.__processado

  def init(self):
    self.__titulo = input('\n\tTitulo do processo\n> ')
    self.__inicio = int(input('\n\tEm qual tempo ele ira entrar na memoria?\n> '))
    self.__necessario = int(input('\n\tTempo necessario\n> '))
