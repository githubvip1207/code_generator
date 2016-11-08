#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: __AUTHOR__
#########################################################################
# Created Time: __CREATE_DATETIME__ 
# File Name: DBRouter.py
# Description: 
#########################################################################

class DBRouter(object):

	def db_for_read(self, model, **hints):
		return 'slave'

	def db_for_write(self, model, **hints):
		return 'default'

	def allow_relation(self, obj1, obj2, **hints):
		return None

	def allow_syncdb(self, db, model):
		return None

# vim: set noexpandtab ts=4 sts=4 sw=4 :
