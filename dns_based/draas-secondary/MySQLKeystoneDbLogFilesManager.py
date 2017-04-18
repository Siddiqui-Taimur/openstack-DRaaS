import os
import subprocess
from DBLogFilesManager import DBLogFilesManager
from KeystoneConfigurations import KeystoneConfigurations
from DraasConfigurations import DraasConfigurations


# Every dbms can have its own way of maintaining log files. Similarly, creating sql and flushing techniques
# can also vary. However, this class provides the mechanism  for creating logs, extracting sql(s) and
# flushing logs for MySQL.
class MySQLKeystoneDbLogFilesManager(DBLogFilesManager):

    # Attributes Start #

    # Since everything is public in python. So, some conventional tactics have been used.

    # '_' with some attribute means a protected attribute. One should not touch this unless one's using it in subclass.
    # Similarly, '__' with some attribute means a private attribute. And, except this class, no other class can use it.
    # And attribute with no sign means a public attribute and can be used anywhere.

    # Attributes End #

    #  Functions Start #

    def __init__(self):
        pass

    def renamelogs(self, logdirectory):
        for filename in os.listdir(logdirectory):
            self.renamefile(logdirectory + filename, logdirectory + filename + '.old')

    def flushlogs(self):
        output = subprocess.call(['scripts/flushlog.sh'])    # Executes a script file.
        if output != 0:
            raise subprocess.CalledProcessError('Script returend non-zero value', output)

    def createsql(self):
        subprocess.call(['scripts/createsql.sh', KeystoneConfigurations.LOCALDB,
                         DraasConfigurations.WORKDIR + KeystoneConfigurations.RESTOREFILE])

    def createdump(self, database, outputfile):
        output = subprocess.call(['scripts/dump.sh', database, outputfile])    # Executes a script file.
        if output != 0:
            raise subprocess.CalledProcessError('Script returend non-zero value', output)

    def executesql(self, database, inputfile):
        output = subprocess.call(['scripts/executesql.sh', database, inputfile])
        if output != 0:
            raise subprocess.CalledProcessError('Script returend non-zero value', output)

    def bintosql(self, database, outputfile):
        subprocess.call(['scripts/bintosql.sh', database, outputfile])
