import serial
from Aplicacao import *
from ARQ import *
from Enquadramento import *


def menu():
    print('Digite o número da porta serial:')
    porta = '/dev/pts/' + input()
    p_serial = serial.Serial(porta, 9600, timeout=10)
    print("Digite uma mensgam para ser enviada ou aguarde o recebimento de uma mensagem")

    aplicacao = Aplicacao()

    arq = ARQ(2)
    arq.conecta(superior=aplicacao)

    enquadramento = Enquadramento(p_serial)
    enquadramento.conecta(superior=arq)

    sched = poller.Poller()
    sched.adiciona(aplicacao)
    sched.adiciona(arq)
    sched.adiciona(enquadramento)
    sched.despache()

if __name__ == "__main__":
    menu()
