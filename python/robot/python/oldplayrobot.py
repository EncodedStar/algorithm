#!/usr/bin/python3 
# encoding: utf-8

import socket,random,string,logging,json,time,math
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
import sys
selector = DefaultSelector()
stopped = False
 
class Crawler:
	addr_list = [ ("172.18.0.150",60001),("172.18.0.153",60001),("172.18.0.156",60001) ] 
	#echo_list = [ ("172.18.0.150",60051),("172.18.0.153",60051),("172.18.0.156",60051) ] 	
	echo_list = [ ("172.18.0.153",60051),("172.18.0.156",60051) ] 	
	craCount = 0
	rev_addr = 0
	def __init__(self,account_name):
		self.Robot_account_name = str(account_name)
		self.sock = None
		self.response = b''
		self.Number = 0
		Crawler.craCount += 1
		self.Echo_num = 0
		self.echo_socketlist = []
		self.addr_server_ip = "172.18.0.150"
		self.addr_server_port = 60051

	def Send_echo(self):
		Time = math.floor(time.time()*1000)
		client2echo_pro  = '''{"Pro_Name":"GetAddr","send_time_ms":%d,"account":"%s"}'''%(Time,self.Robot_account_name)
		time.sleep(0.001)
		for num in range(0,len(self.echo_list)):
			echo_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			echo_socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
			echo_socket.settimeout(0)
			self.echo_socketlist.append(echo_socket)
			address = self.echo_list[num]
			echo_socket.sendto(client2echo_pro.encode('ascii'),address)
			logging.info("echo sendto")
			selector.register(echo_socket.fileno(), EVENT_READ, self.Rev_echo)

	def Rev_echo(self, key, mask):
		selector.unregister(key.fd)
		if(self.Echo_num > 0):
			return
		for num in range(0,len(self.echo_socketlist)):
			try:
				(echo_re_data,_)= self.echo_socketlist[num].recvfrom(8192)
				logging.info(echo_re_data)
				self.Echo_num += 1 
				if echo_re_data != "":
					try:
						rdata = json.loads(echo_re_data)
						self.addr_server_ip = rdata["ip"]
						self.addr_server_port = int(rdata["port"])
						self.Conn_addr()
					except:
						error_log = '''AccountName: %s received false echoserver data'''%(self.Robot_account_name) 
						logging.debug(error_log)
				break
			except BlockingIOError:
				pass
		
		
	
	def Conn_addr(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
		addr_server = (self.addr_server_ip, self.addr_server_port)
		try:
			self.sock.connect(addr_server)
			self.sock.setblocking(False)
		except:
			(ErrorType, ErrorValue, ErrorTB) = sys.exc_info()
			print ("Connect server failed: ",ErrorValue)
			#error_log = '''AccountName: %s connaddr false Ip : %s Port : %d'''%(self.Robot_account_name,self.addr_server_ip, self.addr_server_port)
			#logging.debug(error_log)
		selector.register(self.sock.fileno(), EVENT_WRITE, self.Send_addr)

	def Send_addr(self, key, mask):
		selector.unregister(key.fd)
		client2addr_pro = '''{"Pro_Name":"GetAccount", "account":"%s", "echo_no_resp":"%s" ,"request_seq":%d}'''%(self.Robot_account_name,"false",1)
		try:
			self.sock.send(client2addr_pro.encode('ascii'))
			Log = '''AccountName: %s sendaddr'''%(self.Robot_account_name)
			logging.debug(Log)
		except:
			pass
			error_log = '''AccountName: %s sendaddr false'''%(self.Robot_account_name)
			logging.debug(error_log)
		selector.register(key.fd, EVENT_READ, self.Rev_addr)

	def Rev_addr(self, key, mask):
		selector.unregister(key.fd)
		try:
			chunk = self.sock.recv(4096)
		except:
			error_log = '''AccountName: %s revaddr false'''%(self.Robot_account_name)
			logging.debug(error_log)
			return

		if chunk:
			self.response += chunk
			Log = '''AccountName: %s revaddr %s'''%(self.Robot_account_name,self.response)
			logging.info(Log)
		Crawler.rev_addr += 1
		if( Crawler.rev_addr >= 2000):
			Crawler.rev_addr = 0
			global stopped
			stopped = True

def loop():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback(event_key, event_mask)
 
if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
		datefmt='%a, %d %b %Y %H:%M:%S',
		filename='oldplay.log',
		filemode='a')
	while True:
		for account_name in range(0,2000):
			crawler = Crawler(account_name)
			crawler.Send_echo()
		stopped = False
		loop()
