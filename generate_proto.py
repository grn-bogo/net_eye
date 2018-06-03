import general_utils
import os
if __name__ == '__main__':

    proto_root = os.path.join(general_utils.git_root()[0], 'protobuf_defs')
    general_utils.generate_proto(proto_root)


