import socket
import os
import sys
import select

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 3:
	print "Numero de argumentos invalido"
	print "Esperado:\tpython script.py 'IP' 'PORT'"
	exit()
IP = str(sys.argv[1])
PORT = int(sys.argv[2])
server.connect((IP , PORT))

while True:
	sockets = [sys.stdin , server]
	
	legivel_sockets, gravar_socket, erro_socket = select.select(sockets,[],[])

	for s in legivel_sockets:
		if s == server:
			mensagem = s.recv(1024)
			print mensagem
		else:
			mensagem =  sys.stdin.readline()
			server.send(mensagem)
			sys.stdout.write("[Voce] ")
			sys.stdout.write(mensagem)
			sys.stdout.flush()

server.close()