import ConfigParser

# This singleton class has some constants regarding Fail-Over.
class HybridConfigurations(ConfigParser.RawConfigParser):

    PRI_IP = None
    SEC_IP = None
    DOMAIN = None
    USERNAME = None
    PASS = None
    PRI_FRONTEND = None
    SEC_FRONTEND = None
    LISTENING_PORT = None
    KEYSTONE_PORT = None

    __filepath = 'hybrid.conf'
    __hybridconf = None

    def __new__(cls, *args, **kwargs):
        if not HybridConfigurations.__hybridconf:
            HybridConfigurations.__hybridconf = HybridConfigurations()
        return HybridConfigurations.__hybridconf

    def __init__(self):
        ConfigParser.RawConfigParser.__init__(self)
        self.read(self.__filepath)
        
	HybridConfigurations.PRI_IP = self.get('services_ips', 'primary_ip')
	HybridConfigurations.SEC_IP = self.get('services_ips', 'secondary_ip')

	HybridConfigurations.DOMAIN = self.get('dns', 'public_domain')
        HybridConfigurations.USERNAME = self.get('dns', 'username')
        HybridConfigurations.PASS = self.get('dns', 'pass')
		
	HybridConfigurations.PRI_FRONTEND = self.get('frontend_ips', 'primary_frontend_ip')
	HybridConfigurations.SEC_FRONTEND = self.get('frontend_ips', 'secondary_frontend_ip')
        HybridConfigurations.LISTENING_PORT = self.get('frontend_ips', 'listening_port')

	HybridConfigurations.KEYSTONE_PORT = self.get('services_endpoints_ports', 'keystone_port')
