class Processo(object):
    def __init__(self, dados):
        self.nome = dados['nome']
        self.inicio = dados['inicio']
        self.fatias = dados['fatias']

        self.historico = []
        self.processado = 0

        self.ativo = False
        self.finalizado = False

        for fatia in range(self.inicio):
            self.registrar(estado='nao alocado')

    def run(self):
        self.registrar('executando')
        self.processado += 1

        if self.fatias - self.processado <= 0:
            self.finalizado = True

    def estado(self):
        if self.finalizado:
            mensagem = 'finalizado'
        elif not self.ativo:
            mensagem = 'nao alocado'
        else:
            mensagem = 'pronto'

        return mensagem

    def registrar(self, estado='finalizado'):
        self.historico.append(estado)

    def entrar_na_memoria(self):
        self.ativo = True
