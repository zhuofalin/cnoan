#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhuofalin
@contact:1822643111@qq.com
@version: 1.0.0
@license: Apache Licence
@file: __init__.py
@time: 2022/5/10 9:50
"""
__version__ = '0.1.1'

from .cn2an import CN2ArabicNumerals as Cn2An
from .an2cn import ArabicNumerals2CN as An2Cn
from .translate import Translate

cn2an = Cn2An().convert
an2cn = An2Cn().convert
translate = Translate().convert

__all__ = [
    '__version__',
    'cn2an',
    'an2cn',
    'translate'
]