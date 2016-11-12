#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Author: __AUTHOR__
#########################################################################
# Created Time: __CREATE_DATETIME__ 
# File Name: __PROJECTNAME__.py
# Description: 
#########################################################################

import os 
import sys 
import logging
import threading
import setproctitle

# 获取默认的运行时路径，并设置运行时需要加到sys.path的模块
basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basePath)

from lib.config_handle import cnf as Cnf
from lib.util import util as Util


class Model1(object):
	def __init__(self):
		self.logger = logging.getLogger(self.__class__.__name__)
		self.__running = False
		self.loopInterval = int(Cnf.basic['loop_interval'])
		setproctitle.setproctitle('__PROJECTNAME__: worker process[model1]')

	def listener(self):
		while self.__running:
			if self.queue.get() == 'stop':
				self.__running = False
				self.logger.info('__PROJECTNAME__.model1 will stop. please wait...')
			time.sleep(1)

	def startup(self, queue):
		self.queue = queue
		self.__running = True
		t = threading.Thread(target = self.listener, args = ())
		t.start()
		self.run()

	def run(self):
		while self.running:
			self.logger.info('I\'m running')
			Util.db.reconnect()
			# do something as your wish
			time.sleep(self.loopInterval)


# vim: set noexpandtab ts=4 sts=4 sw=4 :
