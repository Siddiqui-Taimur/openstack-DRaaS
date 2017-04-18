import os
#os.environ['http_proxy']=''
import urllib
import time
import subprocess
from ftplib import all_errors as FTPException
from socket import error as ConnectionException
from CommunicationManager import CommunicationManager
from DraasConfigurations import DraasConfigurations
from KeystoneConfigurations import KeystoneConfigurations
from FailoverConfigurations import FailoverConfigurations
from MySQLKeystoneDbLogFilesManager import MySQLKeystoneDbLogFilesManager
from DraasLogFilesManager import DraasLogFilesManager
#from Switchable import Switchable


# This class extends 'CommunicationManager' so, intuitively it should inherit all the communication
# powers of its parental class. This class is responsible for handling all the communication of
# 'Keystone'
# required for its recovery in disaster.
class KeystoneManager(CommunicationManager):
    # Attributes Start #

    # Since everything is public in python. So, some conventional tactics have been used.

    # '_' with some attribute means a protected attribute. One should not touch this unless one's
    # using it in subclass.
    # Similarly, '__' with some attribute means a private attribute. And, except this class,
    # no other class can use it.
    # And attribute with no sign means a public attribute and can be used anywhere.

    __keystonedbman = None

    # Attributes End #

    #  Functions Start #

    # Constructor #
    def __init__(self):
        super(KeystoneManager, self).__init__()
        self.__keystonedbman = MySQLKeystoneDbLogFilesManager()

    # This method implements the process of synchronization for keystone once waiting time is over.
    # Pseudo code:
    # 1- Get the log files of dbms.
    # 2- Create new log files for next queries (flush logs).
    # 3- Move the created logs files to desired directory.
    # 4- Create sql file for 'keystone; queries only.
    # 5- Send 'SYN' message to secondary data center.
    # 6- Wait for the reply of 'SYNACK'.
    # 7- Transfer sql file to secondary data center.
    # 8- Send 'SENT' message.
    # 9- Wait for 'ACKQUIT' message.
    # 10- Close the connection
    def _sync(self):
        while True:
            if KeystoneConfigurations.STATE == 'Normal':
                time.sleep(int(KeystoneConfigurations.SYNCTIME))
                self._syncnormal()
            elif KeystoneConfigurations.STATE == 'Self-Recover':
                self._selfrecover()
            elif KeystoneConfigurations.STATE == 'Emergency':
                self._syncemergency()
            elif KeystoneConfigurations.STATE == 'Recover':
                self._syncrecover()
            DraasLogFilesManager.update('Keystone')

    def _syncnormal(self):
        if not self.__keystonedbman.isfile(DraasConfigurations.WORKDIR +
                                                   KeystoneConfigurations.RESTOREFILE):
	    print('Restore not found')
            try:
                self.__keystonedbman.renamelogs(KeystoneConfigurations.LOGFILESDIR)
                self.__keystonedbman.flushlogs()
                for filename in os.listdir(KeystoneConfigurations.LOGFILESDIR):
                    if filename.endswith('old'):
                        self.__keystonedbman.movefile(KeystoneConfigurations.LOGFILESDIR + filename,
                                                      DraasConfigurations.WORKDIR + filename)
                self.__keystonedbman.bintosql(KeystoneConfigurations.LOCALDB,
                                              DraasConfigurations.WORKDIR +
                                              KeystoneConfigurations.RESTOREFILE)
                for filename in os.listdir(DraasConfigurations.WORKDIR):
                    if filename.endswith('old'):
                        self.__keystonedbman.deletefile(DraasConfigurations.WORKDIR + filename)
                KeystoneConfigurations.STATE = 'Normal'
		print('Done')
            except(OSError, subprocess.CalledProcessError):
		print('Some error in files or service')
                if KeystoneConfigurations.STATE == 'Self-Recover':
                    KeystoneConfigurations.STATE = 'Emergency'
                else:
		    print('State = self-recover')
                    KeystoneConfigurations.STATE = 'Self-Recover'
                return

        try:
	    print('Connecting ',KeystoneConfigurations.REMOTEIP, ' and ',KeystoneConfigurations.PORT)
            self._createconnection((KeystoneConfigurations.REMOTEIP, int(KeystoneConfigurations.PORT)))
            self._socket.send('SYN')
            reply = self._socket.recv(1024)
            if reply == 'SYNACK':
                self._ftp.connect(KeystoneConfigurations.REMOTEIP)
                self._ftp.login(user=DraasConfigurations.USERNAME, passwd=DraasConfigurations.PASS)
                self._ftp.storbinary('STOR ' + KeystoneConfigurations.RESTOREFILE, open(
                    DraasConfigurations.WORKDIR + KeystoneConfigurations.RESTOREFILE, 'rb'))
                self._socket.send('SENT')
                reply = self._socket.recv(1024)
                if reply == 'ACKQUIT':
                    self._ftp.quit()
                    self._socket.close()
            self.__keystonedbman.deletefile(DraasConfigurations.WORKDIR +
                                            KeystoneConfigurations.RESTOREFILE)
	    KeystoneConfigurations.STATE = 'Normal'
        except (ConnectionException, FTPException, OSError):
            ## If connectios is.. clos i
	    print('Some problem in conn')
            if KeystoneConfigurations.STATE == 'Normal':
                KeystoneConfigurations.STATE = 'Self-Recover'
            else:
                KeystoneConfigurations.STATE = 'Emergency'

    def _selfrecover(self):
	print('Recovering')
	try:
            subprocess.call(['sudo ./draas-primary.sh'], shell = True)
	    self._syncnormal()
	except subprocess.CalledProcessError:
	    print('Cannot recover')

    def _syncemergency(self):
        try:
            subprocess.call(['ping -c1 8.8.8.8'], shell = True)
        except subprocess.CalledProcessError:
            time.sleep(KeystoneConfigurations.RPO)
            return
        else:
            try:
                self._createconnection((KeystoneConfigurations.LOCALIP,
                                        int(KeystoneConfigurations.PORT)))
		print('Connected ' + KeystoneConfigurations.LOCALIP)
            except ConnectionException:
                try:
                    self._createconnection((KeystoneConfigurations.REMOTEIP,
                                            int(KeystoneConfigurations.PORT)))
		    print('Connected ' + KeystoneConfigurations.REMOTEIP)
                except ConnectionException:
                    try:
			print('Switching IP')
                        #subprocess.call(['scripts/ipchanger.sh', KeystoneConfigurations.REMOTEIP,
                                     #KeystoneConfigurations.NETMASK, KeystoneConfigurations.GATEWAY])

