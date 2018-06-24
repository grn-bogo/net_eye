#! /usr/bin/env python

import unittest
from dispatcher.packet_file_dispatcher import PacketFileDispatcher


class TestPacketFileDispatcher(unittest.TestCase):
    '''
    '''
    def setUp(self):
        self.nr_pkts_in_http2_pcap = 24
        self.file_name = "test/http2.pcap"

    def test_number_of_packets(self):
        packets = PacketFileDispatcher(self.file_name)
        self.assertEqual(self.nr_pkts_in_http2_pcap, len(packets))

    def test_throwing_exception(self):
        self.assertRaises(ValueError, PacketFileDispatcher)

    def test_piling_packets_into_list(self):
        lst = list()
        packets = PacketFileDispatcher(self.file_name)
        for pkt in packets:
            lst.append(pkt)
        self.assertEqual(len(lst), len(packets))
