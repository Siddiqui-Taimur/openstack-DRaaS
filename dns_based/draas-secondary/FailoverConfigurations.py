import ConfigParser

# This singleton class has some constants regarding Fail-Over.
class FailoverConfigurations(ConfigParser.RawConfigParser):

    DNS_STATUS = None
    DOMAIN = None
    USERNAME = None
    PASS = None
    FRONTEND_STATUS = None
    HYBRID_STATUS = None

    __filepath = 'failover.conf'
    __failoverconf = None

    def __new__(cls, *args, **kwargs):
        if not FailoverConfigurations.__failoverconf:
            FailoverConfigurations.__failoverconf = FailoverConfigurations()
        return FailoverConfigurations.__failoverconf

    def __init__(self):
        ConfigParser.RawConfigParser.__init__(self)
        self.read(self.__filepath)
        FailoverConfigurations.DNS_STATUS = self.get('dns_based', 'status')
	FailoverConfigurations.DOMAIN = self.get('dns_based', 'public_domain')
        FailoverConfigurations.USERNAME = self.get('dns_based', 'username')
        FailoverConfigurations.PASS = self.get('dns_based', 'pass')
        FailoverConfigurations.FRONTEND_STATUS = self.get('front_end_based', 'status')
        FailoverConfigurations.HYBRID_STATUS = self.get('hybrid_based', 'status')
