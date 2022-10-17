import crc
Flag = b'\x7E'
ESC = b'\x7D'


class Quadro():

    def __init__(self, tipoQuadro, sequencia, idproto):
        self.quadro = bytearray()
        self.tipoQuadro = tipoQuadro # 0 para DATA e 1 para ACK
        self.sequencia = sequencia
        self.idproto = idproto
        self.dados = bytearray()
        byteReservado = bytes(1)  # ID conexão

        byteControle = bytearray(1)
        byteControle[0] = ((tipoQuadro << 7) | (sequencia << 3)) # usado no ARQ

        self.quadro = (byteControle + byteReservado)

        #if tipoQuadro == 0: #Tipo de quadro DATA
        self.quadro += self.idproto.to_bytes(1, 'big')

    def anexaDados(self, dados):
        #print("Quadro: Anexando dados: " + str(dados[0:1023]))
        self.dados += dados[0:1023] #sempre vai pegar 1024 bytes dos dados. Se for mais do que 1024, vai ignorar o excedente.
        self.quadro += dados[0:1023]
        #print("Quadro: Teste dados do quadro: " + str(self.dados))

    def getTipoQuadro(self):
        return self.tipoQuadro

    def getSequencia(self):
        return self.sequencia

    def getDados(self):
        #print("Dados retornados pelo quadro: " + str(self.dados))
        return self.dados[0:-2]

    def setCRC(self):
        quadroCRC = bytearray()
        fcs = crc.CRC16()
        fcs.update(self.quadro)
        data_crc = fcs.gen_crc()

        for i in range(0, len(data_crc)):
            if data_crc[i] == Flag:
                ESC_BYTE = b'\x5E'
                quadroCRC += (ESC + ESC_BYTE)
            elif data_crc[i] == ESC:
                ESC_BYTE = b'\x5D'
                quadroCRC += (ESC + ESC_BYTE)
            else:
                quadroCRC += bytes([data_crc[i]])

        fcs.clear()
        return quadroCRC #retorna quadro com CRC

    def checkCRC(self):
        fcs = crc.CRC16(self.quadro)
        if fcs.check_crc():
            self.quadro = self.quadro[0:-2]
            fcs.clear()
            return True
        else:
            return False
