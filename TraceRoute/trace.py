#!/usr/bin/python

import socket
import os
import sys
import struct
import time	

class flush(file):
    def __init__(self, f):

        self.f = f

    def write(self, x):

        self.f.write(x)

        self.f.flush()


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
		i = 0
		flag1 = False
		rt = []
		while not flag and i < 3:
			
			try:
				_, c_addr = recv.recvfrom(512)

				roundt = ((time.time()) - t) * 1000
				rt.append(roundt)
				#sys.stdout.write("Teste: %s\n" % c_addr[0])
				c_addr = c_addr[0]
				
				try:
				
					c_name = socket.gethostbyaddr(c_addr)[0]

				except:
					c_name = c_addr

				flag = True

			except socket.error:
				i = i + 1	
				sys.stdout.write("* ")
				flag1 = True

		if flag1:
			sys.stdout.write("\n")
					
		send.close()
		recv.close()
		
		if c_addr is not None and flag is not False:

			sys.stdout.write("(%s)  %s " %(c_addr, c_name))
			for x in range(len(rt)):
				sys.stdout.write("%.3f ms " % rt[x])

			sys.stdout.write("\n")
		ttl = ttl + 1

		if (c_addr == d_addr): 
			break

sys.stdout = flush(sys.stdout)

main()
