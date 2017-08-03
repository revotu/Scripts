# -*- coding:utf-8 -*-

import os,sys,subprocess,commands
import requests
import logging


def use_logging(func):
    def wrapper():
        logging.warn("{} is running".format(func.__name__))
        return func()
    return wrapper


# @use_logging
def foo():
    print('I am foo')


foo = use_logging(foo)
foo()
print(dir())
print(globals())
print(locals())