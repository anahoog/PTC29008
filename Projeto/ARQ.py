from Enquadramento import *
from Quadro import *
from Subcamada import *
from enum import *


class Estado(Enum):
    ocioso = 0
    espera = 1


class ARQ(Subcamada):

    def __init__(self, tout):
        Subcamada.__init__(self, None, tout)
        self.estado = Estado.ocioso
        self.disable_timeout()
        self.quadro = None
        self.ultimoDataN = None
        self.seqN = 0 #sequencia N
        self.seqM = 0 #sequencia M
        self.dados = bytearray()
        self.quadroFromApp = False

    def envia(self, dados):
        self.dados = dados
        self.quadroFromApp = True
        self.MEF_ARQ()

    def recebe(self, quadro):
        self.quadro = quadro
        self.MEF_ARQ()

    def handle(self): #Não é usado para esta classe.
        pass

    def handle_timeout(self):
        print("Deu timeout no ARQ")
        if self.estado == Estado.espera:
            #self.disable_timeout()
            self.lower.envia(self.ultimoDataN)

    def MEF_ARQ(self):
        if self.estado == Estado.ocioso:
            if self.quadroFromApp:
                self.ultimoDataN = Quadro(0, self.seqN, 0)  # 0 para tipo de quadro DADOS, 0 para sequencia e byte de zeros para IDProto
                self.ultimoDataN.anexaDados(self.dados)
                self.reload_timeout()
                self.enable_timeout()
                self.estado = Estado.espera
                self.quadroFromApp = False
                self.lower.envia(self.ultimoDataN)
            else:
                if self.quadro.getTipoQuadro() == 0: #Quadro tipo DATA e não veio da aplicacao
                    self.trataData()

        elif self.estado == Estado.espera:
            if self.quadro.getTipoQuadro() == 0: #Quadro tipo DATA
                self.trataData()
            elif self.quadro.getTipoQuadro() == 1: #Quadro tipo ACK
                if self.quadro.getSequencia() == self.seqN: #Confere se a sequencia é a correta. Se for, volta pra ocioso. Se não for, não faz nada.
                    self.mudaSeqN()
                    self.disable_timeout()
                    self.estado = Estado.ocioso

    def mudaSeqN(self):
        if self.seqN == 0:
            self.seqN = 1
        else:
            self.seqN = 0

    def mudaSeqM(self):
        if self.seqM == 0:
            self.seqM = 1
        else:
            self.seqM = 0

    def trataData(self):
        # Criado para tratar exclusivamente das ações da MEF quando recebido quadro tipo DATA
        if self.quadro.getSequencia() == self.seqM:  # DATA recebido tem a sequencia esperada.
            quadroACK = Quadro(1, self.seqM, 0)
            self.mudaSeqM()
            self.lower.envia(quadroACK)
            self.upper.recebe(self.quadro.getDados())
        else:  # DATA recebido tem a sequencia barrada.
            #self.mudaSeqM()
            quadroACK = Quadro(1, self.quadro.getSequencia(), 0)
            self.lower.envia(quadroACK)

    def conecta(self, superior):
        self.upper = superior
        superior.lower = self
