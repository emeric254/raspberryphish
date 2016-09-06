# -*- coding: utf-8 -*-

import configparser
import logging


def load_server_conf():
    """Load configuration from 'configuration.conf' file

    :return: cert_path, http_port, https_port

    """
    # TODO add some logging
    config = configparser.ConfigParser()
    config.read('configuration.conf')  # load configuration from 'configuration.conf' file
    if 'SERVER' not in config:
        raise ValueError('Please verify your configuration file contains a [SERVER] section')
    if 'http_port' not in config['SERVER'] or 'https_port' not in config['SERVER']\
            or 'cert_path' not in config['SERVER']:
        raise ValueError('Please verify [SERVER] section of your configuration file')
    cert_path = config['SERVER']['cert_path']  # directory name where the server will load cert and key files
    http_port = config['SERVER']['http_port']  # HTTP port to bind
    https_port = config['SERVER']['https_port']  # HTTPS port to bind
    return cert_path, http_port, https_port


def load_fish_conf():
    """Load configuration from 'configuration.conf' file

    :return: page_path, rsc_path

    """
    # TODO add some logging
    config = configparser.ConfigParser()
    config.read('configuration.conf')  # load configuration from 'configuration.conf' file
    if 'MAIN' not in config:
        raise ValueError('Please verify your configuration file contains a [MAIN] section')
    if 'website_name' not in config['MAIN'] or 'page_folder_path' not in config['MAIN'] \
            or 'rsc_folder_path' not in config['MAIN'] or 'dumps_folder_path' not in config['MAIN']:
        raise ValueError('Please verify [MAIN] section of your configuration file')
    website_name = config['MAIN']['website_name']   # website to load name
    page_folder_path = config['MAIN']['page_folder_path']  # parent directory where to find 'pages'
    rsc_folder_path = config['MAIN']['rsc_folder_path']  # parent directory where to find 'rsc'
    dumps_folder_path = config['MAIN']['dumps_folder_path']  # parent directory where dumps will be written
    return website_name, page_folder_path, rsc_folder_path, dumps_folder_path


def load_log_conf():
    """Load configuration from 'configuration.conf' file

    :return: log_level, log_file

    """
    config = configparser.ConfigParser()
    config.read('configuration.conf')  # load configuration from 'configuration.conf' file
    if 'LOG' not in config:
        raise ValueError('Please verify your configuration file contains a [LOG] section')
    if 'log_level' not in config['LOG'] or 'log_file' not in config['LOG']:
        raise ValueError('Please verify [LOG] section of your configuration file')
    log_level = config['LOG']['log_level']   # log level
    log_file = config['LOG']['log_file']  # log file
    if log_level.lower() == 'debug':
        log_level = logging.DEBUG
    elif log_level.lower() == 'info':
        log_level = logging.INFO
    elif log_level.lower() == 'warning':
        log_level = logging.WARNING
    elif log_level.lower() == 'error':
        log_level = logging.ERROR
    elif log_level.lower() == 'critical':
        log_level = logging.CRITICAL
    else:
        log_level = logging.NOTSET
    return log_level, log_file
