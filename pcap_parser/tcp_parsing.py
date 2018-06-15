import matplotlib.pyplot as plt
import numpy
import os

from scapy.all import rdpcap, \
                      TCP, \
                      IP

FIG_SIZE = (6.0, 16.0)


def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(
            rect.get_x()+rect.get_width()/2., 0.05 + height, '%d' %
            int(height), ha='center', va='bottom')


class TCPTrafficSequence:

    def __init__(self,
                 srv_port=8888,
                 srv_ip="127.0.0.1",
                 file_name="tst.pcapng"):
        self._srv_port = srv_port
        self._srv_ip = srv_ip
        self._file_name = file_name
        self._sequence = []
        self._stats_dir = '{0}_stats'.format(self._file_name.split(".")[0])

        self.payload_size = 0
        self.overhead_size = 0

        self.ctrl_pkts = 0
        self.data_pkts = 0

    def init(self):
        packets = rdpcap(self._file_name)
        for pkt in packets:

            if pkt.haslayer(TCP) \
               and pkt[TCP].dport == self._srv_port \
               and ((pkt[IP].src == self._srv_ip) or
                    (pkt[IP].dst == self._srv_ip)):

                self.add_payload_to_seq(pkt)
                payload_len = len(pkt[TCP].payload)

                self.overhead_size += len(pkt[IP]) - payload_len
                self.payload_size += payload_len

                if payload_len == 0:
                    self.ctrl_pkts += 1
                else:
                    self.data_pkts += 1

    def add_payload_to_seq(self, pkt):
        self._sequence += pkt[TCP].payload

    @property
    def payload_ratio(self):
        return self.payload_size / self.overhead_size

    def ctrl_msgs_to_data_msgs(self):
        # colors = matplotlib.colors.cnames.keys()
        msg_tags = ["control", "data"]
        colors = ["red", "blue"]
        msg_counts = [self.ctrl_pkts, self.data_pkts]
        plt.figure(num=1, figsize=FIG_SIZE)
        h = plt.bar(numpy.arange(len(msg_tags)),
                    msg_counts,
                    label=msg_tags,
                    color=colors)
        xticks_pos = [
                0.65 * patch.get_width() + patch.get_xy()[0] for patch in h]
        plt.xticks(xticks_pos, msg_tags, ha='right', rotation=80)
        autolabel(h)
        plt.tight_layout()
        plt.title("Number of TCP data messages and control messages")
        plt.savefig(
                os.path.join(self._stats_dir, "msg_count_ctrl_to_data.png"))
        plt.close()

    def payload_to_overhead(self):
        msg_tags = ["overhead data bytes", "payload data bytes"]
        colors = ["red", "blue"]
        msg_counts = [self.overhead_size, self.payload_size]
        plt.figure(num=1, figsize=FIG_SIZE)
        h = plt.bar(numpy.arange(len(msg_tags)),
                    msg_counts,
                    label=msg_tags,
                    color=colors)
        xticks_pos = [
                0.65 * patch.get_width() + patch.get_xy()[0] for patch in h]
        plt.xticks(xticks_pos, msg_tags, ha='right', rotation=80)
        autolabel(h)
        plt.tight_layout()
        plt.title("TCP Overhead to Payload")
        plt.savefig(os.path.join(self._stats_dir, "overhead_to_payload.png"))
        plt.close()

    def make_stats_dir(self):
        os.makedirs(self._stats_dir, exist_ok=True)

    def create_statistics_files(self):
        self.make_stats_dir()

        self.ctrl_msgs_to_data_msgs()
        self.payload_to_overhead()
