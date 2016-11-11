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

from lib import torndb
from lib.config_handle import cnf as Cnf


class Util:

	def __init__(self):
		self.logger = logging.getLogger()
		self.db = None

	def connectDb(self):
		self.db = torndb.Connection(
			host = '%s:%s' % (Cnf.database_master['host'], 
				Cnf.database_master['port']),
			database = Cnf.database_master['name'],
			user = Cnf.database_master['user'],
			password = Cnf.database_master['pawd']
			)

	def closeDb(self):
		try:
			self.db.close()
		except Exception, e:
			pass

util = Util()

# vim: set noexpandtab ts=4 sts=4 sw=4 :
