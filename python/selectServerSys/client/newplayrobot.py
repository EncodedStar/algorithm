#!/usr/bin/python3 
# encoding: utf-8

import socket,random,string,logging,json,time,math
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ
import sys
selector = DefaultSelector()
stopped = False
Numaccount = 2000
class Crawler:
	addr_list = [ ("172.18.0.150",60001),("172.18.0.153",60001),("172.18.0.156",60001) ] 
	#echo_list = [ ("172.18.0.150",60051),("172.18.0.153",60051),("172.18.0.156",60051) ] 	
	echo_list = [ ("10.0.93.12",60051),("10.0.93.17",60051),("10.0.93.5",60051),("10.0.93.16",60051) ]

	rev_addr = 0
	def __init__(self,account_name):
		self.Robot_account_name = str(sys.argv[1]) + "-" + str(account_name)
		self.account_num = account_name
		self.sock = None
		self.response = b''
		self.Number = 0
		self.Echo_num = 0
		self.echo_socketlist = []
		self.addr_server_ip = "172.18.0.150"
		self.addr_server_port = 60052

	def Send_echo(self):
		random.shuffle(self.echo_list)
		logging.debug (self.echo_list)
		Time = math.floor(time.time()*1000)
		client2echo_pro  = '''{"Pro_Name":"GetAddr","send_time_ms":%d,"account":"%s"}'''%(Time,self.Robot_account_name)
		for num in range(0,len(self.echo_list)):
			echo_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			echo_socket.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
			echo_socket.settimeout(0)
			self.echo_socketlist.append(echo_socket)
			address = self.echo_list[num]
			try:
				echo_socket.sendto(client2echo_pro.encode('ascii'),address)
				logging.info("echo sendto seccess")
			except:
				error_log = '''ERROR :: AccountName: %s echo sendto False IP : %s'''%(self.Robot_account_name,self.echo_list[num][0])
				logging.error(error_log)
			selector.register(echo_socket.fileno(), EVENT_READ, self.Rev_echo)

	def Rev_echo(self, key, mask):
		selector.unregister(key.fd)
		if(self.Echo_num > 0):
			return
		for num in range(0,len(self.echo_socketlist)):
			try:
				(echo_re_data,_)= self.echo_socketlist[num].recvfrom(8192)
				Log = '''AccountName: %s revaddr %s'''%(self.Robot_account_name,echo_re_data)
				logging.info(Log)
				self.Echo_num += 1 
				if echo_re_data != "":
					try:
						echo_re_data = bytes.decode(echo_re_data)
						rdata = json.loads(echo_re_data)
						self.addr_server_ip = rdata["ip"]
						self.addr_server_port = int(rdata["port"])
						self.Conn_addr()
					except:
						error_log = '''ERROR :: AccountName: %s echo_re_data False'''%(self.Robot_account_name) 
						logging.debug(error_log)
				break
			except BlockingIOError:
				#TODO: log
				error_log = ''' AccountName: %s received Null echoserver data'''%(self.Robot_account_name)
				logging.error(error_log)
	
	def Conn_addr(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.sock.setblocking(False)
		addr_server = (self.addr_server_ip, self.addr_server_port)
		try:
			self.sock.connect(addr_server)
		except BlockingIOError:
			pass
		selector.register(self.sock.fileno(), EVENT_WRITE, self.Send_addr)

	def Send_addr(self, key, mask):
		selector.unregister(key.fd)
		# echo有响应发送的协议
		client2addr_pro1 = '''{"Pro_Name":"GetAccount", "account":"%s", "echo_no_resp":"%s" ,"request_seq":%d}'''%(self.Robot_account_name,"false",1)
		client2addr_pro2 = '''{"Pro_Name":"GetAccount", "account":"%s", "echo_no_resp":"%s" ,"request_seq":%d}'''%(self.Robot_account_name,"false",2)
		# echo没有响应发送的协议
		client2addr_pro3 = '''{"Pro_Name":"GetAccount", "account":"%s", "echo_no_resp":"%s" ,"request_seq":%d}'''%(self.Robot_account_name,"true",1)
		client2addr_pro4 = '''{"Pro_Name":"GetAccount", "account":"%s", "echo_no_resp":"%s" ,"request_seq":%d}'''%(self.Robot_account_name,"true",2)
		client2addr_pro_list = [client2addr_pro1,client2addr_pro2,client2addr_pro3,client2addr_pro4]
		client2addr_pro = client2addr_pro_list[int(self.account_num)%4]
		try:
			#TODO: return value
			self.sock.send(client2addr_pro.encode('ascii'))
			Log = '''AccountName: %s sendaddr'''%(self.Robot_account_name)
			logging.debug(Log)
			selector.register(self.sock.fileno(), EVENT_READ, self.Rev_addr)
		except:
			error_log = '''ERROR :: AccountName: %s sendaddr False'''%(self.Robot_account_name)
			logging.error(error_log)

	def Rev_addr(self, key, mask):
		selector.unregister(key.fd)
		try:
			chunk = self.sock.recv(4096)
			if chunk:
				self.response += chunk
				Log = '''AccountName: %s revaddr %s'''%(self.Robot_account_name,self.response)
				logging.info(Log)
		except:
			error_log = '''ERROR :: AccountName: %s revaddr False'''%(self.Robot_account_name)
			logging.error(error_log)

		Crawler.rev_addr += 1
		if( Crawler.rev_addr >= Numaccount):
			Crawler.rev_addr = 0
			global stopped
			stopped = True

def loop():
	while not stopped:
		events = selector.select(5)
		if(len(events) == 0):
			break
		for event_key, event_mask in events:
			callback = event_key.data
			callback(event_key, event_mask)
 
if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
		datefmt='%a, %d %b %Y %H:%M:%S')

	while True:
		stopped = False
		for account_name in range( 0, Numaccount ):
			crawler = Crawler(account_name)
			crawler.Send_echo()
		loop()
