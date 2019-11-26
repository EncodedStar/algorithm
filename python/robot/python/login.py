#!/usr/bin/python   
# -*- coding: utf-8 -*-

import mylib
import Command_py.Command_pb2 
import Command_py.LoginCommand_pb2  
import Command_py.SelectCommand_pb2 
import Command_py.TaskCommand_pb2 
import Command_py.map_screen_command_pb2 
import Command_py.PlayerDataCommand_pb2 

def PlayerVerifyVerLoginClient(game, zone, version):
	protocmd = Command_py.LoginCommand_pb2.PlayerVerifyVerLoginClientCmd()
	protocmd.game = game
	protocmd.zone = zone
	protocmd.version = version.encode('utf-8')
	messages = protocmd.SerializeToString()
	return mylib.PackData(messages,"PlayerVerifyVerLoginClientCmd")

def ServerReturnLoginClient(data):
	try:
		target = Command_py.LoginCommand_pb2.ServerReturnLoginClientCmd()
		target.ParseFromString(data)
		return ["ServerReturnLoginClientCmd_S",target.ret_code]
	except :
		#print("Error : ServerReturnLoginClient")
		return [""]

def PlayerRequestLoginClient(account,password,platform_id):
	protocmd = Command_py.LoginCommand_pb2.PlayerRequestLoginClientCmd()
	protocmd.account = account
	protocmd.password = password
	protocmd.platform_id = 1
	messages = protocmd.SerializeToString()
	return mylib.PackData(messages,"PlayerRequestLoginClientCmd")

def ServerReturnLoginSuccessLoginClient(data):
	try:
		target = Command_py.LoginCommand_pb2.ServerReturnLoginSuccessLoginClientCmd()
		target.ParseFromString(data)
		#print('Accountid:{accountid} Loginid:{loginid} Ip:{ip} Port:{port} State:{state} Account:{account}'.format(accountid = target.account_id, loginid = target.login_id, ip = target.ip, port = target.port, state = target.state, account = target.account))
		return ["ServerReturnLoginSuccessLoginClientCmd_S", target.account_id, target.login_id, target.ip, target.port, target.state, target.account]
	except :
		#print("Error : ServerReturnLoginSuccessLoginClient")
		return [""]

def LoginAccessLoginClient(account_id, login_id, version, account, password):
	protocmd = Command_py.LoginCommand_pb2.LoginAccessLoginClientCmd()
	protocmd.login_id = login_id
	protocmd.account_id = account_id
	protocmd.version = version
	protocmd.account = account
	protocmd.password = password 
	messages = protocmd.SerializeToString()
	return mylib.PackData(messages,"LoginAccessLoginClientCmd")

def SendReconnectKeyClient(data):
	try:
		target = Command_py.LoginCommand_pb2.SendReconnectKeyClientCmd()
		target.ParseFromString(data)
		return ["SendReconnectKeyClient",target.key]
	except:
		return [""]

def ReqInitDevice():
	protocmd = Command_py.LoginCommand_pb2.ReqInitDeviceCmd()
	protocmd.token = '3'.encode('utf-8')
	messages = protocmd.SerializeToString()
	return mylib.PackData(messages,"ReqInitDeviceCmd")

def RespondMsgClient(data):
	try:
		target = Command_py.LoginCommand_pb2.SendReconnectKeyClientCmd()
		target.ParseFromString(data)
		return ["RespondMsgClient", msg_id]
	except:
		return [""]

#随机创建一个玩家名字
def CreateRandomRoleNameClient():
	protocmd = Command_py.SelectCommand_pb2.CreateRandomRoleNameClientCmd()
	protocmd.sex = 0
	protocmd.name = ""
	messages = protocmd.SerializeToString()
	return mylib.PackData(messages,"CreateRandomRoleNameClientCmd")

def CreateRandomRoleNameClientRev(data):
	try:
		target = Command_py.SelectCommand_pb2.CreateRandomRoleNameClientCmd()
		target.ParseFromString(data)
		#print("sex:{} name:{}".format(target.sex, target.name))
		return ["CreateRandomRoleNameClientCmd_CS", target.sex, target.name]
	except:
		return [""]
	

#检测玩家是否正确
def CheckNameSelectClient(name):
	protocmd = Command_py.SelectCommand_pb2.CheckNameSelectClientCmd()	
	protocmd.name = name
	protocmd.err_code = 0
	messages = protocmd.SerializeToString()
	return mylib.PackData(messages,"CheckNameSelectClientCmd")

def CheckNameSelectClientRev(data):
	try:
		target = Command_py.SelectCommand_pb2.CheckNameSelectClientCmd()
		target.ParseFromString(data)
		#print("name:{} err_code:{}".format(target.name, target.err_code))
		return ["CheckNameSelectClientCmd_CS", target.name, target.err_code]
	except:
		return [""]
	
#创建玩家
def CreateSelectClient(account_id, playerid, sex, name, account):
	protocmd = Command_py.SelectCommand_pb2.CreateSelectClientCmd()	
	protocmd.data.accid = account_id
	protocmd.data.playerid = playerid
	protocmd.data.sex = sex
	protocmd.data.name = name
	protocmd.data.account = account
	messages = protocmd.SerializeToString()
	return mylib.PackData(messages,"CreateSelectClientCmd")

