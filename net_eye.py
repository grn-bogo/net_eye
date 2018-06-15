#! /usr/bin/env python3
import logging


def create_logger(name):
    '''

    '''
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def main(argv):
    '''

    '''
    from argparse import ArgumentParser
    from pcap_parser.tcp_parsing import TCPTrafficSequence
    parser = ArgumentParser()
    parser.add_argument(
            '-pcap',
            help='Absolute path of pcap or pcapng file to be processed',
            action='store',
            type=str,
            default='test2.pcap',
            dest="pcap_path")
    parser.add_argument(
            '-ip',
            help='IP address of the processed traffic s serving entity',
            action='store',
            type=str,
            dest="srv_ip")
    parser.add_argument(
            '-port',
            help='TCP port of the processed traffic s serving entity',
            action='store',
            type=int,
            dest="tcp_port")
    args = parser.parse_args()

    logger.info("  @@@@@@@@@@@@@@@@@@@@@@@@@")
    logger.info("  -------------------------")
    logger.info("||    N E T   --  E Y E    ||")
    logger.info("  -------------------------")
    logger.info("  @@@@@@@@@@@@@@@@@@@@@@@@@")

    logger.debug("Arguments: -----")
    for arg in vars(args):
        logger.debug("arg[{k}] = {v}".format(k=arg, v=getattr(args, arg)))
    logger.debug("----------------")

    sequence = TCPTrafficSequence(
                    srv_port=args.tcp_port,
                    srv_ip=args.srv_ip,
                    file_name=args.pcap_path)
    sequence.init()

    logger.info(
        "PAYLOAD: {0}, OVERHEAD {1}".format(
            sequence.payload_size, sequence.overhead_size))
    logger.info(
        "PAYLOAD TO OVERHEAD {0}".format(sequence.payload_ratio))

    sequence.create_statistics_files()


if __name__ == '__main__':
    import sys
    logger = create_logger('net_eye')
    main(sys.argv)
