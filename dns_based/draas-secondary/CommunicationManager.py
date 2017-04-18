import socket
import threading
from abc import ABCMeta, abstractmethod
from ftplib import FTP


# Communication Manager is an abstract class that can handle all possible types of communication
# between two systems from simple chat messages to file transfer (using FTP). Additionally, it
# extends the thread class since disaster recovery of every component should reside on an independent
#  thread.
class CommunicationManager(threading.Thread):
    __metaclass__ = ABCMeta  # Abstract Class #

    # Attributes Start #

    # Since everything is public in python. So, some conventional tactics have been used.

    # '_' with some attribute means a protected attribute. One should not touch this unless one's using it in subclass.
    # Similarly, '__' with some attribute means a private attribute. And, except this class, no other class can use it.
    # And attribute with no sign means a public attribute and can be used anywhere.

    _socket = None
    _ftp = None

    # Attributes End #

    #  Functions Start #

    # Constructor instantiating a socket and FTP object. Socket is used for the
    # application layer communication whereas FTP object helps in transmission of files
    # between data centers.
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
        self._ftp = FTP()
        super(CommunicationManager, self).__init__()

    # sync method should have the procedural way to keep two or more data centers synchronized. And, it
    # is MUST for every child class (Disaster Recovery of component) to implement this method.
    @abstractmethod
    def _sync(self):
        raise NotImplementedError

    # This is the conventional 'run' method of thread. Procedural way for disaster recovery to
    # take place independently should be implemented or called here.
    @abstractmethod
    def run(self):
        super(CommunicationManager, self).run()
        # Functions End #
