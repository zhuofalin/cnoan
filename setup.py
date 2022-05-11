#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhuofalin
@contact:1822643111@qq.com
@version: 1.0.0
@license: Apache Licence
@file: setup.py
@time: 2022/5/10 9:54
"""

import os
import sys
from setuptools import setup, find_packages

NAME = 'cnoan'
AUTHOR = 'zhuofalin'
EMAIL = '1822643111@qq.com'
URL = 'https://github.com/zhuofalin/cnoan.git'
LICENSE = "MIT License"
DESCRIPTION = "Convert Chinese numerals and Arabic numerals."

if sys.version_info < (3, 6, 0):
    raise RuntimeError(f'{NAME} requires Python >=3.6.0, but yours is {sys.version}!')

try:
    lib_py = os.path.join(NAME, '__init__.py')
    with open(lib_py, 'r', encoding='utf8') as f_v:
        v_line = ""
        for line in f_v.readlines():
            if line.startswith('__version__'):
                v_line = line.strip()
                break
        exec(v_line)  # get __version__ from __init__.py
except FileNotFoundError:
    __version__ = '0.0.0'

if __name__ == '__main__':
    __version__ = '1.1.1'
    setup(
        name=NAME,
        version=__version__,
        author=AUTHOR,
        url=URL,
        author_email=EMAIL,
        license=LICENSE,
        description=DESCRIPTION,
        packages=find_packages(),
        include_package_data=True,
        install_requires=open('./requirements.txt', "r", encoding="utf-8").read().splitlines(),
        long_description=open('./README.md', "r", encoding="utf-8").read(),
        long_description_content_type='text/markdown',
        zip_safe=True,
        classifiers=[
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            "Programming Language :: Python :: 3.8",
            f"License :: OSI Approved :: {LICENSE}",
            'Operating System :: OS Independent',
        ],
        python_requires=">=3.6"
    )
