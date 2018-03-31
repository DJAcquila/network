#!/usr/bin/python

import socket, os, sys, struct, binascii

def met_tcp_header(recv):
	'''
 	0                   1                   2                   3
	0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	|          Source Port          |       Destination Port        |
	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	|                        Sequence Number                        |
	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	|                    Acknowledgment Number                      |
	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	|  Data |           |U|A|P|R|S|F|                               |
	| Offset| Reserved  |R|C|S|S|Y|I|            Window             |
	|       |           |G|K|H|T|N|N|                               |
	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	|           Checksum            |         Urgent Pointer        |
	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	|                    Options                    |    Padding    |
	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	|                             data                              |
	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	'''
	tcp_header = struct.unpack("!2H2I4H", recv[:20])
	source_port = tcp_header[0]
	destination_port = tcp_header[1]
	sequence_number = tcp_header[2]
	acknowledgment_number = tcp_header[3]
	data_offset = tcp_header[4] >> 12
	reserverd = (tcp_header[4] >> 6) & 0x03ff
	flag = tcp_header[4] &0x003f
	urgent_pointer = flag & 0x0020
	acknowledgment = flag & 0x0010
	push = flag & 0x0000
	reset = flag & 0x0004
	sync = flag & 0x0002
	fin = flag & 0x0001
	window = tcp_header[5]
	check_sum = tcp_header[6]
	urgent_pointer = tcp_header[7]
	
	recv = recv[20:]
	
	return recv
def met_udp_header(recv):
	'''
	 0      7 8     15 16    23 24    31  
     +--------+--------+--------+--------+ 
     |     Source      |   Destination   | 
     |      Port       |      Port       | 
     +--------+--------+--------+--------+ 
     |                 |                 | 
     |     Length      |    Checksum     | 
     +--------+--------+--------+--------+ 
     |                                     
     |          data octets ...            
     +---------------- ...       
	'''
	udp_header = struct.unpack("!4H", recv[:8])
	source_port = udp_header[0]
	destination_port = udp_header[1]
	length = udp_header[2]
	check_sum = udp_header[3]
	
	recv = recv[8:]
	
	return recv
def met_ip_header(recv):
	''' 
	0                   1                   2                   3
	0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	|Version|  IHL  |Type of Service|          Total Length         |
	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	|         Identification        |Flags|      Fragment Offset    |
	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	|  Time to Live |    Protocol   |         Header Checksum       |
	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	|                       Source Address                          |
	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	|                    Destination Address                        |
	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	|                    Options                    |    Padding    |
	+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
	'''
	ip_header = struct.unpack("!6H4s4s", recv[:20])
	type_of_service = ip_header[0] & 0x00ff
	version = ip_header[0] >> 12
	ihl = (ip_header[0] >> 8) & 0x0f
	total_len = ip_header[1]
	identification = ip_header[2]
	flags = ip_header[3] >> 13
	offset = ip_header[3] & 0x1fff
	time = ip_header[4] >> 8
	protocol = ip_header[4] & 0x00ff
	checksum = ip_header[5]
	end_maquina_saida = socket.inet_ntoa(ip_header[6])
	end_maquina_destino = socket.inet_ntoa(ip_header[7])
	no_frag = flags >> 1
	more_frag = flags & 0x01
	
	print "+----------------------IP Header------------------------+"
	print "+                                                       +"
	print "+\tVersion:\t%hu\t\t\t\t+" % version
	print "+\tIHL:\t%hu\t\t\t\t\t+" %ihl
	print "+\tType of Service:\t%hu\t\t\t+" % type_of_service
	print "+\tTotal Length:\t%hu\t\t\t\t+" % total_len
	print "+\tIdentification:\t%hu\t\t\t\t+"% identification
	print "+\tNo Frag:\t%hu\t\t\t\t+" % no_frag
	print "+\tMore Frag:\t%hu\t\t\t\t+" % more_frag
	print "+\tFragment Offset:\t%hu\t\t\t+" % offset
	print "+\tTime to Live\t%hu\t\t\t\t+" % time
	print "+\tNext Protocol:\t%hu\t\t\t\t+" % protocol
	print "+\tCheck Sum:\t%hu\t\t\t\t+" % checksum
	print "+\tIP Source:\t%s\t\t\t\b +" % end_maquina_saida
	print "+\tIP Dest:\t%s\t\t\t\b +" % end_maquina_destino
	print "+                                                       +"
	print "+-------------------------------------------------------+"

	if protocol == 6:
		prox = 'TCP'
	elif protocol == 17:
		prox = 'UDP'
	else:
		prox = 'nul'
	recv = recv[20:]
	
	return recv, prox
	
def met_ethernet_header(recv):
	ip = False
	# The firs parameter is the mac destination (6 octets)
	# When using '(number)s' we have the number of bytes wanted
	et_header = struct.unpack("!6s6sH", recv[:14])
	end_maquina_destino = binascii.hexlify(et_header[0])
	end_maquina_saida = binascii.hexlify(et_header[1])
	end_maquina_protocolo = et_header[2] >> 8
	print "+-------------------Ethernet Header---------------------+"
	print "+                                                       +"
	print "+\tMAC address destino:\t%s %s %s %s %s %s\t+" % (end_maquina_destino[0:2], end_maquina_destino[2:4], end_maquina_destino[4:6], 			end_maquina_destino[6:8], end_maquina_destino[8:10], end_maquina_destino[10:12])
	print "+\tMAC address de saida:\t%s %s %s %s %s %s\t+" % (end_maquina_saida[0:2], end_maquina_saida[2:4], end_maquina_saida[4:6], 			end_maquina_saida[6:8], end_maquina_saida[8:10], end_maquina_saida[10:12])
	print "+\tProtocolo:\t%s\t\t\t\t+" %hex(end_maquina_protocolo)
	print "+                                                       +"
	print "+-------------------------------------------------------+"
	#IPv4 == 0X0800
	
	if end_maquina_protocolo == 0x08:
		ip = True
	recv = recv[14:]
	
	return recv, ip
def main():
	'''Convert 16-bit positive integers from host to network byte order. On machines
	where the host byte order is the same as network byte order, this is a no-op; otherwise, 
	it performs a 2-b
	yte swap operation.'''
	'''socket.PF_PACKET to send and recieve messages, below the internet protocol layer
	The process must be run with root access'''
	''' When using socket.bind(()) we will redirect the access to an especific port
	I am using socket.RAW, so i dont want to bind my connection to a port'''
	sniffer = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.htons(0x0003))
	recv = sniffer.recv(2048)
	os.system("clear")
	dados, ip = met_ethernet_header(recv)
	#print ip
	if ip:
		dados, prox = met_ip_header(recv)
	else:
		return
		
	if prox == 'TCP':
		dados = met_tcp_header(recv)
	elif prox == 'UDP':
		dados = met_udp_header(recv)
while True:	
	main()