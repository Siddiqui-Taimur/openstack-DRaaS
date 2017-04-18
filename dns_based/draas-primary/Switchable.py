from abc import ABCMeta, abstractmethod


class Switchable:
    __metaclass__ = ABCMeta

    def __init__(self):
        pass

    @abstractmethod
    def switch(self, newip, oldip):
        raise NotImplementedError
