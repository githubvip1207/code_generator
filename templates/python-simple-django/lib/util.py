#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: __AUTHOR__
#########################################################################
# Created Time: __CREATE_DATETIME__ 
# File Name: util.py
# Description: 
#########################################################################

import os
import sys
import logging

# 获取默认的运行时路径，并设置运行时需要加到sys.path的模块
basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basePath)

from lib.config_handle import cnf as Cnf


class Util:

	def __init__(self):
		self.logger = logging.getLogger()

util = Util()

# vim: set noexpandtab ts=4 sts=4 sw=4 :
