#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: __AUTHOR__
#########################################################################
# Created Time: __CREATE_DATETIME__ 
# File Name: __PROJECTNAME___config.py
# Description: 
#########################################################################

import sys
from ConfigParser import ConfigParser

class __PROJECTNAME_CLASS___config(object):

	def reload(self, file):
		self.__cfg_parser = ConfigParser()
		self.__cfg_parser.read(file)

		self.basic = {
			'execute_dir' : '',
			'interval' : self.__cfg_parser.getint('basic', 'interval'),
		}

		self.database_master = {
			'host' : self.__cfg_parser.get('database_master', 'host'),
			'port' : self.__cfg_parser.getint('database_master', 'port'),
			'name' : self.__cfg_parser.get('database_master', 'name'),
			'user' : self.__cfg_parser.get('database_master', 'user'),
			'pawd' : self.__cfg_parser.get('database_master', 'pawd'),
		}

		self.database_slave = {
			'host' : self.__cfg_parser.get('database_slave', 'host'),
			'port' : self.__cfg_parser.getint('database_slave', 'port'),
			'name' : self.__cfg_parser.get('database_slave', 'name'),
			'user' : self.__cfg_parser.get('database_slave', 'user'),
			'pawd' : self.__cfg_parser.get('database_slave', 'pawd'),
		}

cnf = __PROJECTNAME_CLASS___config()

# vim: set noexpandtab ts=4 sts=4 sw=4 :
