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
import time
import signal
import logging
import argparse
import setproctitle
import ConfigParser
import logging.config
#import multiprocessing
import django

# 获取默认的运行时路径，并设置运行时需要加到sys.path的模块
basePath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basePath)

from lib.util import util as Util
from conf.__PROJECTNAME___config import cnf  as Cnf


class __PROJECTNAME_CLASS__(object):

	def __init__(self):
		# 正常的运行时日志Logger
		self.logger = logging.getLogger()
		self.executeDir = Cnf.basic['execute_dir']
		self.running = False
		self.initSignalHandler()

		Util.setCnf(Cnf)
		setproctitle.setproctitle('__PROJECTNAME__: master process')

	# 删除不需要处理的信号，以及增加需要处理的信号
	# 并且设置不同的处理方法
	# 这里默认处理了SIGTERM和SIGINT，并且尝试停止service
	# SIGINT = 2，可使用kill -2 pid 或 当CTRL+C终止程序时发出
	# SIGTERM = 15，可使用kill -15 pid发出
	def initSignalHandler(self):
		signals = (signal.SIGTERM, signal.SIGINT)
		self.signalHandlers = {}
		for sig in signals:
			self.signalHandlers[sig] = signal.getsignal(sig)
			signal.signal(sig, self.handleSignal)

	def handleSignal(self, signal, frame):
		self.logger.info('Handle signal %d, stop service', signal)
		self.logger.info('Try to stop all workers.')
		self.stop()
		self.logger.info('Bye-bye.')
		sys.exit(0)

	def run(self):
		self.logger.info('__PROJECTNAME__ service starts to run.')
		self.running = True
		# 方案一，轮训任务
		'''
		while self.running:
			self.logger.info('I\'m running')
			# 使用django连接数据库,所以这里废弃
			# Util.connectDb()
			# do something as your wish
			time.sleep(Cnf.basic['interval'])
		'''
		# 方案二、多进程任务
		'''
		from src.model1 import Model1 
		self.model1_processor = Model1()
		model1_thread = multiprocessing.Process(target = self.model1_processor.run, args = ())
		model1_thread.daemon = True
		model1_thread.start()

		# join
		model1_thread.join()
		'''

	def stop(self):
		self.logger.info('__PROJECTNAME__ service will stop.')
		# 方案二需要开启
		'''
		self.model1_processor.stop()
		'''
		self.running = False	


if __name__ == '__main__':
	# 命令行参数解析，默认解析'-d'，即指定该模块的运行时目录
	ap = argparse.ArgumentParser(description = '__PROJECTNAME__ service')
	ap.add_argument('-d', '--executeDir', type = str,
		help = '__PROJECTNAME__ service execute directory',
		default = basePath)
	args = ap.parse_args()
	print 'Run __PROJECTNAME__ service at %s' % args.executeDir
	os.chdir(args.executeDir)

	# 读取项目的配置，包括模块自身的基本配置，日志模块配置等
	# logging config
	print 'Load logging config...'
	logging.config.fileConfig(os.path.join(args.executeDir, 'conf/__PROJECTNAME___logging.cfg'))
	# __PROJECTNAME__ service config
	print 'Load __PROJECTNAME__ service config...'
	#cfg = ConfigParser.RawConfigParser()
	#cfg.read(os.path.join(args.executeDir, 'conf/__PROJECTNAME___config.cfg'))
	Cnf.reload(os.path.join(args.executeDir, 'conf/__PROJECTNAME___config.cfg'))
	Cnf.basic['execute_dir'] = args.executeDir

	# Let's rock 'n roll!
	__PROJECTNAME_CLASS__().run()

# vim: set noexpandtab ts=4 sts=4 sw=4 :
