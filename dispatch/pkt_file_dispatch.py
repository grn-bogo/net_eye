#! /usr/bin/env

from .pkt_dispatch import PacketDispatcher
from scapy.all import rdpcap


class PacketFileDispatcher(PacketDispatcher):
    '''Definition of PacketDispatcher for files of packets.
    Args:
        pkt_src: str - network interface (wlan0, eth0, lo, ...)
        filtr: str - tcpdump-like filters (BPF)
    '''
    def __init__(self, pkt_src=""):
        '''
        '''
        super(PacketFileDispatcher, self).__init__(pkt_src)
        self._pkt_iter = (x for x in rdpcap(self.pkts_src))

    def __next__(self):
        '''
        '''
        return self._pkt_iter.__next__()

    def __len__(self):
        '''
        '''
        nr = 0
        for pkt in rdpcap(self.pkts_src):
            nr += 1
        return nr
