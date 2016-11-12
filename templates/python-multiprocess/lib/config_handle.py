#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: __AUTHOR__
#########################################################################
# Created Time: __CREATE_DATETIME__ 
# File Name: config_handle.py
# Description: 
#########################################################################

import sys
from ConfigParser import ConfigParser

class ConfigHandle(object):

	def reload(self, file):
		self._cfg_parser = ConfigParser()
		self._cfg_parser.read(file)

		for section in self._cfg_parser.sections():
			for option, value in self._cfg_parser.items(section):
				if not hasattr(self, section):
					self.__dict__[section] = {}
				self.__dict__[section].update({option: value})

cnf = ConfigHandle()

# vim: set noexpandtab ts=4 sts=4 sw=4 :
