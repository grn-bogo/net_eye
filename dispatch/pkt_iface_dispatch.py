#! /usr/bin/env python3

from .packet_dispatcher import PacketDispatcher
from collections import deque
from scapy.all import sniff
from threading import Thread
from time import sleep


class PacketIfaceDispatcher(PacketDispatcher):
    '''Definition of PacketExtractor for NIC packet extraction
    Args:
        pkt_src: str <- network interface (wlan0, eth0, lo, ...)
        maxbuf: int <- max. number of packets able to hold without readings
        filtr: str <- tcpdump-like filters (BPF)
    '''
    def __init__(self, pkt_src=None, maxbuf=100, filtr=""):
        '''
        '''
        super(PacketIfaceDispatcher, self).__init__(pkt_src)
        self._filter = filtr
        self._circbuf = deque(maxlen=maxbuf)
        self._pkt_miss = 0
        self._maxbuf = maxbuf

    def __next__(self):
        '''
        '''
        try:
            thread = Thread(target=self._sniff)
            thread.start()
            while True:
                try:
                    pkt = self._circbuf.popleft()
                except IndexError:
                    sleep(0.5)
                else:
                    return pkt
        except KeyboardInterrupt:
            raise StopIteration
        finally:
            thread.join()

    def _sniff(self):
        '''
        '''
        sniff(iface=self._pkt_src, prn=self._pkt_callback, filter=self._filter,
              store=0)

    def _pkt_callback(self, pkt):
        '''
        '''
        if len(self._circbuf) == self._maxbuf:
            self._pkt_miss += 1
        self._circbuf.append(pkt)
