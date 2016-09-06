#!/usr/bin/env python
# -*- coding: utf-8 -*-

# from __future__ import print_function

import argparse
import logging
import sys

from colorama import init, Fore

init(autoreset=True)


def enable_debug():
    logging.getLogger().setLevel(logging.DEBUG)
    logging.debug("debug mode enabled")


# global variables
VERBOSE = False


def global_config(args):
    global VERBOSE
    if args.verbose:
        VERBOSE = True


def verbose(msg):
    if VERBOSE:
        print msg


def error(msg):
    print Fore.RED + msg
    sys.exit(-1)


class K2Platform:
    def __init__(self):
        self.client = None

    def foo(self, args):
        logging.debug('doing foo')
        pass

    def bar(self, args):
        logging.debug('doing bar')
        pass

    def kip_config(self, args):
        logging.debug("executing kip config")

    def kip_next(self, args):
        logging.debug("executing kip next")


class Cmdline:
    def __init__(self):
        pass

    @classmethod
    def cmdline(cls):
        k2platform = K2Platform()
        root_command_hierarchy = [
            'foo',
            'bar',
            ('kip', ['next', 'config']),
        ]
        root_parser = argparse.ArgumentParser(description='K2 docker operation CLI')
        root_parser.add_argument('-v', '--verbose', action='store_true', help='verbose')
        root_parser.add_argument('--debug', '-d', action='store_true', help='debug mode')
        args, others = root_parser.parse_known_args()
        if args.debug:
            enable_debug()
        cls.setup_parser(parser=root_parser, hierarchy=root_command_hierarchy, context=[], executor=k2platform)
        args = root_parser.parse_args()
        global_config(args)
        return args

    @classmethod
    def setup_parser(cls, parser, hierarchy, context, executor):
        if len(hierarchy) > 0:
            subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands',
                                               help='sub-commands')
            for c in hierarchy:
                if isinstance(c, str):
                    cmd_chain_array = list(context)  # foo_bar_zzz
                    cmd_chain_array.append(c)
                    cmd_chain = '_'.join(cmd_chain_array)
                    command_parser = subparsers.add_parser(c)
                    # here is the magic: if a command has no sub-command, we can determine the func serves that command
                    command_parser.set_defaults(func=getattr(K2Platform(), cmd_chain))
                    # set optional arguments
                    if hasattr(cls, cmd_chain):
                        getattr(cls, cmd_chain)(command_parser)
                elif isinstance(c, tuple):
                    cmd = c[0]
                    if not isinstance(cmd, str):
                        print 'Except str but got %s' % type(cmd)
                        continue
                    sub_hierarchy = c[1]
                    if not isinstance(sub_hierarchy, list):
                        print 'Except list but got %s' % type(cmd)
                        continue
                    cmd_chain_array = list(context)  # foo_bar_zzz
                    cmd_chain_array.append(cmd)
                    cmd_chain = '_'.join(cmd_chain_array)
                    command_parser = subparsers.add_parser(cmd)
                    # set optional arguments
                    getattr(cls, cmd_chain)(command_parser)
                    cls.setup_parser(parser=command_parser, hierarchy=sub_hierarchy, context=cmd_chain_array,
                                     executor=executor)
                else:
                    print 'Expect tuple but got %s' % type(c)
                    continue

    @classmethod
    def foo(cls, parser):
        logging.debug('setup arguments for foo')
        pass

    @classmethod
    def bar(cls, parser):
        pass

    @classmethod
    def kip(cls, parser):
        pass

    @classmethod
    def kip_next(cls, parser):
        pass

    @classmethod
    def kip_config(cls, parser):
        pass


def run():
    args = Cmdline.cmdline()
    logging.debug(args)
    args.func(args)


if __name__ == '__main__':
    run()
