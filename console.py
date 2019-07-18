class Console(object):
  def __init__(self):
    pass

  def obter(self, msg='', tipo=''):
    valor = ''
    while not valor:
      if msg:
        valor = input(f'\t\t{msg}\n\t\t> ')
        self.quebraDeLinha()
      else:
        valor = input()
    if tipo == 'int':
      return int(valor)
    elif tipo == 'float':
      return float(valor)
    else:
      return valor.lower().replace('  ', ' ').replace('   ', ' ')

  def mostrar(self, msg, n='\n', t='\t'):
    print(f'{t}{msg}', end=n)

  def linha(self, quantidade):
    resultado = '=-' * quantidade + '='
    print(f'\t{resultado}')

  def quebraDeLinha(self, numeroDeLinhas=1):
    print('\n' * (numeroDeLinhas-1))
