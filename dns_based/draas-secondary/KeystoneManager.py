import os
import urllib
import time
import subprocess
from socket import timeout as TimeoutException
from ftplib import all_errors as FTPException
from CommunicationManager import CommunicationManager
from DraasConfigurations import DraasConfigurations
from DraasLogFilesManager import DraasLogFilesManager
from KeystoneConfigurations import KeystoneConfigurations
from FailoverConfigurations import FailoverConfigurations
from MySQLKeystoneDbLogFilesManager import MySQLKeystoneDbLogFilesManager
#from Switchable import Switchable


# This class extends 'CommunicationManager' so, intuitively it should inherit all the communication
# powers of its parental class. This class is responsible for handling all the communication of 'Keystone'
# required for its recovery in disaster.
class KeystoneManager(CommunicationManager):
    # Attributes Start #

    # Since everything is public in python. So, some conventional tactics have been used.

    # '_' with some attribute means a protected attribute. One should not touch this unless one's using it in subclass.
    # Similarly, '__' with some attribute means a private attribute. And, except this class, no other class can use it.
    # And attribute with no sign means a public attribute and can be used anywhere.

    __keystonedbman = None
    __connectioncounter = 0

    # Attributes End #

    #  Functions Start #

    # Constructor #
    def __init__(self):
        super(KeystoneManager, self).__init__()
        self.__keystonedbman = MySQLKeystoneDbLogFilesManager()
        # Initializing the communication socket
        self._socket.setblocking(True)
        self._socket.bind(('', int(KeystoneConfigurations.PORT)))
        self._socket.listen(5)
        self._socket.settimeout(int(KeystoneConfigurations.SYNCTIME) + int(KeystoneConfigurations.RPO))

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
            try:
                print("Ready to accept")
                connection, address = self._socket.accept()
                print("Connection Found..!!")
                while True:
                    reply = connection.recv(1024)
                    print("Reply: " + reply)
                    if reply == 'SYN':
                        connection.sendall('SYNACK')
                        continue
                    elif reply == 'SENT':
                        connection.sendall('ACKQUIT')
                        connection.close()
                        self.__keystonedbman.executesql(KeystoneConfigurations.LOCALDB,
                                                        DraasConfigurations.WORKDIR +
                                                        KeystoneConfigurations.RESTOREFILE)
                        self.__keystonedbman.deletefile(DraasConfigurations.WORKDIR +
                                                        KeystoneConfigurations.RESTOREFILE)
                        for filename in os.listdir(KeystoneConfigurations.LOGFILESDIR):
                            self.__keystonedbman.deletefile(KeystoneConfigurations.LOGFILESDIR + filename)
                        self.__keystonedbman.flushlogs()
                        break
                    elif reply == 'EMERGENCY':
                        self.__keystonedbman.renamelogs(KeystoneConfigurations.LOGFILESDIR)
                        self.__keystonedbman.flushlogs()
                        for filename in os.listdir(KeystoneConfigurations.LOGFILESDIR):
                            if filename.endswith('old'):
                                print("Moving from " + KeystoneConfigurations.LOGFILESDIR + filename +
                                      " to " + DraasConfigurations.WORKDIR + filename)
                                self.__keystonedbman.movefile(KeystoneConfigurations.LOGFILESDIR + filename,
                                                              DraasConfigurations.WORKDIR + filename)
                        self.__keystonedbman.bintosql(KeystoneConfigurations.LOCALDB,
                                                      DraasConfigurations.WORKDIR +
                                                      KeystoneConfigurations.RESTOREFILE)
                        print('FTP at ' + address[0])
                        self._ftp.connect(address[0])
                        self._ftp.login(user=DraasConfigurations.USERNAME, passwd=DraasConfigurations.PASS)
                        print('Login Success')
                        self._ftp.storbinary('STOR ' + KeystoneConfigurations.RESTOREFILE, open(
                            DraasConfigurations.WORKDIR + KeystoneConfigurations.RESTOREFILE, 'rb'))
                        print('Files Transfered')
                        self._ftp.quit()
                        print('FTP quit')
                        print("Log Files sent")
                        connection.sendall('SENT')
                        connection.close()
                        #subprocess.call(['scripts/ipchanger.sh', KeystoneConfigurations.LOCALIP,
                                         #KeystoneConfigurations.NETMASK, KeystoneConfigurations.GATEWAY])
                        self._socket.settimeout(int(KeystoneConfigurations.SYNCTIME) +
                                                int(KeystoneConfigurations.RPO))
			self.__keystonedbman.deletefile(DraasConfigurations.WORKDIR +
                                                        KeystoneConfigurations.RESTOREFILE)
			break
                    elif reply == 'RECOVER':
                        self.__keystonedbman.createdump(KeystoneConfigurations.LOCALDB,
                                                        DraasConfigurations.WORKDIR +
                                                        KeystoneConfigurations.DUMPFILE)
                        self._ftp.connect(address[0])
                        self._ftp.login(user=DraasConfigurations.USERNAME,
                                        passwd=DraasConfigurations.PASS)
                        self._ftp.storbinary('STOR ' + KeystoneConfigurations.DUMPFILE, open(
                            DraasConfigurations.WORKDIR + KeystoneConfigurations.DUMPFILE, 'rb'))
                        self._ftp.quit()
                        print("Dump File sent")
                        connection.sendall('SENT')
                        connection.close()
                        #subprocess.call(['scripts/ipchanger.sh', KeystoneConfigurations.LOCALIP,
                                         #KeystoneConfigurations.NETMASK, KeystoneConfigurations.GATEWAY])
                        self._socket.settimeout(int(KeystoneConfigurations.SYNCTIME) +
                                                int(KeystoneConfigurations.RPO))
                        self.__keystonedbman.deletefile(DraasConfigurations.WORKDIR +
                                                        KeystoneConfigurations.DUMPFILE)
                        break
                self.__connectioncounter = 0
                print("Going to write draas log.")
                DraasLogFilesManager.update('Keystone')
            except TimeoutException:
		if self.__connectioncounter == 0:
		    start_time = time.time()

                self.__connectioncounter += 1
                if self.__connectioncounter == 5:
                    print("Counter reached 5")
                    self._socket.settimeout(None)
                    #subprocess.call(['scripts/ipchanger.sh', KeystoneConfigurations.REMOTEIP,
                                     #KeystoneConfigurations.NETMASK, KeystoneConfigurations.GATEWAY])
                    #self.switch(KeystoneConfigurations.REMOTEIP, KeystoneConfigurations.LOCALIP)
                    #print("IP switched")
                    if FailoverConfigurations.DNS_STATUS=='enable':						
	                self.bindTo(KeystoneConfigurations.LOCALIP)
			print '\nThe disaster detection time is', (time.time() - start_time) + int(KeystoneConfigurations.RPO), ' Seconds'


            except (OSError, subprocess.CalledProcessError):
                print('Some error in files or script')
            except FTPException:
                print('Error in FTP connection')

    def bindTo(self, ip):
        #subprocess.call(['scripts/switch.sh', newip, oldip])
	content  = urllib.urlopen("http://" +FailoverConfigurations.USERNAME+ ":" +FailoverConfigurations.PASS+ "@dynupdate.no-ip.com/nic/update?hostname=" +FailoverConfigurations.DOMAIN+ "&myip=" + ip).read()
	print 'Ready to DNS Re-binding to', content

    # Wait for desired time and start sync process forever.
    def run(self):
        super(KeystoneManager, self).run()
        self._sync()

    def start(self):
        # super(KeystoneManager, self).setDaemon(True)
        return super(KeystoneManager, self).start()
        # Functions End #
