#!/usr/bin/python3

from serial import Serial
import sys

try:
    porta = '/dev/pts/4'

except:
    print('Uso: %s porta_serial' % sys.argv[0])
    sys.exit(0)

try:
    p = Serial(porta, 9600, timeout=10)
except Exception as e:
    print('Não conseguiu acessar a porta serial', e)
    sys.exit(0)

msg = 'um testekkkkk ...\r\n'

n = p.write(msg.encode('ascii'))
print('Enviou %d bytes' % n)

input('Digite ENTER para terminar:')

sys.exit(0)
