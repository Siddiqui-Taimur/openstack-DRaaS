import ConfigParser


# This singleton class contains some constant regarding DRaaS after reading draas.conf.
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

    __filepath = '/etc/draas/draas.conf'
    __drassconf = None
    # Attributes End #

    #  Functions Start #

    def __new__(cls, *args, **kwargs):
        if not DraasConfigurations.__drassconf:
            DraasConfigurations.__drassconf = DraasConfigurations()
        return DraasConfigurations.__drassconf

    def __init__(self):
        ConfigParser.RawConfigParser.__init__(self)
        self.read(self.__filepath)
        DraasConfigurations.SERVICES = self.get('services', 'enable-services')
        DraasConfigurations.WORKDIR = self.get('work', 'dir')
        DraasConfigurations.USERNAME = self.get('credential', 'username')
        DraasConfigurations.PASS = self.get('credential', 'pass')

        #  Functions End #
