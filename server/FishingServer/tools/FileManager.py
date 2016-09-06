# -*- coding: utf-8 -*-

import os


def ensure_existence(folder: str):
    """Create a folder if it does not exist

    :param folder: foloder to ensure existence

    """
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)  # make this folder and all its parent if necessary
        except OSError:
            pass  # TODO logging already existent


def append_to_file(file_path: str, content: str):
    """Append some content to a file

    :param file_path:
    :param content:

    """
    ensure_existence(os.path.dirname(file_path))
    try:
        with open(file_path, mode='a', encoding='UTF-8') as file:
            file.write(content)
    except IOError:
        pass  # TODO logging write error
