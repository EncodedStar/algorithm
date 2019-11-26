#!/usr/bin/python   
# -*- coding: utf-8 -*-   
from datetime import datetime
import time
import socket
from locust import Locust, TaskSet, events, task, seq_task,TaskSequence

import login
import GMcmd
import Fb
import mylib
import sys
import struct

import Command_py.GameConfig_pb2
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
		#	events.request_failure.fire(request_type="tcpsocket", name="send", response_time=total_time, exception=e)
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
	client = None
	client2 = None
	#client2 = TcpSocketClient(socket.AF_INET, socket.SOCK_STREAM)
	name = ""
	sex = 0
	account = "hx10000"
	password = "123455"
	account_id = 0 
	login_id = 0 
	playerid = 0
	ip = ''
	port = 0
	version = '0.12.1.5'.encode('utf-8')
	fundict = {}

	PingTime = datetime.now()
	FbEnterFirst = True
	FbTime = datetime.now()

	def InitCallBack(self):
		login.InitCallBack()
		GMcmd.InitCallBack()
		Fb.InitCallBack()

	def on_start(self):
		config = Command_py.GameConfig_pb2.GameConfig()
		
		self.client = TcpSocketClient(socket.AF_INET, socket.SOCK_STREAM)
		#ADDR = ("94.191.102.152", 3000)
		ADDR = (config.ip, config.port)
		self.client.connect((ADDR))
		self.InitCallBack()
		self.setaccount()
		self.version = config.version
		self.client.send(login.PlayerVerifyVerLoginClient(config.game, config.zone, config.version))
		print(config.ip, config.port, config.game, config.zone, config.version)
		for num in range(1,10):
			try:
				(msgsize, msgNo) = struct.unpack('2H',self.client.recv(4))
				msg = self.client.recv(msgsize)
				f = mylib.UnpackData(msgsize, msgNo, msg)
				if self.fundict.has_key(f[0]) :
					self.fundict[f[0]](self,f)
					if f[0] == "ServerReturnLoginSuccessLoginClientCmd_S":
						break
			except:
				self.client.send(login.PlayerVerifyVerLoginClient(config.game, config.zone, config.version))
				
		self.client.close()
		self.client2 = TcpSocketClient(socket.AF_INET, socket.SOCK_STREAM)
		ADDR = (self.ip, self.port)
		self.client2.connect((ADDR))
		self.client2.setblocking(False)
		self.client2.send(login.LoginAccessLoginClient(self.account_id, self.login_id, self.version, self.account, self.password))

	def setaccount(self):
		self.account = mylib.Ranstr(9)

	def FunPlayerRequestLoginClient(self,argv):
		#print("FunServerReturnLoginClient")
		self.client.send(login.PlayerRequestLoginClient(self.account, self.password, 1))
	
	def FunLoginAccessLoginClient(self,argv):
		self.account_id = argv[1]
		self.login_id = argv[2]
		self.ip = argv[3]
		self.port = argv[4]

	def FunCheckNameSelectClient(self,argv):
		#print("FunCheckNameSelectClient")
		self.sex = argv[1]
		self.name = argv[2]
		self.client2.send(login.CheckNameSelectClient(self.name))
	
	def FunCreateSelectClient(self,argv):
		#print("FunCreateSelectClient")
		self.client2.send(login.CreateSelectClient(self.account_id, self.playerid, self.sex, self.name, self.account))

	def FunPlayerListSelectClient(self,argv):
		#print("FunCreateSelectClient")
		self.client2.send(login.CreateRandomRoleNameClient())
		self.finishFb = 0
	
	def FunAddMapMapScreenClient(self,argv):
		#print("FunAddMapMapScreenClient")
		self.client2.send(Fb.SendReadyClient())

	fundict["ServerReturnLoginClientCmd_S"] = FunPlayerRequestLoginClient
	fundict["ServerReturnLoginSuccessLoginClientCmd_S"] = FunLoginAccessLoginClient
	fundict["CreateRandomRoleNameClientCmd_CS"] = FunCheckNameSelectClient
	fundict["CheckNameSelectClientCmd_CS"] = FunCreateSelectClient
	fundict["PlayerListSelectClientCmd_S"] = FunPlayerListSelectClient
	
	fundict["AddMapMapScreenClientCmd_S"] = FunAddMapMapScreenClient

	@task(2)
	def recvmessage(self):
		for num in range(1,30):
			try:
				(msgsize, msgNo) = struct.unpack('2H',self.client2.recv(4))
				msg = self.client2.recv(msgsize)
			except:
				pass
			else:
				f = mylib.UnpackData(msgsize, msgNo, msg)
				if self.fundict.has_key(f[0]) :
					self.fundict[f[0]](self,f)
	
	@task(1)
	def RequestPing(self):
		if (datetime.now() - self.PingTime).seconds > 10 :
			self.client2.send(login.RequestPingClient())
			self.PingTime = datetime.now()
	
	#@task(1)
	def SendGmCmd(self):
		if (datetime.now() - self.FbTime).seconds > 60 :
			if self.FbEnterFirst == True :
				self.client2.send(GMcmd.GMChatClient("addlevel","lv=80"))
				self.client2.send(GMcmd.GMChatClient("addphysical","value=100"))
				self.client2.send(GMcmd.CompletePlotChapterClient(1001, 1001, 1, True))
				self.FbEnterFirst = False
			else:
				self.FbTime = datetime.now()

			self.client2.send(Fb.RequestEnterFbClient(1011, 2000, 1))


class PlayerVerifyVerLogin(Locust):
	min_wait = 100
	max_wait = 1000
	task_set = VerifyVerLogin
	
if __name__ == "__main__":
	user = PlayerVerifyVerLogin()
	user.run()
	
