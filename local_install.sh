#!/usr/bin/env bash
#apt-get install -y python python-pip
SCRIPT_DIR=$(dirname $(readlink -e $0))
rm -rf *.egg-info build dist
pip uninstall -y tool
python setup.py install