###################
#                	self.switchTo("192.168.40.35")


                    except subprocess.CalledProcessError:
                        return
            try:
                self._socket.send('SYN')
		print('Connected after emergency')
                reply = self._socket.recv(1024)
                if reply == 'SYNACK':
                    self._socket.send(KeystoneConfigurations.STATE.upper())
                reply = self._socket.recv(1024)
                if reply == 'SENT':
                    self._socket.close()
                    self.__keystonedbman.executesql(KeystoneConfigurations.LOCALDB,
                                                    DraasConfigurations.WORKDIR +
                                                    KeystoneConfigurations.RESTOREFILE)
                    KeystoneConfigurations.STATE = 'Normal'
                    #subprocess.call(['scripts/ipchanger.sh', KeystoneConfigurations.LOCALIP,
                                     #KeystoneConfigurations.NETMASK, KeystoneConfigurations.GATEWAY])
                    #self.switch(KeystoneConfigurations.LOCALIP, KeystoneConfigurations.REMOTEIP)
                    self.__keystonedbman.deletefile(DraasConfigurations.WORKDIR +
                                                    KeystoneConfigurations.RESTOREFILE)
		    if FailoverConfigurations.DNS_STATUS=='enable':									
                       self.bindTo(KeystoneConfigurations.LOCALIP) # re-bind back to its own IP in DNS 

            except(ConnectionException, OSError, subprocess.CalledProcessError):
                pass

    def _syncrecover(self):
        #subprocess.call(['scripts/ipchanger.sh', KeystoneConfigurations.REMOTEIP,
                         #KeystoneConfigurations.NETMASK, KeystoneConfigurations.GATEWAY])
###############
        
#	self.switchTo("192.168.40.35")


        try:
            self._createconnection((KeystoneConfigurations.LOCALIP, int(KeystoneConfigurations.PORT)))
            self._socket.send('SYN')
            reply = self._socket.recv(1024)
            if reply == 'SYNACK':
                self._socket.send(KeystoneConfigurations.STATE.upper())
            reply = self._socket.recv(1024)
            if reply == 'SENT':
                self._socket.close()
                self.__keystonedbman.executesql(KeystoneConfigurations.LOCALDB,
                                                DraasConfigurations.WORKDIR +
                                                KeystoneConfigurations.DUMPFILE)
                KeystoneConfigurations.STATE = 'Normal'
                self.__connectioncounter = 0
                #subprocess.call(['scripts/ipchanger.sh', KeystoneConfigurations.LOCALIP,
                                 #KeystoneConfigurations.NETMASK, KeystoneConfigurations.GATEWAY])
                #self.switch(KeystoneConfigurations.LOCALIP, KeystoneConfigurations.REMOTEIP)
                print("reached to switch call")
                self.__keystonedbman.deletefile(DraasConfigurations.WORKDIR +
                                                KeystoneConfigurations.DUMPFILE)
		if FailoverConfigurations.DNS_STATUS=='enable':	
		   self.bindTo(KeystoneConfigurations.LOCALIP)
        except ConnectionException:
            pass

    #def switch(self, newip, oldip):
       #subprocess.call(['scripts/switch.sh', newip, oldip])

    def bindTo(self, ip):
	#subprocess.call(['scripts/switch.sh', newip, oldip])
	time.sleep(4) # this sleep time is  for the network to get stable as soon as this machine comes back from disaster to recover state
	content  = urllib.urlopen("http://" +FailoverConfigurations.USERNAME+ ":" +FailoverConfigurations.PASS+ "@dynupdate.no-ip.com/nic/update?hostname=" +FailoverConfigurations.DOMAIN+ "&myip=" + ip)
        print(content.read())


    # Wait for desired time and start sync process forever.
    def run(self):
        super(KeystoneManager, self).run()
        # self.__initsync()
        self._sync()

    def start(self):
        return super(KeystoneManager, self).start()

        #  Functions End #
