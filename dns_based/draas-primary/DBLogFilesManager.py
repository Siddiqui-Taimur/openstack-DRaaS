from abc import ABCMeta, abstractmethod
from LogFilesManager import LogFilesManager


# Almost every dbms keeps log of all the transactions made to it. And, some operations are needed to
# get those logs. Most common of them are: creating logs, flushing logs and creating sql(s).
# This abstract class provide the signatures of all these methods for all the child classes to implement.

class DBLogFilesManager(LogFilesManager):

    # Abstract Class #
    __metaclass__ = ABCMeta
    # Abstract Class #

    # Attributes Start #

    # Since everything is public in python. So, some conventional tactics have been used.

    # '_' with some attribute means a protected attribute. One should not touch this unless one's using it in subclass.
    # Similarly, '__' with some attribute means a private attribute. And, except this class, no other class can use it.
    # And attribute with no sign means a public attribute and can be used anywhere.

    # Attributes End #

    #  Functions Start #

    def __init__(self):
        pass

    @abstractmethod
    def flushlogs(self):
        raise NotImplementedError

    @abstractmethod
    def createdump(self, database, outputfile):
        raise NotImplementedError

    @abstractmethod
    def executesql(self, database, inputfile):
        raise NotImplementedError
