import ConfigParser

# This singleton class has some constants regarding Fail-Over.
class FrontendConfigurations(ConfigParser.RawConfigParser):

    PRI_IP = None
    SEC_IP = None
    FRONTEND_IP = None
    KEYSTONE_PORT = None

    __filepath = 'frontend.conf'
    __frontendconf = None

    def __new__(cls, *args, **kwargs):
        if not FrontendConfigurations.__frontendconf:
            FrontendConfigurations.__frontendconf = FrontendConfigurations()
        return FrontendConfigurations.__frontendconf

    def __init__(self):
        ConfigParser.RawConfigParser.__init__(self)
        self.read(self.__filepath)
        FrontendConfigurations.PRI_IP = self.get('services_ips', 'primary_ip')
	FrontendConfigurations.SEC_IP = self.get('services_ips', 'secondary_ip')
	FrontendConfigurations.FRONTEND_IP = self.get('this_server_ip', 'frontend_server_ip')
        FrontendConfigurations.KEYSTONE_PORT = self.get('services_endpoints_ports', 'keystone_port')
