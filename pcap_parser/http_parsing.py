from pcap_parser import TCPTrafficSequence
from pcap.all import HTTP


class HTTPTrafficSequence(TCPTrafficSequence):
    def add_payload_to_seq(self, pkt):
        if pkt.haslayer(HTTP):
            self._sequence += pkt[HTTP].payload
