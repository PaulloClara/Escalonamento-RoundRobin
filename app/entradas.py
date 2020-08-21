from app.console import Console


class Entradas(object):
    def __init__(self):
        self.quantum = 0
        self.trocaDeContexto = 0
        self.tituloDosProcessos = []
        self.dicionarioDeDicionariosDeProcessos = {}

    def processarArquivo(self):
        self.quantum = int(Console.obter().split(': ')[1])
        self.trocaDeContexto = int(Console.obter().split(': ')[1])
        Console.obter()  # Discartando linha
        self.tituloDosProcessos = Console.obter().upper().split(' ')
        listaDeEntradaNaMemoria = Console.obter().split(' ')
        Console.obter()  # Discartando linha
        Console.obter()  # Discartando linha
        listaDeTimeSlicesNecessarios = Console.obter().split(' ')
        for i in range(len(self.tituloDosProcessos)):
            tituloDoProcesso = self.tituloDosProcessos[i]
            entradaNaMemoria = int(listaDeEntradaNaMemoria[i])
            tempoNecessario = int(listaDeTimeSlicesNecessarios[i])
            self.dicionarioDeDicionariosDeProcessos[tituloDoProcesso] = {
                'entrada': entradaNaMemoria,
                'necessario': tempoNecessario
            }

    def processarManual(self):
        self.quantum = int(Console.obter(
            'Quanto vale o quantum?'
        ))
        self.trocaDeContexto = int(Console.obter(
            'Quanto vale a troca de contexto?'
        ))
        quantidadeDeProcessos = int(Console.obter(
            'Quantidade de processos'
        ))
        for i in range(quantidadeDeProcessos):
            tituloDoProcesso = Console.obter(
                f'Titulo do processo {i+1}'
            ).upper()
            self.tituloDosProcessos.append(tituloDoProcesso)
        for i in range(quantidadeDeProcessos):
            tituloDoProcesso = self.tituloDosProcessos[i]
            Console.adicionar_separador(tamanho=22)
            entradaNaMemoria = int(Console.obter(
                f'Em qual fatia de tempo "{tituloDoProcesso}" entra na memoria?'
            ))
            tempoNecessario = int(Console.obter(
                f'Quantas fatias de tempo "{tituloDoProcesso}" irá precisar?',
                linhas=0
            ))
            Console.adicionar_separador(tamanho=22)
            Console.quebrar_linha(vezes=2)

            self.dicionarioDeDicionariosDeProcessos[tituloDoProcesso] = {
                'entrada': entradaNaMemoria,
                'necessario': tempoNecessario
            }
