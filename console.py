class Console(object):
  def __init__(self):
    pass

  def obter(self, msg='', tipo='', n=1):
    valor = ''
    while not valor:
      if msg:
        valor = input(f'\t{msg}\n\t> ')
        if n:
          self.quebraDeLinha(n)
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
