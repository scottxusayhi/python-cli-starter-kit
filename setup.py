#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
import setuptools

setup(name="tool",
      version='0.0.1',
      packages=[
          '',
          'subpackage',
          'subsubpackage',
      ],
      package_dir={
          '': '.',
          'subpackage': 'subpackage',
          'subsubpackage': 'subpackage/subsubpackage',
      },
      package_data={
          'subsubpackage': ['datafiles/*'],
      },
      include_package_data=True,
      description='Awesome Tool',
      author='Developer',
      author_email='developer@examplec.om',
      url='http://example.com',
      install_requires=[
          'colorama',
      ],
      entry_points={                                                             
          'console_scripts': [
            'tool=main:run',
            'tool-alias=main:run',
          ]
      }
      )
