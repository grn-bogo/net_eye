#! /usr/bin/env python3
from abc import ABC, abstractmethod


class PacketDispatcher(ABC):
    '''API definition - Dispatcher of packet from a source
    Args:
        pkt_src: string - packets source (iface, file, ...)
    '''
    def __init__(self, pkt_src=""):
        '''
        '''
        if not pkt_src:
            raise ValueError("No packet source")
        super(PacketDispatcher, self).__init__()
        self.__pkt_src = pkt_src

    def __iter__(self):
        '''
        '''
        return self

    @abstractmethod
    def __next__(self):
        '''
        '''
        pass

    @property
    def pkts_src(self):
        '''
        '''
        return self.__pkt_src
