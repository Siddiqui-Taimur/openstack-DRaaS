#!/usr/bin/env python
import os
import platform
import time
import urllib
import json
import socket

# setting default timeout for all type of sockets, change it according to your needs
#  here we are setting this 2 sec timeout for testing purposes in our local environment
socket.setdefaulttimeout(2)

# hostname
hostname =  'namaltesting.ddns.net'


# globle ping string for checking out the platform
ping_plat = ""

if platform.system().lower()=="windows":
        ping_plat = "-n 1"
else:
        ping_plat = "-c 1 -W1"



check = 0
start_time = None
tries = 0
print 'Requesting ....'
while True:
        response = os.system("ping " + ping_plat + " " + hostname)
        if response == 0:
		tries = 0
                web_res = None
                api_res = None
                web_latency = None
                api_latency = None
                try:
                        webStart = time.time()
                        web_res = urllib.urlopen('http://'+hostname)
                        if web_res.getcode()==200:
                                web_latency  = time.time()-webStart
                                print '\nStatus code for web_response = ', web_res.getcode(), '\nWeb_latency = ', web_latency
                        apiStart = time.time()
                        api_res = urllib.urlopen('http://'+hostname+':5000/v2.0/')
                        if api_res.getcode()==200:
                                api_latency  = time.time()-apiStart
                                print '\nStatus code for api_response = ', api_res.getcode(), '\nApi_latency = ', api_latency
                        print '\nSo, All is well so far...'
                except Exception as e:
                        print '\nThere are some connection issues in Keystone service, its not working properly'
                        if check==0:
                                # measuring the start time when the host goes down
                                start_time = time.time()
                                check=1

                if check!=0 and (None not in (web_res, api_res)) and web_res.getcode()==api_res.getcode()==200:
                        end_time = time.time()-start_time - web_latency - api_latency - 1 # subtracting 1 coz. it's over head due to some above cals.
                        if end_time <= 1:
                                print '\n\nNo Downtime is detected'
                        else:
                                print '\nTotal downtime or RTO = ', end_time, ' seconds'
                
                        break
        
        else:
                if check==0 and tries==1:
                        # measuring the start time when the host goes down
                        start_time = time.time()
                        check=1
		tries = 1 		# lets give it two tries atleast
                print 'Trying...'
                
