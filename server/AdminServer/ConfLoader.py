# -*- coding: utf-8 -*-

import configparser
import random
import string
import logging


def load_conf(conf_file: str = 'configuration.conf'):
    """Load configuration from a file

    :param conf_file: the file to load
    :return: https_port, login, password, cookie_secret, debug, autoreload
    """
    # load configuration
    config = configparser.ConfigParser()
    config.read(conf_file)  # load configuration from 'configuration.conf' file
    # missing section ?
    if 'SERVER' not in config:
        logging.error('Invalid configuration : Please verify [configuration.conf] contains a [SERVER] section')
        raise ValueError('Please verify [configuration.conf] contains a [SERVER] section')
    # missing a value ?
    if 'https_port' not in config['SERVER'] or 'login' not in config['SERVER'] \
            or 'password' not in config['SERVER'] or 'cookie_secret' not in config['SERVER']:
        logging.error('Invalid configuration : Please verify [SERVER] section in [configuration.conf]')
        raise ValueError('Please verify [SERVER] section in [configuration.conf]')
    # get configuration values
    https_port = config['SERVER']['https_port']  # HTTPS port to bind
    login = config['SERVER']['login']  # login for admin
    password = config['SERVER']['password']  # password for admin
    cookie_secret = config['SERVER']['cookie_secret']  # hash to create cookies
    if len(cookie_secret) < 1:
        cookie_secret = ''.join([random.choice(string.printable) for _ in range(24)])
    debug = False
    if 'debug' in config['SERVER'] and isinstance(config['SERVER']['debug'], bool):
        debug = config['SERVER']['debug']
    autoreload = False
    if 'autoreload' in config['SERVER'] and isinstance(config['SERVER']['autoreload'], bool):
        autoreload = config['SERVER']['autoreload']
    # invalid configuration ?
    if not https_port or not login or not password or not cookie_secret \
            or int(https_port) < 1 or int(https_port) > 65535 \
            or len(login) < 1 or len(password) < 1 or len(cookie_secret) < 1:
        logging.error('Invalid configuration : Please verify configuration values in [configuration.conf]')
        raise ValueError('Please verify values in [configuration.conf]')
    return https_port, login, password, cookie_secret, debug, autoreload
