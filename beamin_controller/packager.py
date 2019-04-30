import os
import fnmatch
import re
from zipfile import ZipFile
import json


class Packager():
    def __init__(self, root_path, zip_path='node.zip'):
        self.root = os.path.expanduser(root_path)
        self.zip_path = zip_path

        zip_file = ZipFile(self.zip_path, mode='w').close()

    def add_matching(self, includes, excludes=None, validate_json=True):
        """
        Heavily based on http://stackoverflow.com/questions/5141437/filtering-os-walk-dirs-and-files
        """
        if excludes is None:
            excludes = []

        includes = r'|'.join([fnmatch.translate(x) for x in includes])
        excludes = r'|'.join([fnmatch.translate(x) for x in excludes]) or r'$.'

        with ZipFile(self.zip_path, mode='a') as z:
            for root, dirs, files in os.walk(self.root):
                # exclude dirs
                dirs[:] = [os.path.join(root, d) for d in dirs]
                dirs[:] = [d for d in dirs if not re.match(excludes, d)]

                # exclude/include files
                files = [f for f in files if not re.match(excludes, f)]
                files = [f for f in files if re.match(includes, f)]

                for f in files:
                    file_path = os.path.join(root, f)

                    if validate_json and f.endswith('.json'):
                        try:
                            json.load(open(file_path))
                        except ValueError as error:
                            msg = '{} is not valid JSON. {}'.format(f, error)
                            raise ValueError(msg)

                    relative_path = os.path.relpath(root, self.root)
                    z.write(file_path, os.path.join(relative_path, f))
