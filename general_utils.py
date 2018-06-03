import glob
import logging
import os
import shutil
import subprocess

PROTOC_ALL_CMD = 'protoc -I. --cpp_out={proto_cpp} --python_out={proto_py} {proto_file}'


def generate_proto(proto_root):
    proto_files = proto_files_in_build(proto_root)

    output_path_py = os.path.join('..', 'generated_proto_py')
    output_path_cpp = os.path.join('..', 'generated_proto_cpp')
    os.makedirs(output_path_cpp, exist_ok=True)
    os.makedirs(output_path_py, exist_ok=True)

    cmd_template = PROTOC_ALL_CMD
    os.chdir(proto_root)

    for proto_file in proto_files:
        rel_file_path = os.path.relpath(proto_file, proto_root)
        cmd = cmd_template.format(proto_cpp=output_path_cpp,
                                  proto_py=output_path_py,
                                  proto_file=rel_file_path)
        print(cmd)
        try:
            subprocess.check_output(str(cmd), shell=True)
        except subprocess.CalledProcessError as e:
            pass


def proto_files_in_build(root_path):
    return _files_with_extension(path=root_path, extension='proto')


def log_files_in_build(root_path):
    return _files_with_extension(path=root_path, extension='log')


def _files_with_extension(path, extension):
    return [file for fs_elem in os.walk(path) for file in glob.glob(
        os.path.join(fs_elem[0], '*.{ext}'.format(ext=extension)))]


def _file_dir_and_name(file_path):
    path_chunks = file_path.split(os.sep)
    file_name = path_chunks[len(path_chunks) - 1]
    location_dir = os.sep.join(path_chunks[:len(path_chunks) - 1])
    return location_dir, file_name


def log_horizontal_sep():
    logging.error(90 * "#")


def copy_r(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        src_path = os.path.join(src, item)
        dst_path = os.path.join(dst, item)
        if os.path.isdir(src_path):
            if not os.path.exists(dst_path):
                shutil.copytree(src_path, dst_path, symlinks, ignore)
        else:
            shutil.copy2(src_path, dst_path)


def git_root():
    top_level = subprocess.check_output('git rev-parse --show-toplevel', shell=True)
    if type(top_level) is not str:
        top_level = top_level.decode("utf-8")

    dir_parts = top_level.replace('\n', '').split('/')
    return os.path.join(dir_parts[0] + os.sep, *dir_parts[1:]), top_level.replace('\n', '')
