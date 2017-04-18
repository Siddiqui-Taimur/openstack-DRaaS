import ConfigParser


# This class contains some constant regarding DRaaS after reading draas.conf.
class DraasConfigurations(ConfigParser.RawConfigParser):

    # Attributes Start #

    # Since everything is public in python. So, some conventional tactics have been used.

    # '_' with some attribute means a protected attribute. One should not touch this unless one's using it in subclass.
    # Similarly, '__' with some attribute means a private attribute. And, except this class, no other class can use it.
    # And attribute with no sign means a public attribute and can be used anywhere.

    SERVICES = None
    WORKDIR = None
    USERNAME = None
    PASS = None

    __filename = 'draas.conf'
    __draasconf = None
    # Attributes End #

    #  Functions Start #

    def __new__(cls, *args, **kwargs):
        if not DraasConfigurations.__draasconf:
            DraasConfigurations.__draasconf = DraasConfigurations()
        return DraasConfigurations.__draasconf

    def __init__(self):
        ConfigParser.RawConfigParser.__init__(self)
        self.read(self.__filename)
        DraasConfigurations.SERVICES = self.get('services', 'enable-services')
        DraasConfigurations.WORKDIR = self.get('work', 'dir')
        DraasConfigurations.USERNAME = self.get('credential', 'username')
        DraasConfigurations.PASS = self.get('credential', 'pass')
