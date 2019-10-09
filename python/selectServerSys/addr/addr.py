#!/usr/bin/env python

import pika
import json as js
import json
import socket
from time import ctime
import datetime
import threading
import redis
import logging


config_file = file('config')
config_text = js.load(config_file)
#print config_text

AMQP_SERVER = "47.106.148.60"
AMQP_USER = "guest"
AMQP_PASS = "guest"
AMQP_VHOST = "/"
AMQP_CENTER_QUEUE = "Center_MQ"

LOCAL_ID = str(config_text['id'])
LOCAL_REGION = str(config_text['region'])
LOCAL_IP = str(config_text['ip'])
LOCAL_PORT = int(config_text['port'])
LOCAL_QUEUE = LOCAL_REGION + '_addr_' + LOCAL_ID

account2sock = {}
lock = threading.Lock()
gamelist = []
recommend_ip = 'null'
recommend_port = -1

creds_broker_producer = pika.PlainCredentials(AMQP_USER,AMQP_PASS)
conn_params_producer = pika.ConnectionParameters(AMQP_SERVER,virtual_host = AMQP_VHOST,credentials = creds_broker_producer)

redis_pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
redis_server = redis.Redis(connection_pool = redis_pool)

def log_init():     
    logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
		datefmt='%a, %d %b %Y %H:%M:%S',
		filename='addr.log',
		filemode='w')

def id2ip_port(game_id):
	ip = recommend_ip
	port = recommend_port
	try:
		if -1 == game_id:
			return ip,port
		for i in range(0,len(gamelist)):
			game_data = gamelist[i]
			game_data_id = game_data['id']
			if int(game_data_id) == game_id:
				ip = game_data['ip']
				port = game_data['port']
				return ip,port
	except Exception,e:
	        logging.error('[id2ip_port :]' + str(e))
	return ip,port

def get_gamelist(body_js):
	global gamelist
	global recommend_ip
	global recommend_port
	#print body_js
	recommend_id = body_js['recommend']['id']
	gamelist = body_js['gamelist']
	recommend_ip,recommend_port = id2ip_port(int(recommend_id))
	#print gamelist
	logging.debug('[recommend_ip,recommend_port]' + str(recommend_ip) + ',' + str(recommend_port) )

def keepalive(body_js):
	body = json.dumps(body_js)
	logging.info('[keepalive]' + str(body)) 

def register_addr():
	logging.info('register_addr')
	register_message = '{\"Pro_Name\" : \"RegisterAddr\" , \"id\" : ' + LOCAL_ID + ' ,\"region\" : ' + '\"' +LOCAL_REGION + '\"' + ',\"ip\" :' + '\"' + LOCAL_IP + '\"'+ ',\"port\" : ' + str(LOCAL_PORT) + '}'
	return str(register_message)

def msg_consumer(channel_consumer,method,header,body):
	logging.debug('msg_consumer rev body :' + str(body))
        channel_consumer.basic_ack(delivery_tag = method.delivery_tag)
	global account2sock
	try:
		body_js = json.loads(body)
		ProName = str(body_js['Pro_Name'])
		logging.debug(' ProName == ' + ProName)

		if   'GameList' == ProName or 'UpdateGameList_Re' == ProName: 
			get_gamelist(body_js)

		elif 'GetAccountinfo_Re' == ProName:
			game_id = body_js['id']
			retcode = body_js['retcode']
			account_name = body_js['account']
			sock = account2sock[account_name]
			ip,port = id2ip_port(int(game_id))
			if game_id != -1: 
				redis_server.set(account_name,game_id)
			getaccountinfo_re_message = '{\"Pro_Name\":\"GetAccount_Re\",\"retcode\":' + str(retcode)  + ',\"ip\": ' + '\"' + ip + '\"' + ', \"port\" : ' + str(port) +  '}'
			logging.debug('getaccountinfo_re_message send :' + getaccountinfo_re_message)
			sock.send(getaccountinfo_re_message)
			lock.acquire() 
			del account2sock[account_name]
			lock.release()
			sock.close()

		elif 'KeepAlive' == ProName:
			keepalive(body_js)

		else:
			logging.error(' ProName == ' + ProName)

	except Exception,e:
		logging.error('[thread :]' + str(e))
	return

