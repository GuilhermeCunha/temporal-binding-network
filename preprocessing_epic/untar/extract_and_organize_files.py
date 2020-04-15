import os
from glob import glob
import tarfile
import tqdm

import argparse

parser = argparse.ArgumentParser()

# Dataloading-related settings
parser.add_argument('--p', type=str, default=None,
                    help="Path to 'frames_rgb_flow' folder")
parser.add_argument('--m', type=str, default=None,
                    help="Path to 'frames_rgb_flow' folder")
args = parser.parse_args()


class ExtractionClass:
    def __init__(self, frames_rgb_flow_path):
        self.frames_rgb_flow_path = frames_rgb_flow_path

        self.flow_tar_file_names = []
        self.flow_tar_file_paths = []
        self.flow_tar_file_save_paths = []

        self.rgb_tar_file_names = []
        self.rgb_tar_file_paths = []
        self.rgb_tar_file_save_paths = []

    def process(self, modalities=['flow', 'rgb']):
        self.search_tar_files(frames_rgb_flow_path)
        for m in modalities:
            self.untar_files(m)

    def search_tar_files(self, frames_rgb_flow_path):
        for m in ['flow', 'rgb']:
            for split in ['test', 'train']:
                current_path = os.path.join(
                    self.frames_rgb_flow_path, m, split)
                for path, subdirs, files in os.walk(current_path):
                    for _p, s, f in os.walk(path):
                        for _f in f:
                            if(_f.endswith('.tar')):
                                f_name = os.path.splitext(_f)[0]
                                _tar_file_save_path = os.path.join(_p, f_name)
                                if m == 'flow':
                                    self.flow_tar_file_names.append(_f)
                                    self.flow_tar_file_paths.append(_p)
                                    self.flow_tar_file_save_paths.append(
                                        _tar_file_save_path)
                                else:
                                    self.rgb_tar_file_names.append(_f)
                                    self.rgb_tar_file_paths.append(_p)
                                    self.rgb_tar_file_save_paths.append(
                                        _tar_file_save_path)

    def untar_files(self, modality):
        print(f"### {modality}")
        if modality == 'flow':
            _tar_file_names = self.flow_tar_file_names
            _tar_file_paths = self.flow_tar_file_paths
            _tar_file_save_paths = self.flow_tar_file_save_paths
        else:
            _tar_file_names = self.rgb_tar_file_names
            _tar_file_paths = self.rgb_tar_file_paths
            _tar_file_save_paths = self.rgb_tar_file_save_paths

        progress_bar = tqdm.tqdm(
            range(len(_tar_file_names)))
        for i in progress_bar:

            progress_bar.set_description(
                f"Extracting [{i + 1}/{len(_tar_file_names)}]")

            current_arq_path = os.path.join(
                _tar_file_paths[i], _tar_file_names[i])

            my_tar = tarfile.open(current_arq_path)
            # specify which folder to extract to
            my_tar.extractall(_tar_file_save_paths[i])
            my_tar.close()


if __name__ == "__main__":

    frames_rgb_flow_path = ''
    if args.p is None:
        ROOT_PATH = os.path.abspath(os.getcwd())
        frames_rgb_flow_path = os.path.join(ROOT_PATH, 'frames_rgb_flow')
    else:
        frames_rgb_flow_path = args.p
    print(f"Extracting files from the folder: {frames_rgb_flow_path}")
    d = ExtractionClass(frames_rgb_flow_path)
    if args.m is None:
        d.process()
    else:
        if args.m == 'flow':
            d.process(modalities=['flow'])
        else:
            d.process(modalities=['rgb'])
