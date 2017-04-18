#!/usr/bin/python

import SimpleHTTPServer
import SocketServer
import urllib
import time
import json
import socket
from HybridConfigurations import HybridConfigurations


# setting default timeout for all type of sockets, Uncomment the following line according to the test nature

# Testing purposes for local machines
socket.setdefaulttimeout(0.7)

# For AWS 
#socket.setdefaulttimeout(3.5)

class MasterRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    

	def do_GET(self):
		aliveServer = self.find_aliveServer()      	
		self.send_response(302)
       		self.send_header('Location','http://' +aliveServer + self.path)
		print 'redirected to ' + aliveServer
       		self.end_headers()
		return



	def find_aliveServer(self):

		primary = HybridConfigurations.PRI_IP

		sec = HybridConfigurations.SEC_IP

		#tries = 1

		start_time = time.time()

		json_obj = None, 

		status = None

		try:

        		response = urllib.urlopen('http://' +primary)

			status = response.getcode()

		except Exception as e:

        		print '\nPrimary is down, its not working properly'

		if status!=None and status==200:

			print '\nRedirection Time = ', (time.time()-start_time), ' seconds'	

			return primary

		else:

			print '\nTotal downtime or RTO = ', (time.time()-start_time), ' seconds'	

			return sec



		# must add the case if both are down 

				



try:

	HybridConfigurations()
	thisServerIP = HybridConfigurations.PRI_FRONTEND
	# this port will identify what you are accessing, the below one is for keystone accessing via horizon or web 
	PORT = 80
	server = SocketServer.TCPServer((thisServerIP, PORT), MasterRequestHandler)


	print "Web server started at port", PORT

	server.serve_forever()



except KeyboardInterrupt:

	print 'shutting down the server'

	server.socket.close()
