#!/usr/bin/python
import socket
import sys

class bcolors:
    BOLD = '\033[1m'
    ABERTA = '\033[92m'
    FECHADA = '\033[91m'
    END = '\033[0m'

dominio = sys.argv[1]
ports = sys.argv[2].split()
print bcolors.BOLD + "Porta\tStatus\tCodigo" + bcolors.END
for x in ports:
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.settimeout(0.1)
    codigo = cliente.connect_ex((dominio, int(x)))
    if codigo == 0:
        print x, bcolors.ABERTA + bcolors.BOLD + "\tAberta\t" + bcolors.END, " ",codigo
    else:
        print x, bcolors.FECHADA + bcolors.BOLD + "\tFechada\t" + bcolors.END, " ",codigo

