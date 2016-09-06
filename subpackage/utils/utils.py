#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import yaml
from colorama import Fore, Back


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
VERBOSE = False


def verbose(msg):
    if VERBOSE:
        print msg


def error(msg):
    print Fore.RED + msg
    sys.exit(-1)


def read_credential_from_disk():
    conf_path = os.path.expanduser('~/.k2')
    credential_file = os.path.join(conf_path, 'kip.yaml')
    if not os.path.exists(conf_path):
        os.mkdir(conf_path)
    if not os.path.exists(credential_file):
        print Fore.RED + "Missing credential file %s" % credential_file
        error('run \'k2 config\' first')

    conf = yaml.load(open(credential_file))

    user = conf.get('user', None)
    if user is None:
        error('Missing field user')
    password = conf.get('password', None)
    if password is None:
        error('Missing field password')
    return user, password


def ask_for_input(prompt, default_value, value_type=str, value_checker=None, check_failed_message='Invalid input'):
    value_type = int if value_type == int else str
    result = None
    while result is None:
        result = raw_input("%s [%s]" % (prompt, default_value))
        try:
            result = default_value if result == '' else value_type(result)
        except Exception:
            print 'Can not cast %s to %s' % (result, value_type)
            result = None
            continue
        if value_checker and not value_checker(result):
            print check_failed_message
            result = None
    return result
