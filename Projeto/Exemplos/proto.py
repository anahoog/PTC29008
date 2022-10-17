import Enquadramento
import Adaptacao
import poller
import serial
import sys

porta = serial.Serial(sys.argv[1], 9600)
framing = Enquadramento.Enquadramento(porta, 1)
terminal = Adaptacao.Adaptacao()
framing.conecta(terminal)

sched = poller.Poller()
sched.adiciona(framing)
sched.adiciona(terminal)

sched.despache()