def thread():
	logging.info('thread()')
	creds_broker_consumer = pika.PlainCredentials(AMQP_USER,AMQP_PASS)                                                         
	conn_params_consumer = pika.ConnectionParameters(AMQP_SERVER,virtual_host = AMQP_VHOST,credentials = creds_broker_consumer)
	conn_broker_consumer = pika.BlockingConnection(conn_params_consumer)
	channel_consumer = conn_broker_consumer.channel()
	channel_consumer.basic_consume( msg_consumer,queue = LOCAL_QUEUE,consumer_tag = "addr-consumer")
	channel_consumer.start_consuming()
	conn_broker_consumer.close()
	conn_broker_producer.close()

def main():
	log_init()
	logging.info('main()')
	logging.info(' LOCAL_ID: ' + LOCAL_ID + ' LOCAL_REGION: ' + LOCAL_REGION + ' LOCAL_IP: ' + LOCAL_IP + ' LOCAL_PORT: ' + str(LOCAL_PORT) + ' LOCAL_QUEUE: ' + LOCAL_QUEUE)
	
	try:
		t1 = threading.Thread(target=thread)
		t1.start()
	except:
		logging.error('Error: unable to start thread')

	conn_broker_producer = pika.BlockingConnection(conn_params_producer)
	channel_producer = conn_broker_producer.channel()
	channel_producer.queue_declare(queue = LOCAL_QUEUE)

	register_message = register_addr()
	channel_producer.basic_publish(exchange = '', routing_key = AMQP_CENTER_QUEUE, body = register_message)
	server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	server.bind((LOCAL_IP,LOCAL_PORT))
	server.listen(10000) 
	server.settimeout(1)
	global account2sock
	start_time = datetime.datetime.now()
	data = ""
	while True:
		end_time = datetime.datetime.now()
		if (end_time - start_time).seconds > 29 :
			start_time = datetime.datetime.now()
			logging.info('send KeepAlive')
			keepalive_message = '{\"Pro_Name\":\"KeepAlive\",\"id\":' + LOCAL_ID  + ',\"region\": ' + '\"' + LOCAL_REGION + '\"' + '}'
			logging.debug('KeepAlive : ' + keepalive_message)
			channel_producer.basic_publish(exchange = '', routing_key = AMQP_CENTER_QUEUE, body = keepalive_message)	
		try:
			sock,addr = server.accept()
			data = sock.recv(1024)
			data_js = json.loads(data)
			logging.debug('Get client msg is:' + data)
			logging.debug('Received from and returned to: ' + str(addr))
			ProName = str(data_js['Pro_Name'])
			logging.info(ProName)

			if 'GetAccount' == ProName:
				account_name = data_js['account']
				account_message = '{\"Pro_Name\":\"GetAccountinfo\",\"id\":' + LOCAL_ID  + ',\"region\": ' + '\"' + LOCAL_REGION + '\"' +', \"account\": ' + '\"' + account_name + '\"' +'}'
				redis_get_id = redis_server.get(account_name)
				logging.debug(' redis_get_id :' + str(redis_get_id))

				if redis_get_id != None:
					game_id = redis_server.get(account_name)
					ip,port = id2ip_port(int(game_id))
					retcode = 0
					getaccountinfo_re_message = '{\"Pro_Name\":\"GetAccount_Re\",\"retcode\":' + str(retcode)  + ',\"ip\": ' + '\"' + ip + '\"' + ', \"port\" : ' + str(port) +  '}'
					sock.send(getaccountinfo_re_message)
					sock.close()
				else:
					lock.acquire()
					account2sock[str(account_name)] = sock
					lock.release()
					channel_producer.basic_publish(exchange = '', routing_key = AMQP_CENTER_QUEUE, body = account_message)
			else:
				logging.error(' ProName == ' + ProName)
		except Exception,e:
			if str(e) != 'timed out':
				logging.error('[main :]' + str(e))

if __name__=="__main__":
	main()
