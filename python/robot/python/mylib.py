#!/usr/bin/python   
# -*- coding: utf-8 -*-

import time
import sys
import Command_py.Command_pb2
import random
import struct 

defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding: 
	reload(sys)
	sys.setdefaultencoding(defaultencoding)

def UnpackData(msgsize, msgNo, msg):
	try:
		if msgNo == 157:
			return[""]

		print(" Rev : msgsize:{} msgNo:{} msgNoName:{}".format(msgsize, msgNo, NoToCmd(msgNo)))
		protocol = NoToCmd(msgNo)
		if protocol == "ClientCmdNone":
			return [""]
		else:
			if CheckCallBackList(protocol):
				return CallBack(protocol)(msg) 
			else:
				print("No Protocol Register CallBack!")
				return [""]
	except:
		return [""]

def PackData(messages,proname):
	#print("send Name:{}",proname)
	messages_len = len(messages)
	No = CmdToNo(proname)
	messagespack = struct.pack('<HH', messages_len, No) 
	messagespack = messagespack + messages
	return messagespack
def CmdToNo(cmd):
	cmd_c = cmd + "_C"
	try:
		return Command_py.Command_pb2.CmdNumber.Value(cmd_c)
	except ValueError:
		cmd_s = cmd + "_S"
	try:
		return Command_py.Command_pb2.CmdNumber.Value(cmd_s)
	except ValueError:
		cmd_cs = cmd + "_CS"
	try:
		return Command_py.Command_pb2.CmdNumber.Value(cmd_cs)
	except ValueError:
		print(" CmdError:",cmd)

def NoToCmd(no):
	try:
		return Command_py.Command_pb2.CmdNumber.Name(no)
	except:
		print(" NoError:",no)

def Sleep(t):
	time.sleep(t)

def Ranstr(num):
	H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
	salt = ''
	for i in range(num):
		salt += random.choice(H)
	return salt

RevCallBackList = {}
#回调注册
def RegisterCallBack(func_type,func):
	RevCallBackList[func_type] = func

def CallBack(func_type):
	return RevCallBackList[func_type]

def CheckCallBackList(func_type):
	return RevCallBackList.has_key(func_type)



