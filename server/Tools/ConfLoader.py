# -*- coding: utf-8 -*-

import configparser


def load_server_conf():
    """Load configuration from 'configuration.conf' file

    :return: page_path, http_port, https_port
    """

    config = configparser.ConfigParser()
    config.read('configuration.conf')  # load configuration from 'configuration.conf' file

    if 'SERVER' not in config:
        raise ValueError('Please verify your configuration file contains a [SERVER] section')

    if 'page_path' not in config['SERVER'] \
            or 'http_port' not in config['SERVER'] \
            or 'https_port' not in config['SERVER']:
        raise ValueError('Please verify [SERVER] section of your configuration file')

    page_path = config['SERVER']['page_path']  # directory name where the server will load in 'pages' and 'static'
    http_port = config['SERVER']['http_port']  # HTTP port to bind
    https_port = config['SERVER']['https_port']  # HTTPS port to bind

    return page_path, http_port, https_port
