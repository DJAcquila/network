import socket
from urlparse import urlparse

class Parser():
	"""
		Parser: Esta clase reunira funcoes para lidar com parsing de url e manipulacoes http
	"""
	def __init__(self):
		self.end_line = '\r\n'
		self.end_header = '\r\n\r\n'

	def http_request(self, hostname, path):
		"""
			param: hostname (string do hostname), path (caminho da requisicao)
			http_request: Este metodo ira montar um requisicao HTTP para enviar ao servidor
			return: Requisicao HTTP montada
		"""
		method = 'GET ' + path + ' HTTP/1.1' + self.end_line
		host = 'Host: ' + hostname + self.end_line
		connection = 'Connection: close' + self.end_line
		charset = 'Accept-charset: utf-8' + self.end_line
		request = (method + host + charset +connection + self.end_line)
		return request

	def get_http_field(self, request, name, end):
		"""
			param: request (string da requisicao), name (campo http buscado), end (final do campo)
			get_http_field: Metodo para buscar um valor especifico dentro de um campo especifico da requisicao
			return: Ira retornar o valor relativo ao campo buscado
		"""
		#try:
		start_idx = request.index(name)
		name_end_len = start_idx + len(name)
		field_end_len = name_end_len + request[name_end_len : ].index(end)
		val = request[name_end_len: field_end_len]
		return val
		#except:
			#print("O campo informadaormado nao foi encontrado")
			#return '-1'

	def parse_url(self, url):
		""" 
			param: url (string com a url)
			parse_url: Este metodo ira realizar o parsing da url com a ajuda da 
				biblioteca urlparse, afim de retornar o pathname e o hostname
			return: hostname e pathname em uma lista
		"""
		path = urlparse(url).path
		hostname = urlparse(url).hostname
		return [hostname, path]

	def add_If_Modified_Since(self, request, date):
		"""
			param: request (string da requisicao), date (data a se adicionar no campo last-modified
			add_If_Modified_Since: Este metodo adiciona da reqisicao que sera feita ao servidor o campo If-Modified-Since
				com a data informada
			return: nova mensagem de requisicao com o campo If-Modified-Since
		"""
		try:
			end_value = request.index(self.end_header) + len(self.end_line) 
			old = request[ : end_value]
			If_Modified_Since_field = 'If-Modified-Since: ' + self.end_line
			new = old + If_Modified_Since_field + self.end_line
			return new
		except:
			print("Erro ao tentar adicionar o campo If-Modified-Since")
			return "-1"