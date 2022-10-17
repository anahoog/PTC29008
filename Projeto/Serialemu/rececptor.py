#!/usr/bin/python3

from serial import Serial
import sys

try:
    porta = sys.argv[1]
except:
    print('Uso: %s porta_serial' % sys.argv[0])
    sys.exit(0)

try:
    p = Serial(porta, 9600, timeout=5)
except Exception as e:
    print('Não conseguiu acessar a porta serial', e)
    sys.exit(0)


def menu():
    menu_principal = input("Press enter and exit")
    return menu_principal


if __name__ == '__main__':

    x = " "
    while x == " ":
        msg = p.read(1024)
        print("Mensagem Recebida: ", msg)

    # sys.exit(0)
