from enum import *
from Quadro import Quadro
from Subcamada import Subcamada

Flag = b'\x7E'
ESC = b'\x7D'


class Estado(Enum):
    ocioso = 0
    preparacao = 1
    recepcao = 2
    esc = 3


class Enquadramento(Subcamada):

    def __init__(self, porta_serial):
        self.porta_serial = porta_serial
        Subcamada.__init__(self, porta_serial, 2)
        self.estado = Estado.ocioso
        self.dados = bytearray()  # recebe os dados em byte
        self.n_bytes = 0  # contador de bytes que serão utilizados

    def envia(self, dados):
        quadroEnviado = bytearray()
        quadroEnviado += Flag
        quadroEnviado += dados.setCRC() #retorna o quadro inteiro com CRC
        quadroEnviado += Flag
        self.porta_serial.write(quadroEnviado)
        print('Enquadramento: Enviando: ', quadroEnviado)

    def recebe(self, dados):
        pass

    def handle(self):
        byte = self.porta_serial.read(1)

        if self.estado == Estado.ocioso:
            self.handle_ocioso(byte)

        elif self.estado == Estado.preparacao:
            self.handle_preparacao(byte)

        elif self.estado == Estado.recepcao:
            self.handle_recepcao(byte)

        elif self.estado == Estado.esc:
            self.handle_esc(byte)

    def handle_ocioso(self, byte):
        if byte == Flag:
            self.n_bytes = 0
            self.enable_timeout()
            self.estado = Estado.preparacao

    def handle_preparacao(self, byte):
        if byte == Flag:
            self.dados.clear()

        elif byte == ESC:
            self.estado = Estado.esc

        else:
            self.dados += byte
            self.estado = Estado.recepcao
            self.n_bytes += 1

    def handle_recepcao(self, byte):
        if byte == Flag:
            print("Enquadramento: Info recebida: " + str(self.dados))
            quadroRecebido = Quadro((self.dados[0] & (1 << 7)) >> 7, (self.dados[0] & (1 << 3)) >> 3, self.dados[2])
            quadroRecebido.anexaDados(self.dados[3:])
            self.voltaProOcioso()

            if quadroRecebido.checkCRC():
                print("Enquadramento: CRC OK do quadro recebido!")
                self.upper.recebe(quadroRecebido)
            else:
                print("Enquadramento: Erro no CRC!")

        elif byte == ESC:
            self.estado = Estado.esc

        else:
            self.dados += byte
            self.n_bytes += 1

    def handle_esc(self, byte):
        if byte == Flag or byte == ESC:
            self.voltaProOcioso()
        else:
            print("Enquadramento: Entrou no ESC")
            #self.dados += (int.from_bytes(byte, byteorder="big") ^ 20).to_bytes(1, byteorder="big")
            self.dados += (byte ^ b'0x20')
            self.estado = Estado.recepcao

    def handle_timeout(self):
        self.voltaProOcioso()

    def voltaProOcioso(self):
        self.disable_timeout()
        self.dados.clear()
        self.n_bytes = 0
        self.estado = Estado.ocioso

    def conecta(self, superior):
        self.upper = superior
        superior.lower = self
