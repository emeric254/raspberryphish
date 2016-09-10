# -*- coding: utf-8 -*-

import logging
import configparser


def load_server_conf():
    """Load configuration from 'configuration.conf' file.

    :return: cert_path, http_port, https_port

    """
    config = configparser.ConfigParser()
    config.read('configuration.conf')  # load configuration from 'configuration.conf' file
    logging.info('Loading Server related configuration')
    if 'SERVER' not in config:
        logging.error('[SERVER] section of configuration is missing')
        raise ValueError('Please verify your configuration file contains a [SERVER] section')
    if 'http_port' not in config['SERVER'] or 'https_port' not in config['SERVER']\
            or 'cert_path' not in config['SERVER']:
        logging.error('At least a configuration field is missing')
        raise ValueError('Please verify [SERVER] section of your configuration file')
    cert_path = config['SERVER']['cert_path']  # directory name where the AdminServer will load cert and key files
    http_port = config['SERVER']['http_port']  # HTTP port to bind
    https_port = config['SERVER']['https_port']  # HTTPS port to bind
    return cert_path, http_port, https_port


def load_fish_conf():
    """Load configuration from 'configuration.conf' file.

    :return: page_path, rsc_path

    """
    config = configparser.ConfigParser()
    config.read('configuration.conf')  # load configuration from 'configuration.conf' file
    logging.info('Loading Fishing related configuration')
    if 'MAIN' not in config:
        logging.error('[MAIN] section of configuration is missing')
        raise ValueError('Please verify your configuration file contains a [MAIN] section')
    if 'website_name' not in config['MAIN'] or 'page_folder_path' not in config['MAIN'] \
            or 'rsc_folder_path' not in config['MAIN'] or 'dumps_folder_path' not in config['MAIN']:
        logging.error('At least a configuration field is missing')
        raise ValueError('Please verify [MAIN] section of your configuration file')
    website_name = config['MAIN']['website_name']   # website to load name
    page_folder_path = config['MAIN']['page_folder_path']  # parent directory where to find 'pages'
    rsc_folder_path = config['MAIN']['rsc_folder_path']  # parent directory where to find 'rsc'
    dumps_folder_path = config['MAIN']['dumps_folder_path']  # parent directory where dumps will be written
    return website_name, page_folder_path, rsc_folder_path, dumps_folder_path
