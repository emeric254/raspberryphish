# -*- coding: utf-8 -*-

import os
import logging


def del_recursive_folder(folder: str):
    """Delete a folder content before itself.

    :param folder: folder to delete

    """
    logging.info('deleting folder : ' + folder)
    for root, folders, files in os.walk(folder):
        for temp in files:
            path = os.path.join(root, temp)
            logging.debug('delete file : ' + path)
            os.remove(path)
        for temp in folders:
            path = os.path.join(root, temp)
            logging.debug('delete folder : ' + path)
            os.rmdir(path)
    os.rmdir(folder)


def del_folder(folder: str):
    """Delete a folder.

    :param folder: folder to delete

    """
    logging.info('deleting folder : ' + folder)
    os.rmdir(folder)