#创建玩家结果
def CreateSelectResultClient(data):
	try:
		target = Command_py.SelectCommand_pb2.CreateSelectResultClientCmd()
		target.ParseFromString(data)
		#print("CreateSelectResultClient_Re err_code:{}".format(target.err_code))
		return ["CreateSelectResultClient_Re", target.err_code]
	except:
		return [""]

def LoginStepSelectClient(data):
	try:
		target = Command_py.SelectCommand_pb2.LoginStepSelectClientCmd()
		target.ParseFromString(data)
		#print("manhood:{} servertime:{} onlinetime:{}".format(target.manhood, target.servertime, target.onlinetime))
		return ["LoginStepSelectClientCmd_S",target.manhood, target.servertime, target.onlinetime]
	except:
		return [""]

#玩家第一次登陆返回
def PlayerListSelectClient(data):
	try:
		target = Command_py.SelectCommand_pb2.PlayerListSelectClientCmd()
		target.ParseFromString(data)
		#print("num:{} needCreate:{} manhood:{} servertime:{}".format(target.num, target.needCreate, target.manhood, target.servertime))
		return ["PlayerListSelectClientCmd_S",target.num, target.needCreate, target.manhood, target.servertime]
	except:
		return [""]
	
def SendQuestQuestClient(data):
	#TODO:任务信息
	try:
		target = Command_py.TaskCommand_pb2.SendQuestQuestClientCmd()
		target.ParseFromString(data)
		return ["SendQuestQuestClientCmd_S"]
	except:
		return [""]

def SendQuestElementQuestClient(data):
	#TODO:任务信息
	try:
		target = Command_py.TaskCommand_pb2.SendQuestElementQuestClientCmd()
		target.ParseFromString(data)
		return ["SendQuestElementQuestClientCmd_S", target.elem.quest_id]
	except:
		return [""]

def SyncPlayerFlagClientCmd(data):
	#TODO:信息
	try:
		return [""]
	except:
		return [""]

def AddDataItemClientCmd(data):
	#TODO:信息
	try:
		return [""]
	except:
		return [""]

def SyncTime(data):
	#TODO:信息
	try:
		return [""]
	except:
		return [""]

def SetPackageGridPackageClient(data):
	#TODO:信息
	try:
		return [""]
	except:
		return [""]

def TODO(data):
	try:
		return [""]
	except:
		return [""]

def RequestPingClient():
	protocmd = Command_py.LoginCommand_pb2.RequestPingClientCmd()	
	messages = protocmd.SerializeToString()
	return mylib.PackData(messages,"RequestPingClientCmd")
	
def RespondPingClientRev(data):
	return ["RequestPingClientCmd_S"]
	
	
def InitCallBack():
	mylib.RegisterCallBack("ServerReturnLoginClientCmd_S",ServerReturnLoginClient)
	mylib.RegisterCallBack("ServerReturnLoginSuccessLoginClientCmd_S",ServerReturnLoginSuccessLoginClient)
	mylib.RegisterCallBack("SendReconnectKeyClientCmd_S",SendReconnectKeyClient)
	mylib.RegisterCallBack("RespondMsgClientCmd_S",RespondMsgClient)
	mylib.RegisterCallBack("CreateRandomRoleNameClientCmd_CS",CreateRandomRoleNameClientRev)
	mylib.RegisterCallBack("CheckNameSelectClientCmd_CS",CheckNameSelectClientRev)
	mylib.RegisterCallBack("CreateSelectResultClientCmd_S",CreateSelectResultClient)
	mylib.RegisterCallBack("LoginStepSelectClientCmd_S",LoginStepSelectClient)
	mylib.RegisterCallBack("PlayerListSelectClientCmd_S",PlayerListSelectClient)
	mylib.RegisterCallBack("SendQuestQuestClientCmd_S",SendQuestQuestClient)
	mylib.RegisterCallBack("SendQuestElementQuestClientCmd_S",SendQuestElementQuestClient)
	mylib.RegisterCallBack("SyncPlayerFlagClientCmd_S",SyncPlayerFlagClientCmd)
	mylib.RegisterCallBack("AddDataItemClientCmd_S",AddDataItemClientCmd)
	mylib.RegisterCallBack("SyncTime_S",SyncTime)
	mylib.RegisterCallBack("SetPackageGridPackageClientCmd_S",SetPackageGridPackageClient)
	mylib.RegisterCallBack("AddItemListItemClientCmd_S",TODO)
	mylib.RegisterCallBack("SendQuestListQuestClientCmd_S",TODO)
	mylib.RegisterCallBack("SendPlotListClientCmd_S",TODO)
	mylib.RegisterCallBack("RefreshAchievePointListClientCmd_S",TODO)
	mylib.RegisterCallBack("SyncWorldFlagClientCmd_S",TODO)
	mylib.RegisterCallBack("SendInstanceAchieveInfo_S",TODO)
	mylib.RegisterCallBack("RefreshHeadInfoCmd_S",TODO)
	mylib.RegisterCallBack("RefreshFriendListClientCmd_S",TODO)
	mylib.RegisterCallBack("RefreshMailListClientCmd_S",TODO)
	mylib.RegisterCallBack("UpdateRoleDataClientCmd_S",TODO)
	mylib.RegisterCallBack("RespondPingClientCmd_S",RespondPingClientRev)
