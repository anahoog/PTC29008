#!/usr/bin/python3

import crc

fcs = crc.CRC16('123456')
msg = fcs.gen_crc()
print('Mensagem com FCS:', msg)

fcs.clear()
fcs.update(msg)
print('Resultado da verificação da mensagem com FCS:', fcs.check_crc())

msg=msg[:-1]
fcs.clear()
fcs.update(msg)
print('Resultado da verificação da mensagem com FCS após modificá-la:', fcs.check_crc())