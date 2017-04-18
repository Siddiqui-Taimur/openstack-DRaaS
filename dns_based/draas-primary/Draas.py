from DraasConfigurations import DraasConfigurations
from KeystoneConfigurations import KeystoneConfigurations
from FailoverConfigurations import FailoverConfigurations
from KeystoneManager import KeystoneManager


if __name__ == '__main__':
    DraasConfigurations()
    KeystoneConfigurations()
    FailoverConfigurations()
    services = DraasConfigurations.SERVICES.split(',')
    for service in services:
        if service == 'keystone':
            keystonedraas = KeystoneManager()
            keystonedraas.start()
