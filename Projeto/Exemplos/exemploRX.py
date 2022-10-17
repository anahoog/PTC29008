#!/usr/bin/python3

from serial import Serial
import sys

try:
  porta = '/dev/pts/3'
except:
  print('Uso: %s porta_serial' % sys.argv[0])
  sys.exit(0)

try:
  p = Serial(porta, 9600, timeout=10)
except Exception as e:
  print('Não conseguiu acessar a porta serial', e)
  sys.exit(0)

  while():
    msg = p.read(128)
    print('Recebeu: ', msg)

#sys.exit(0)