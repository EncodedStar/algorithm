#coding:utf-8
import sys
reload(sys) 
sys.setdefaultencoding( "utf-8" ) 
import itchat
# itchat.auto_login()
itchat.auto_login(enableCmdQR=2)
itchat.send('Hello, filehelper', toUserName='filehelper')
