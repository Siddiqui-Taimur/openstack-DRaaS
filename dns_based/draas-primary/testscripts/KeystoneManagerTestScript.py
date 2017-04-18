from KeystoneManager import KeystoneManager
from KeystoneConfigurations import KeystoneConfigurations


if __name__ == '__main__':
    kc = KeystoneConfigurations()
    km = KeystoneManager()
    km.start()