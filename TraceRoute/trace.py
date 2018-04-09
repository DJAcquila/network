#!/usr/bin/python

import socket
import os
import sys
import struct
import time	

class flushfile(file):
    def __init__(self, f):
        self.f = f
    def write(self, x):
        self.f.write(x)
        self.f.flush()

sys.stdout = flushfile(sys.stdout)

def main():
	d_url = sys.argv[1]

	ttl = 1

	d_addr = socket.gethostbyname(d_url)

	port = 33434

	max_h = 35

	sys.stdout.write("Tracerouting to: %s (%s) [%d hops max] [Port: %d]\n\n" % (d_addr, d_url, max_h, port))

	while ttl < max_h:

		recv = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
		send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.getprotobyname('udp'))
		#Set the value of the given socket option
		send.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)

		#socket.setsockopt(level, optname, value)
		recv.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, struct.pack("ll", 5, 0))

		recv.bind(("", port))

		t = (time.time())

		sys.stdout.write(" %d \t" % ttl)
		send.sendto("",(d_url, port))

		flag = False
		recv_addr = None
		recv_name = None

		
			
		try:
			_, c_addr = recv.recvfrom(512)

			roundt = ((time.time()) - t) * 1000
			#sys.stdout.write("Teste: %s\n" % c_addr[0])
			
			c_addr = c_addr[0]
			
			c_name = socket.gethostbyaddr(c_addr)[0]

			flag = True

		except socket.error:
			
			sys.stdout.write("* * *")
			sys.stdout.write("\n")
						
		send.close()
		recv.close()
		
		if c_addr is not None and flag is not False:
			sys.stdout.write("(%s)  %s  %.3f ms\n" %(c_addr, c_name, roundt))

		ttl = ttl + 1

		if (c_addr == d_addr): 
			break

main()
