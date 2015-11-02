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

from lib import mysql_util as MU


class Util:

	def __init__(self):
		self.logger = logging.getLogger()
		self.cnf = None
		self.conn = None

	def setCnf(self, cnf):
		self.cnf = cnf 

	def connectDb(self):
		self.closeDb()
		self.conn = MU.registerConnection('root',
			self.cnf.database['host'],
			self.cnf.database['port'],
			self.cnf.database['user'],
			self.cnf.database['pawd'],
			self.cnf.database['name']
			)

	def closeDb(self):
		try:
			MU.closeConnection('root', self.conn)
		except Exception, e:
			pass

util = Util()

# vim: set noexpandtab ts=4 sts=4 sw=4 :
