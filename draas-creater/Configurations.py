import ConfigParser


# This class contains some constant regarding DRaaS after reading draas.conf.
class Configurations(ConfigParser.RawConfigParser):

    # Attributes Start #

    # Since everything is public in python. So, some conventional tactics have been used.

    # '_' with some attribute means a protected attribute. One should not touch this unless one's using it in subclass.
    # Similarly, '__' with some attribute means a private attribute. And, except this class, no other class can use it.
    # And attribute with no sign means a public attribute and can be used anywhere.

    DISASTERS = []
    __draascreater = None
    __filename = 'draas-creater.conf'

    # Attributes End #

    #  Functions Start #

    def __new__(cls, *args, **kwargs):
        if not Configurations.__draascreater:
            Configurations.__draascreater = Configurations()
        return Configurations.__draascreater

    def __init__(self):
        ConfigParser.RawConfigParser.__init__(self)
        self.read(self.__filename)
        options = self.options('default')
        for option in options:
            if self.get('default', option) == 'enable':
                Configurations.DISASTERS.append(option)
