#!/usr/bin/python

import SimpleHTTPServer
import SocketServer
import urllib
import time
import json
import socket
from FrontendConfigurations import FrontendConfigurations


# setting default timeout for all type of sockets, Uncomment the following line according to the test nature

# Testing purposes for local machines
socket.setdefaulttimeout(0.7)

# For AWS 
#socket.setdefaulttimeout(3.3)

class MasterRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

	def do_GET(self):
		print 'Someone is rquesting...'
		aliveServer = self.find_aliveServer()      	
		self.send_response(302)
	       	self.send_header('Location','http://' +aliveServer + ':' +FrontendConfigurations.KEYSTONE_PORT + self.path)
		print 'Redirected to ' + aliveServer
       		self.end_headers()
		return



	def find_aliveServer(self):

		primary = FrontendConfigurations.PRI_IP

		sec = FrontendConfigurations.SEC_IP

		#tries = 1

		start_time = time.time()

		json_obj = None

		try:

        		ans = urllib.urlopen('http://' +primary+ ':' +FrontendConfigurations.KEYSTONE_PORT+ '/v2.0/')

        		string = ans.read().decode('utf-8')

			json_obj = json.loads(string)

		except Exception as e:

        		print '\nPrimary keystone service is not responding, its not working properly'

		if json_obj!=None and json_obj['version']['status'] == 'stable':

			print '\nRedirection Time = ', (time.time()-start_time), ' seconds'

			return primary

		else:

			print '\nTotal downtime or RTO = ', (time.time()-start_time), ' seconds'	

			return sec



		# must add the case if both are down				



try:

	
	FrontendConfigurations()
	thisServerIP = FrontendConfigurations.FRONTEND_IP
	# this port will identify which endpoint you are accessing, the below one is for Keystone(identity)
	PORT = 	int(FrontendConfigurations.KEYSTONE_PORT)
	server = SocketServer.TCPServer((thisServerIP, PORT), MasterRequestHandler)

	print "HTTP API endpoint(Keystone) server started at port", PORT

	server.serve_forever()



except KeyboardInterrupt:

	print 'shutting down the server'

	server.socket.close()
