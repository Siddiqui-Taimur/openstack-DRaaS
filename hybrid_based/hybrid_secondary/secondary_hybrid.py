#!/usr/bin/env python
import os
import platform
import time
import urllib
import subprocess
import requests
import socket
from HybridConfigurations import HybridConfigurations

# Before importing 'requests' library make sure you've installed this using 'pip install requests'


HybridConfigurations()
primary_frontend  = HybridConfigurations.PRI_FRONTEND
sec_frontend      = HybridConfigurations.SEC_FRONTEND


def rebindDNS(ip):
    content  = urllib.urlopen('http://'+HybridConfigurations.USERNAME+':'+HybridConfigurations.PASS+'@dynupdate.no-ip.com/nic/update?hostname='+HybridConfigurations.DOMAIN+'&myip=' + ip).read()
    print 'Ready to DNS Re-binding for sec_frontend', content



s = socket.socket()         # Creating server socket
s.bind((HybridConfigurations.SEC_FRONTEND, int(HybridConfigurations.LISTENING_PORT)))          # Binding to the port
s.listen(1)                 # listening for client request, but can queue up only 1 client at a time, because it needs one i.e primaryFrontend for sync

while True:
    print 'Waiting for primary_frontend Connection...'
    conn, addr = s.accept()     # Establishing connection.
    print 'Connection found from', addr
    tries = 1
    start_time = None
    print 'Starting to check primary front-end'
    while True:
	if tries==1:
	    start_time = time.time()
        time.sleep(4)
        response = os.system('ping -c 1 -W1 ' + primary_frontend)
        if response == 0:
            tries = 1
            try:
                web_res = requests.get('http://' + primary_frontend, allow_redirects=False)
                api_res = requests.get('http://' + primary_frontend +':'+HybridConfigurations.KEYSTONE_PORT+'/v2.0/', allow_redirects=False)
                print 'web_res = ', web_res
		print 'api_res = ', api_res
                if (web_res.status_code!=302 or api_res.status_code!=302):
                    rebindDNS(sec_frontend)
		    print '\nTotal detection time = ', time.time()-start_time, ' seconds, \nSubtract this time from total downtime then u can have total rebind N Old bind remove time'
                    break
            except requests.exceptions.Timeout:
                print '\nInternet issue or Timeout but trying again...'
            except requests.exceptions.RequestException as e:
                print '\nRequest Exception'
                rebindDNS(sec_frontend)
	        print '\nTotal detection time = ', time.time()-start_time, ' seconds, \nSubtract this time from total downtime then u can have total rebind N Old bind remove time'
                break
        else:
            if tries == 2:
                rebindDNS(sec_frontend)
	        print '\nTotal detection time = ', time.time()-start_time, ' seconds, \nSubtract this time from total downtime then u can have total rebind N Old bind remove time'
                break
            tries = 2
   

    conn.close()                # Close the connection


