from abc import ABCMeta
import os


# This abstract provide some basic file operations for the creation of log files.
class LogFilesManager:

    # Abstract Class #

    __metaclass__ = ABCMeta

    # Attributes Start #

    # Since everything is public in python. So, some conventional tactics have been used.

    # '_' with some attribute means a protected attribute. One should not touch this unless one's using it in subclass.
    # Similarly, '__' with some attribute means a private attribute. And, except this class, no other class can use it.
    # And attribute with no sign means a public attribute and can be used anywhere.

    # Attributes End #

    #  Functions Start #

    def __init__(self):
        pass

    def isfile(self, filename):
        return os.path.isfile(filename)

    def renamefile(self, filename, newfilename):
        os.rename(filename, newfilename)

    def movefile(self, srcpath, despath):
        self.renamefile(srcpath, despath)

    def deletefile(self, filename):
        os.remove(filename)

    def createfile(self, filename, mode='wb'):
        return open(filename, mode)

        #  Functions End #
