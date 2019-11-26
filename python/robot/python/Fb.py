#!/usr/bin/python   
# -*- coding: utf-8 -*-

import mylib
import struct
import Command_py.Command_pb2 
import Command_py.FbCommand_pb2
import Command_py.PlayerDataCommand_pb2

def RequestEnterFbClient(level_id, cardid, degree):
	protocmd = Command_py.FbCommand_pb2.RequestEnterFbClientCmd()
	protocmd.level_id = level_id
	protocmd.cardid.append(cardid)
	protocmd.degree = degree
	messages = protocmd.SerializeToString()
	return mylib.PackData(messages,"RequestEnterFbClientCmd")

#加载场景
def SendReadyClient():
	#print("----------SendReadyClient----")
	protocmd = Command_py.FbCommand_pb2.SendLoadedSceneClientCmd()
	messages = protocmd.SerializeToString()
	return mylib.PackData(messages,"SendLoadedSceneClientCmd")


def AddMapMapScreenClient(data):
	try:
		target = Command_py.map_screen_command_pb2.AddMapMapScreenClientCmd()
		target.ParseFromString(data)
		return ["AddMapMapScreenClientCmd_S", target.scene_id, target.player_id, target.fresh, target.level_id, target.pos_x, target.pos_y]
	except:
		return [""]

def UpdatePlayerMainDataClient(data):
	try:
		target = Command_py.PlayerDataCommand_pb2.UpdatePlayerMainDataClientCmd()
		target.ParseFromString(data)
		main_player_data = target.main_player_data
		#print("pexp:{} plevel:{} physical:{}".format(main_player_data.pexp, main_player_data.plevel, main_player_data.physical))
		return ["UpdatePlayerMainDataClientCmd_S", target.main_player_data]
	except:
		return [""]

def RefreshMoneyDataClient(data):
	#TODO:信息
	try:
		target = Command_py.PlayerDataCommand_pb2.RefreshMoneyDataClientCmd()
		target.ParseFromString(data)
		return ["RefreshMoneyDataClientCmd_S", target.money]
	except:
		return [""]

def UpdatePhysicalClient(data):
	try:
		target = Command_py.PlayerDataCommand_pb2.UpdatePhysicalClientCmd()
		target.ParseFromString(data)
		print("physical:{} resume_physical:{} is_count_down:{} count_down:{}".format(target.physical, target.resume_physical, target.is_count_down, target.count_down))
		return ["UpdatePhysicalClientCmd_S"]
	except:
		return [""]

def UpdateCharacterDataClient(data):
	try:
		return ["UpdatePhysicalClientCmd_S"]
	except:
		return [""]

def RefreshPlotDataClient(data):
	try:
		target = Command_py.PlotCommand_pb2.RefreshPlotDataClientCmd()
		target.ParseFromString(data)
		plot_data = target.plot_data
		print("plot_id:{} cur_element:{} is_finish:{} section_id:{}".format(plot_data.plot_id, plot_data.cur_element, plot_data.is_finish, plot_data.section_id))
		return ["RefreshPlotDataClientCmd_S",target.plot_data]
	except:
		return [""]

def TODO(data):
	try:
		return [""]
	except:
		return [""]

def MoneyChangeClient(data):
	try:
		target = Command_py.PlayerDataCommand_pb2.MoneyChangeClientCmd()
		target.ParseFromString(data)
		print("money_type:{} money_change:{} money_total:{} action:{}".format(target.money_type, target.money_change, target.money_total, target.action))
		return ["MoneyChangeClientCmd_S",target.money_type, target.money_change, target.money_total, target.action]
	except:
		return [""]

		
def InitCallBack():
	mylib.RegisterCallBack("UpdatePhysicalClientCmd_S",UpdatePhysicalClient)  
	mylib.RegisterCallBack("AddMapMapScreenClientCmd_S",AddMapMapScreenClient)
	mylib.RegisterCallBack("UpdatePlayerMainDataClientCmd_S",UpdatePlayerMainDataClient)
	mylib.RegisterCallBack("RefreshMoneyDataClientCmd_S",RefreshMoneyDataClient)
	mylib.RegisterCallBack("UpdateCharacterDataClientCmd_S",UpdateCharacterDataClient)
	mylib.RegisterCallBack("RefreshPlotDataClientCmd_S",RefreshPlotDataClient)
	mylib.RegisterCallBack("RefreshQuestStateQuestClientCmd_S",TODO)
	mylib.RegisterCallBack("RefreshCountItemClientCmd_S",TODO)
	mylib.RegisterCallBack("MoneyChangeClientCmd_S",MoneyChangeClient)
	mylib.RegisterCallBack("RspGetInfoClientCmd_S",TODO)
	return
