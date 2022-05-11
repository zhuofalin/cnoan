#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: zhuofalin
@contact:1822643111@qq.com
@version: 1.0.0
@license: Apache Licence
@file: utils.py
@time: 2022/5/9 15:07
"""
import logging
import pathlib
import time

from pkg_resources import resource_stream
from ruamel.yaml import YAML

yaml = YAML()


def get_default_config(stream_args: list = None) -> dict:
    if stream_args is None:
        # stream_args = ['cnoan', 'config.yaml']
        stream_args = ['cnoan', 'config.yaml']

    with resource_stream(*stream_args) as stream:
        return yaml.load(stream)


def get_logger(name: str = 'cnoan', level: str = 'info') -> logging.Logger:
    logger = logging.Logger(name=name)
    level_dict = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    logger.setLevel(level_dict[level])

    if not logger.handlers:
        log_path = log_path_utils()
        fh = logging.FileHandler(log_path)
        fh.setLevel(logging.INFO)

        fh_fmt = logging.Formatter('%(asctime)-15s %(filename)s %(levelname)s %(lineno)d: %(message)s')
        fh.setFormatter(fh_fmt)

        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console_fmt = logging.Formatter('%(filename)s %(levelname)s %(lineno)d: %(message)s')
        console.setFormatter(console_fmt)

        logger.addHandler(fh)
        logger.addHandler(console)
    return logger


def log_path_utils(name: str = 'cnoan') -> str:
    day = time.strftime('%Y-%m-%d', time.localtime())
    log_path = pathlib.Path(f'./log/{day}')
    if not log_path.exists():
        log_path.mkdir(parents=True)
    return f'{str(log_path)}/{name}.log'
