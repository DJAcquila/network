import socket
import sys
import threading
import parser as p

class Proxy():
	"""Classe que implementa as funcoes de proxy"""
	def __init__(self, host = "localhost", port = 54321, debug = True):
		self.parser = p.Parser()
		self.debug = debug
		self.host = host
		self.port = port
		self.cache = {}
		self.start()

	def start(self):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.bind((self.host, self.port))
			s.listen(1)
		except:
			print("Erro na abertura do socket")
			s.close()
			sys.exit(1)
		while 1:
			connection, address = s.accept()
			thread = threading.Thread(target = self.connect, args = (connection, address))
			thread.start()

	def host_path(self, request, connection):
		"""
			param: request (requisicao do cliente), e um socket relativo a conexao
			host_path: Este metodo ira recuperar da requisicao realizado o campo de url e o campo de caminho.Caso o 
				campo de caminho esteja na forma incorreta em relacao ao padrao de caminhos, ira ser feito
				um parser para extrair da url o caminho e o novo hostname.
			return: serao retornados a nova url e o novo 
		"""
		hostname = self.parser.get_http_field(request, 'Host: ', self.parser.end_line)
		path = self.parser.get_http_field(request, 'GET ', ' HTTP/1.1')
		
		if path == '-1' or hostname == '-1':
			print("Host nao identificado")
			connection.close()
			return
		# Caso o primeiro caractere da string nao for uma barra, o que indica um caminho, 
		# 	devemos extrair o hostname e o path da string	

		elif path[0] != '/':
			[hostname, path] = self.parser.parse_url(path)
		request = self.parser.http_request(hostname, path)
		url = hostname + path

		return request, url, hostname, path

	def connect(self, connection, address):
		utf8_request = connection.recv(4096)
		try:
			request = utf8_request.decode('utf-8')
			print("Requisicao do cliente: ")
			print(request)
		except:
			print("A requisicao nao esta em utf-8")
			connection.close()
			return
		#request, url, hostname, path = self.host_path(request, connection)
		
		hostname = self.parser.get_http_field(request, 'Host: ', self.parser.end_line)
		path = self.parser.get_http_field(request, 'GET ', ' HTTP/1.1')
		
		if path == '-1' or hostname == '-1':
			print("Host nao identificado")
			connection.close()
			return
		# Caso o primeiro caractere da string nao for uma barra, o que indica um caminho, 
		# 	devemos extrair o hostname e o path da string	

		elif path[0] != '/':
			[hostname, path] = self.parser.parse_url(path)
		request = self.parser.http_request(hostname, path)
		url = hostname + path

		if url in self.cache:
			print("URL" + url + "encontrada no cache")
			[tmp_response, tmp_date] = self.cache[url]
			print("Data de cache: " + tmp_date)
			# Para verificar se o dado de cache esta atualizado, enviar uma requisicao com o campo "If-Modified-Since"
			new_request = self.parser.add_If_Modified_Since(request, str(tmp_date))
			print("\t\tNova requisicao: \n" + new_request)
			request = new_request
			utf8_request = request.encode('utf-8')
		# Criar um metodo aqui, mas a principio abrir uma conexao para enviar uma requisicao ao host

		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock.connect((hostname, 80))
			sock.sendall(utf8_request)
		except:
		 	print("Problema na abertura do socket")
		 	sock.close()
		 	connection.close()
		 	return

		# esperar resposta do servidor
		server_response = b'' # cadeia de caracteres
		while True:
			data = sock.recv(4096)
			if not data:
				break
			server_response = server_response + data

		try:
			response = server_response.decode('utf-8')
			try:
				date = self.parser.get_http_field(response, "Last-Modified: ", self.parser.end_line)
				print(date)
			except:
				date = self.parser.get_http_field(response, "Date: ", self.parser.end_line)
		except:
			print("Erro na decodificacao do objeto")

		code = self.parser.get_http_field(response, "HTTP/1.1 ", self.parser.end_line)

		# objeto foi modificado
		if code == "200 OK":
			print("O cache sera atualizado...")
			self.cache[url] = [response, date]
			
			connection.sendall(server_response)
			connection.close()
		# objeto nao modificado, cache atualizado
		elif code == "304 Not Modified":
			# pegar o primeiro elemento do cache e transformar em uma resposta resposta em utf-8
			print("Cache hit!")
			r = self.cache[url][0].encode('utf-8')
			connection.sendall(r)
			connection.close()
		else:
			print("Problema com a requisicao")
			connection.close()
def main():
	proxy = Proxy("localhost", 54321, True)

if __name__ == '__main__':

	main()