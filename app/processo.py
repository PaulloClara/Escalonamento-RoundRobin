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
            self.registrar('nao alocado')

    def status(self):
        if self.finalizado:
            mensagem = 'finalizado'
        elif not self.ativo:
            mensagem = 'nao alocado'
        else:
            mensagem = 'pronto'
        return mensagem

    def run(self):
        self.processado += 1
        self.registrar('executando')
        if self.necessario - self.processado <= 0:
            self.finalizado = True

    def registrar(self, estado='finalizado'):
        self.historico.append(estado)

    def entrarNaMemoria(self):
        self.ativo = True
