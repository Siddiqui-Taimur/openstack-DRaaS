from KeystoneConfigurations import KeystoneConfigurations
from LogFilesManager import LogFilesManager
import datetime
from abc import ABCMeta


# Simple class to keep logs of this project.
class DraasLogFilesManager(LogFilesManager):
    __metaclass__ = ABCMeta

    # Attributes Start #

    # Since everything is public in python. So, some conventional tactics have been used.

    # '_' with some attribute means a protected attribute. One should not touch this unless one's using it in subclass.
    # Similarly, '__' with some attribute means a private attribute. And, except this class, no other class can use it.
    # And attribute with no sign means a public attribute and can be used anywhere.

    __logfilepath = '/var/log/draas/draas.log'

    # Attributes End #

    #  Functions Start #

    # Write the date and time of synchronization into the log file.
    @classmethod
    def update(cls, component):
        now = datetime.datetime.now()
        log = open(DraasLogFilesManager.__logfilepath, 'a')
        log.write('[' + component + '] Synchronized at ' + str(now.day) + '-' +
                  str(now.month) + '-' + str(now.year) + '  ' + str(now.hour) + ':' +
                  str(now.minute) + ':' + str(now.second) + ' at ' + ' IP:' +
                  KeystoneConfigurations.REMOTEIP + ' and Port: ' + KeystoneConfigurations.PORT + '\n')
        log.close()
        #  Functions End #
