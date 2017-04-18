#!/usr/bin/python           
import socket
import urllib
from HybridConfigurations import HybridConfigurations

def rebindDNS(ip):
    content  = urllib.urlopen('http://'+HybridConfigurations.USERNAME+':'+HybridConfigurations.PASS+'@dynupdate.no-ip.com/nic/update?hostname='+HybridConfigurations.DOMAIN+'&myip=' + ip).read()
    print 'Ready to DNS Re-binding for again primary front-end', content

print 'Connecting to secondary front-end'
HybridConfigurations()
s = socket.socket() 
s.connect((HybridConfigurations.SEC_FRONTEND, int(HybridConfigurations.LISTENING_PORT)))
print 'Connected'
rebindDNS(HybridConfigurations.PRI_FRONTEND)
s.close
