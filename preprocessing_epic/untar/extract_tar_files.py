import os
from glob import glob
import tarfile
import tqdm

import argparse

parser = argparse.ArgumentParser()

# Dataloading-related settings
parser.add_argument('--p', type=str, default=None,
                    help="Path to 'frames_rgb_flow' folder")
args = parser.parse_args()


def search_tar_files(frames_rgb_flow_path):
    tar_file_names = []
    tar_file_paths = []
    for m in ['flow', 'rgb']:
        for split in ['test', 'train']:
            current_path = os.path.join(frames_rgb_flow_path, m, split)
            for path, subdirs, files in os.walk(current_path):
                for _p, s, f in os.walk(path):
                    for _f in f:
                        tar_file_paths.append(_p)
                        tar_file_names.append(_f)
    return tar_file_names, tar_file_paths


def untar_files(tar_file_names, tar_file_paths):
    progress_bar = tqdm.tqdm(
        range(len(tar_file_names)))
    for i in progress_bar:

        progress_bar.set_description(
            f"Extracting [{i + 1}/{len(tar_file_names)}]")

        current_arq_path = os.path.join(tar_file_paths[i], tar_file_names[i])

        my_tar = tarfile.open(current_arq_path)
        # specify which folder to extract to
        my_tar.extractall(tar_file_paths[i])
        my_tar.close()


if __name__ == "__main__":

    frames_rgb_flow_path = ''
    if args.p is None:
        ROOT_PATH = os.path.abspath(os.getcwd())
        frames_rgb_flow_path = os.path.join(ROOT_PATH, 'frames_rgb_flow')
    else:
        frames_rgb_flow_path = args.p
    print(f"Extracting files from the folder: {frames_rgb_flow_path}")
    tar_file_names, tar_file_paths = search_tar_files(frames_rgb_flow_path)
    untar_files(tar_file_names, tar_file_paths)
