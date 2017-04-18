import ConfigParser
from DraasConfigurations import DraasConfigurations


# This singleton class has some constants regarding Keystone.
class KeystoneConfigurations(ConfigParser.RawConfigParser):

    # Attributes Start #

    # Since everything is public in python. So, some conventional tactics have been used.

    # '_' with some attribute means a protected attribute. One should not touch this unless one's using it in subclass.
    # Similarly, '__' with some attribute means a private attribute. And, except this class, no other class can use it.
    # And attribute with no sign means a public attribute and can be used anywhere.
    REMOTEIP = None
    LOCALIP = None
    PORT = None
    LOCALDB = None
    LOGFILESDIR = None
    SYNCTIME = None
    RESTOREFILE = None
    RPO = None
    DUMPFILE = None
    STATE = None
    NETMASK = None
    GATEWAY = None

    __filepath = '/etc/draas/keystone.conf'
    __keystoneconf = None
    # Attributes End #

    #  Functions Start #

    def __new__(cls, *args, **kwargs):
        if not KeystoneConfigurations.__keystoneconf:
            KeystoneConfigurations.__keystoneconf = KeystoneConfigurations()
        return KeystoneConfigurations.__keystoneconf

    def __init__(self):
        ConfigParser.RawConfigParser.__init__(self)
        self.read(self.__filepath)
        KeystoneConfigurations.REMOTEIP = self.get('keystone', 'remote_ip')
        KeystoneConfigurations.LOCALIP = self.get('keystone', 'local_ip')
        KeystoneConfigurations.PORT = self.get('keystone', 'port')
        KeystoneConfigurations.LOCALDB = self.get('keystone', 'local_db')
        KeystoneConfigurations.LOGFILESDIR = self.get('keystone', 'log_files_dir')
        KeystoneConfigurations.SYNCTIME = self.get('keystone', 'sync_time')
        KeystoneConfigurations.RPO = self.get('keystone', 'RPO')
        KeystoneConfigurations.RESTOREFILE = self.get('keystone', 'restore_file')
        KeystoneConfigurations.DUMPFILE = self.get('keystone', 'dump_file')
        KeystoneConfigurations.STATE = self.get('keystone', 'state')
        KeystoneConfigurations.NETMASK = self.get('network', 'netmask')
        KeystoneConfigurations.GATEWAY = self.get('network', 'gateway')
        #  Functions End #
