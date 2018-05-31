import glob
import logging
import os
import shutil
import subprocess

PROTOC_PY_CMD = 'protoc {proto_sources} -I{proto_dir} --python_out={out_dir} *.proto'


def generate_proto(root_path, output_path=None):
    proto_dirs = set()
    proto_files = proto_files_in_build(root_path)
    for file_path in proto_files:
        f_dir, f_name = _file_dir_and_name(file_path)
        proto_dirs.add(f_dir)

    if not output_path:
        output_path = os.path.join(root_path, 'generated_proto_py')

    os.makedirs(output_path, exist_ok=True)

    sources_in_cmd = ' -I' + '{sep} -I'.format(sep=os.sep).join(proto_dirs) + os.sep

    for proto_dir in sorted(proto_dirs):
        os.chdir(proto_dir)
        tree_location = os.path.relpath(proto_dir, os.path.join(root_path, 'Celer'))
        out_dir = os.path.join(output_path, tree_location)
        os.makedirs(out_dir, exist_ok=True)
        cmd = PROTOC_PY_CMD.format(proto_sources=sources_in_cmd,
                                   proto_dir=proto_dir,
                                   out_dir=os.path.join(output_path, tree_location))
        print(proto_dir)
        print(cmd)
        try:
            subprocess.check_output(cmd, shell=True)
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


if __name__ == "__main__":
    ver, rever = git_root()
    generate_proto(root_path=ver)
