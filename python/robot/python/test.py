#!/usr/bin/python   
# -*- coding: utf-8 -*-   
import time
import socket
from locust import Locust, TaskSet, events, task, seq_task,TaskSequence

import login
import mylib
import sys
import struct
#cmd = "PlayerVerifyVerLoginClientCmd_C"
#cmd = "PlayerVerifyVerLoginClientCmd_S"
#print(Command_py.Command_pb2.CmdNumber.Name(1))
#print(Command_py.Command_pb2.CmdNumber.Value('ClientCmdNone'))
#print(Command_py.Command_pb2.CmdNumber.Value(cmd))

#print(cmd.split('_')[0])
#print(cmd)

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
	reload(sys)
	sys.setdefaultencoding(defaultencoding)

class TcpSocketClient(socket.socket):
	def __init__(self, af_inet, socket_type):
		super(TcpSocketClient, self).__init__(af_inet, socket_type)

	def connect(self, addr):
		start_time = time.time()
		try:
			super(TcpSocketClient, self).connect(addr)
		except Exception as e:
			total_time = int((time.time() - start_time) * 1000)
			events.request_failure.fire(request_type="tcpsocket", name="connect", response_time=total_time, exception=e)
		else:
			total_time = int((time.time() - start_time) * 1000)
			events.request_success.fire(request_type="tcpsocket", name="connect", response_time=total_time,response_length=0)

	def close(self):
		start_time = time.time()
		try:
			super(TcpSocketClient, self).close()
		except Exception as e:
			total_time = int((time.time() - start_time) * 1000)
			events.request_failure.fire(request_type="tcpsocket", name="close", response_time=total_time, exception=e)
		else:
			total_time = int((time.time() - start_time) * 1000)
			events.request_success.fire(request_type="tcpsocket", name="close", response_time=total_time,response_length=0)

	def send(self, msg):
		start_time = time.time()
		try:
			super(TcpSocketClient, self).send(msg)
		except Exception as e:
			total_time = int((time.time() - start_time) * 1000)
			events.request_failure.fire(request_type="tcpsocket", name="send", response_time=total_time, exception=e)
		else:
			total_time = int((time.time() - start_time) * 1000)
			events.request_success.fire(request_type="tcpsocket", name="send", response_time=total_time,response_length=0)

	def recv(self, bufsize):
		recv_data = ''
		start_time = time.time()
		try:
			recv_data = super(TcpSocketClient, self).recv(bufsize)
		except Exception as e:
			total_time = int((time.time() - start_time) * 1000)
			events.request_failure.fire(request_type="tcpsocket", name="recv", response_time=total_time, exception=e)
		else:
			total_time = int((time.time() - start_time) * 1000)
			events.request_success.fire(request_type="tcpsocket", name="recv", response_time=total_time,response_length=0)
		return recv_data

	def setlogininfo(self,account_id,login_id,version):
		self.account_id = account_id
		self.login_id = login_id
		self.version = version

	def getlogininfo(self):
		return self.account_id,self.login_id,self.version

class VerifyVerLogin(TaskSequence):

	def on_start(self):
		print("------start------")

	@seq_task(1)
	def test1(self):
		print("-------1-------")

	@seq_task(2)
	def test2(self):
		print("-------2-------")

	@seq_task(3)
	@task
	def test3(self):
		print("-------3------")

	@seq_task(3)
	@task
	def test4(self):
		print("-------4-------")

	@seq_task(3)
	@task
	def test5(self):
		print("-------5-------")

class PlayerVerifyVerLogin(Locust):

	min_wait = 100
	max_wait = 1000
	task_set = VerifyVerLogin
	
	
if __name__ == "__main__":
	user = PlayerVerifyVerLogin()
	user.run()
	
