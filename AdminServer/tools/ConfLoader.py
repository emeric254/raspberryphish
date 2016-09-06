# -*- coding: utf-8 -*-

import configparser
import random
import string
import logging


def load_server_conf():
    """Load configuration from 'configuration.conf' file

    :return: cert_path, https_port

    """
    config = configparser.ConfigParser()
    config.read('configuration.conf')  # load configuration from 'configuration.conf' file
    if 'SERVER' not in config:
        raise ValueError('Please verify your configuration file contains a [SERVER] section')
    if 'https_port' not in config['SERVER'] or 'cert_folder_path' not in config['SERVER']:
        raise ValueError('Please verify [SERVER] section of your configuration file')
    cert_path = config['SERVER']['cert_folder_path']  # directory name where crt and key files are present
    https_port = config['SERVER']['https_port']  # HTTPS port to bind
    return cert_path, https_port


def load_conf(conf_file: str = 'configuration.conf'):
    """Load configuration from a file

    :param conf_file: the file to load
    :return: https_port, login, password, cookie_secret, debug, autoreload

    """
    config = configparser.ConfigParser()  # load configuration
    config.read(conf_file)  # load configuration from 'configuration.conf' file
    # missing section ?
    if 'MAIN' not in config:
        logging.error('Invalid configuration : Please verify [configuration.conf] contains a [MAIN] section')
        raise ValueError('Please verify [configuration.conf] contains a [MAIN] section')
    # missing a value ?
    if 'login' not in config['MAIN'] or 'password' not in config['MAIN'] or 'cookie_secret' not in config['MAIN']:
        logging.error('Invalid configuration : Please verify [MAIN] section in [configuration.conf]')
        raise ValueError('Please verify [MAIN] section in [configuration.conf]')
    # get configuration values
    login = config['MAIN']['login']  # login for admin
    password = config['MAIN']['password']  # password for admin
    cookie_secret = config['MAIN']['cookie_secret']  # hash to create cookies
    if len(cookie_secret) < 1:  # empty cookie_secret value result in an automatic generation at app boot
        logging.info('No configuration : cookie_secret. Generating random secret.')
        cookie_secret = ''.join([random.choice(string.printable) for _ in range(24)])
    # load debug value
    debug = False  # test not in debug mode
    if 'debug' in config['MAIN']:
        if isinstance(config['MAIN']['debug'], bool):
            debug = config['MAIN']['debug']
        else:
            logging.warning('Invalid configuration : debug. Continue without debug.')
    # load autoreload value
    autoreload = False  # test no app autoreload
    if 'autoreload' in config['MAIN']:
        if isinstance(config['MAIN']['autoreload'], bool):
            autoreload = config['MAIN']['autoreload']
        else:
            logging.warning('Invalid configuration : autoreload. Continue without autoreload.')
    # load max attemps value
    max_attemps = 5  # test 5 attemps before blocking user
    if 'max_attemps' in config['MAIN']:
        try:
            max_attemps = int(config['MAIN']['max_attemps'])
        except ValueError:
            logging.warning('Invalid configuration : max_attemps. Continue with a test value of 5 attemps.')
    # load blocked duration value
    blocked_duration = 24  # test 1 day
    if 'blocked_duration' in config['MAIN']:
        try:
            blocked_duration = int(config['MAIN']['blocked_duration'])
        except ValueError:
            logging.warning('Invalid configuration : blocked_duration. Continue with a test duration of 24 hours.')
    # invalid configuration ?
    if not login or not password or not cookie_secret \
            or len(login) < 1 or len(password) < 6 or len(cookie_secret) < 6 \
            or blocked_duration < 1 or max_attemps < 1:
        logging.error('Invalid configuration : Please verify configuration values in [configuration.conf]')
        raise ValueError('Please verify values in [configuration.conf]')
    return login, password, cookie_secret, debug, autoreload, max_attemps, blocked_duration
