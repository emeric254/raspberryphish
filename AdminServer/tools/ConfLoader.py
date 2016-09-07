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


def load_cookie_conf():
    """Load configuration from 'configuration.conf' file

    :return: cookie_expiration, cookie_secret

    """
    config = configparser.ConfigParser()
    config.read('configuration.conf')  # load configuration from 'configuration.conf' file
    if 'COOKIE' not in config:
        raise ValueError('Please verify your configuration file contains a [COOKIE] section')
    if 'cookie_expiration' not in config['COOKIE'] or 'cookie_secret' not in config['COOKIE']:
        raise ValueError('Please verify [COOKIE] section of your configuration file')
    cookie_expiration = 1  # default is 1 day (24 hours)
    try:
        cookie_expiration = int(config['COOKIE']['cookie_expiration'])
    except ValueError:
        logging.warning('Invalid configuration : cookie_expiration. Set it to default duration of 1 day.')
    cookie_secret = config['COOKIE']['cookie_secret']  #
    if len(cookie_secret) < 1:  # empty cookie_secret value result in an automatic generation at app boot
        logging.info('No configuration : cookie_secret. Generating random secret.')
        cookie_secret = ''.join([random.choice(string.printable) for _ in range(32)])
    return cookie_expiration, cookie_secret


def load_login_conf():
    """Load configuration from 'configuration.conf' file

    :return: login, password, max_attempts, blocked_duration

    """
    config = configparser.ConfigParser()
    config.read('configuration.conf')  # load configuration from 'configuration.conf' file
    if 'LOGIN' not in config:
        raise ValueError('Please verify your configuration file contains a [LOGIN] section')
    if 'login' not in config['LOGIN'] or 'password' not in config['LOGIN'] \
            or 'max_attempts' not in config['LOGIN']or 'blocked_duration' not in config['LOGIN']:
        raise ValueError('Please verify [LOGIN] section of your configuration file')
    login = config['LOGIN']['login']  #
    password = config['LOGIN']['password']  #
    max_attempts = 5  # default is 5 attemps before blocking user
    try:
        max_attempts = int(config['LOGIN']['max_attempts'])
    except ValueError:
        logging.warning('Invalid configuration : max_attemps. Set it to default value of 5 attemps.')
    blocked_duration = 24  # default is 1 day (24 hours)
    try:
        blocked_duration = int(config['LOGIN']['blocked_duration'])
    except ValueError:
        logging.warning('Invalid configuration : blocked_duration. Set it to default duration of 24 hours.')
    if not login or not password or len(login) < 1 or len(password) < 6 or blocked_duration < 1 or max_attempts < 1:
        logging.error('Invalid configuration : Please verify configuration values in [LOGIN] section')
        raise ValueError('Please verify values in [LOGIN] section')  # invalid configuration
    return login, password, max_attempts, blocked_duration


def load_conf():
    """Load configuration from a file

    :return: login, password, cookie_secret, debug, autoreload, max_attemps, blocked_duration

    """
    config = configparser.ConfigParser()  # load configuration
    config.read('configuration.conf')  # load configuration from 'configuration.conf' file
    # missing section ?
    if 'MAIN' not in config:
        logging.error('Invalid configuration : Please verify [configuration.conf] contains a [MAIN] section')
        raise ValueError('Please verify [configuration.conf] contains a [MAIN] section')
    debug = False  # test not in debug mode
    if 'debug' in config['MAIN']:
        if isinstance(config['MAIN']['debug'], bool):
            debug = config['MAIN']['debug']
        else:
            logging.warning('Invalid configuration : debug. Continue without debug.')
    autoreload = False  # test no app autoreload
    if 'autoreload' in config['MAIN']:
        if isinstance(config['MAIN']['autoreload'], bool):
            autoreload = config['MAIN']['autoreload']
        else:
            logging.warning('Invalid configuration : autoreload. Continue without autoreload.')
    return debug, autoreload
