from utils.general import git_root, \
                          generate_proto
import os
if __name__ == '__main__':

    proto_root = os.path.join(git_root()[0], 'protobuf_defs')
    generate_proto(proto_root)
