#!/usr/bin/python   
# -*- coding: utf-8 -*-

import mylib
import struct
import Command_py.Command_pb2 
import Command_py.ChatCommand_pb2 
import Command_py.PlotCommand_pb2
import Command_py.CharacterDataCommand_pb2

#发送GM命令
def GMChatClient(command, data):
	protocmd = Command_py.ChatCommand_pb2.GMChatClientCmd()
	protocmd.cmd_data.command = command
	protocmd.cmd_data.data = data
	messages = protocmd.SerializeToString()
	return mylib.PackData(messages,"GMChatClientCmd")

#def UpdatePhysicalClient(data):
#	try:
#		target = Command_py.PlayerDataCommand_pb2.UpdatePhysicalClientCmd()
#		target.ParseFromString(data)
#		print("physical:{} resume_physical:{} is_count_down:{} count_down:{}".format(target.physical, target.resume_physical, target.is_count_down, target.count_down))
#		return ["UpdatePhysicalClientCmd_S"]
#	except:
#		return [""]

#添加卡牌
def NewCardInfoCmd(card_id):
	protocmd = Command_py.CharacterDataCommand_pb2.NewCardInfoCmd()
	protocmd.card_id.append(card_id)
	messages = protocmd.SerializeToString()
	return mylib.PackData(messages,"NewCardInfoCmd")

#完成章节
def CompletePlotChapterClient(packageid, chapterid, sectionid, is_last_section):
	protocmd = Command_py.PlotCommand_pb2.CompletePlotChapterClientCmd()
	protocmd.packageid = packageid
	protocmd.chapterid = chapterid
	protocmd.sectionid = sectionid
	protocmd.is_last_section = is_last_section
	messages = protocmd.SerializeToString()
	return mylib.PackData(messages,"CompletePlotChapterClientCmd")

def InitCallBack():
#	mylib.RegisterCallBack("UpdatePhysicalClientCmd_S",UpdatePhysicalClient)
	return
