#!/bin/env python3

import os
import sys
import argparse
import re
from shutil import copyfile


class DropboxDir():

    def __init__(self, directory):
        self.comp_exts = [".gz", ".rar"]
        self.exts = [".py"]
        self.file_rgx = re.compile("^([\w\s]+)\s-\s([\w\s.-]+)$")
        self.abs_path = os.path.abspath(directory)
        dir_contents = os.listdir(self.abs_path)
        self.file_md = self._get_file_md(dir_contents)
        if not self.file_md:
            raise Exception("No valid files found!")

    def _get_file_md(self, dir_contents):
        file_md = {}
        for filename in dir_contents:
            file_path = os.path.join(self.abs_path, filename)
            if os.path.isfile(file_path) and self._is_valid_file(filename):
                match = self.file_rgx.match(filename)
                groups = match.groups()
                file_id = groups[0]
                new_filename = groups[1]
                if file_id not in file_md:
                    file_md[file_id] = []
                metadata = {}
                metadata["old_path"] = os.path.join(file_path)
                metadata["new_path"] = os.path.join(self.abs_path,
                                                    "formated",
                                                    file_id,
                                                    new_filename)
                file_md[file_id].append(metadata)

        return file_md

    def _is_valid_file(self, filename):
        valid_exts = self.exts + self.comp_exts
        filename, exts = os.path.splitext(filename)
        match = self.file_rgx.match(filename)
        if exts in valid_exts and match:
            return True
        return False

    def copy_files(self):
        formated_dir = os.path.join(self.abs_path, "formated")
        if not os.path.exists(formated_dir):
            os.makedirs(formated_dir)
        for md_id, md in self.file_md.items():
            if not os.path.exists(os.path.join(formated_dir, md_id)):
                os.makedirs(os.path.join(formated_dir, md_id))
            for f in md:
                copyfile(f["old_path"], f["new_path"])


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dir",
                        help="Dropbox dir which needs to be formated!",
                        type=str)
    args = parser.parse_args()
    print(args.dir)
    ddir = DropboxDir(args.dir)
    ddir.copy_files()

if __name__ == "__main__":
    main(sys.argv[1:])
