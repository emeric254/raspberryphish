# -*- coding: utf-8 -*-

import os
import logging


def ensure_existence(folder: str):
    """Ensure that a folder exist, if not it create it.

    :param folder: folder to ensure existence

    """
    logging.debug('Ensure folder existence of ' + folder)
    if not os.path.exists(folder):
        try:
            os.makedirs(folder)  # make this folder and all its parent if necessary
        except OSError:
            logging.warning('This folder already exist : ' + folder)
    elif not os.path.isdir(folder):
        logging.error('This is not a folder ' + folder)
        raise FileExistsError


def append_to_file(file_path: str, content: str):
    """Append some content to a file.

    :param file_path: file to append some content
    :param content: content to append to this file

    """
    ensure_existence(os.path.dirname(file_path))
    logging.debug('Trying to append some content to ' + file_path)
    try:
        with open(file_path, mode='a', encoding='UTF-8') as file:
            file.write(content)
    except IOError:
        logging.error('Can\'t write to ' + file_path)
