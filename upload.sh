#!/usr/bin/env bash
PKG_NAME=tool
PKG_FILE=${PKG_NAME}-0.0.1-py2.py3-none-any.whl
python setup.py bdist_wheel --universal
ssh ci2 mkdir -p /home/share/simple/${PKG_NAME}
scp dist/${PKG_FILE} ci2:/home/share/simple/${PKG_NAME}/
ssh ci2 chmod -R 755 /home/share/simple
echo "http://192.168.130.51/simple/k2-compose/${PKG_FILE}"
