# -*- coding:utf-8 -*-
"""
@file： install.py
@description: 安装头文件和lib
@author: 635672377@qq.com
@date：2023/11/28
"""

import os
import shutil
import sys


class App:
	def __init__(self, solution_dir, mode, platform):
		self.header_files = []
		self.log_dir = ['crash_generation_client', 'crash_generation_server', 'crash_report_sender']
		self.root_dir = solution_dir
		self.compile_mode = mode
		self.compile_platform = platform

	# @property
	# def root_dir(self):
	# 	cur_dir = os.getcwd()
	# 	parent_dir, child_dir = os.path.split(cur_dir)
	# 	print('------------root_dir------------------')
	# 	print(parent_dir)
	# 	print('------------root_dir------------------')
	# 	return parent_dir

	# @property
	# def src_dir(self):
	# 	return self.root_dir + '\\src\\'
	#
	@property
	def install_dir(self):
		return self.root_dir + '/install_windows/'

	@property
	def win_file_path(self):
		win_path = self.root_dir + self.compile_mode + '/' + self.compile_platform + '/'
		return win_path

	def read_log(self):
		for log_name in self.log_dir:
			log_path = self.win_file_path + 'obj/' + log_name + '/' + log_name + '.log'
			if not os.path.exists(log_path):
				print('[warning] not find {}'.format(log_path))
				return
			with open(log_path, 'r', encoding='utf-8') as file:
				content = file.readline()
				target_str = '注意: 包含文件:'
				while content:
					content = content.strip()
					if target_str in content:
						content = content.replace(target_str, '').strip()
						if not content.startswith('C:'):
							self.header_files.append(content)
					content = file.readline()

	def intall_headers(self):
		"""
		1、lib文件
		2、头文件
		:return:
		"""
		parent_dir, _ = os.path.split(self.root_dir)
		client_src, _ = os.path.split(parent_dir)
		src_dir, _ = os.path.split(client_src)
		src_dir += '\\'
		dest_install_dir = self.install_dir + '/include'
		for file in self.header_files:
			part_path = file.replace(src_dir, '')
			dest_file_path = dest_install_dir + '\\' + part_path
			dir_name = os.path.dirname(dest_file_path)
			if not os.path.exists(dir_name):
				os.makedirs(dir_name)
			shutil.copy(file, dest_file_path)

	def install_libs(self):
		# 1、源lib目录
		source_lib_path = self.win_file_path + 'lib/'
		# 2、目标lib目录
		dest_libs_path = self.install_dir + '/lib/' + self.compile_mode + '/' + self.compile_platform + '/'
		if not os.path.exists(dest_libs_path):
			os.makedirs(dest_libs_path)
		libs_name = ['common.lib', 'crash_generation_client.lib', 'crash_generation_server.lib', 'crash_report_sender.lib', 'exception_handler.lib']
		for lib in libs_name:
			lib_path = source_lib_path+lib
			if os.path.exists(lib_path):
				shutil.copy(lib_path, dest_libs_path+lib)


if __name__ == "__main__":
	# sys.argv[1] -> solution dir sys.argv[2] -> mode sys.argv[3] -> platform
	if len(sys.argv) == 4:
		print('-------------install started---------------')
		app = App(sys.argv[1], sys.argv[2], sys.argv[3])
		app.read_log()
		app.intall_headers()
		app.install_libs()
		print('install path:{}'.format(app.install_dir))
		print('-------------install finished---------------')
	else:
		print('-------------install started---------------')
		app = App('E:\\my_document\\platypus\\3rdparty\\breakpad\\src\\client\\windows\\', 'Debug', 'Win32')
		app.read_log()
		app.intall_headers()
		app.install_libs()
		print('install path:{}'.format(app.install_dir))
		print('-------------install finished---------------')

