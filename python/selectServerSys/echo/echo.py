#!/usr/bin/env python

import pika
import json as js
import json
from socket import *
from time import ctime
import datetime
import threading
import random
import logging

config_file = file('config')
config_text = js.load(config_file)
print config_text

AMQP_SERVER = "47.106.148.60"
AMQP_USER = "guest"
AMQP_PASS = "guest"
AMQP_VHOST = "/"
AMQP_CENTER_QUEUE = "Center_MQ"

creds_broker_producer = pika.PlainCredentials(AMQP_USER,AMQP_PASS)
conn_params_producer = pika.ConnectionParameters(AMQP_SERVER,virtual_host = AMQP_VHOST,credentials = creds_broker_producer)
conn_broker_producer = pika.BlockingConnection(conn_params_producer)
channel_producer = conn_broker_producer.channel()

LOCAL_ID = str(config_text['id'])
LOCAL_REGION = str(config_text['region'])
LOCAL_IP = str(config_text['ip'])
LOCAL_PORT = int(config_text['port'])
LOCAL_QUEUE = LOCAL_REGION + '_echo_' + LOCAL_ID

channel_producer.queue_declare(queue = LOCAL_QUEUE)

addrlist = 'addrlist is null'

def log_init():
	logging.basicConfig(level=logging.DEBUG,
		format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
		datefmt='%a, %d %b %Y %H:%M:%S',
		filename='echo.log',
		filemode='w')

def package_GetAddr_Re(data_js):
	logging.info('package_GetAdde_Re()')
	logging.debug('addlist: ' + addrlist)
	addrlist_js = json.loads(addrlist)
	addrlist_len = len(addrlist_js['addrlist'])
	logging.debug('addrlist_len :'+ str( addrlist_len ))
	if addrlist_len > 0 :
		addr_ip = addrlist_js['addrlist'][random.randint(0,addrlist_len - 1)]['ip']
		addr_port = addrlist_js['addrlist'][random.randint(0,addrlist_len - 1)]['port']
	else :
		logging.error('addrlist_len null')
		addr_ip = LOCAL_IP
		addr_port = LOCAL_PORT
	re_data = '{\"Pro_Name\" : \"GetAddr_Re\",\"send_time_ms\" : ' + '\"'+ str(data_js['send_time_ms']) +'\"'+ ',\"ip\" : ' + '\"'+ addr_ip + '\"' + ',\"port\" : ' + str(addr_port) + '}'
	return re_data

def get_addrlist(body_js):
	global addrlist;
	addrlist = json.dumps(body_js)
	logging.info('get_addrlist()' + str(addrlist))

def keepalive(body_js):
	body = json.dumps(body_js)
	logging.info('[keepalive]' + str(body)) 

def register_echo():
	logging.info('register_echo')
	register_message = '{\"Pro_Name\" : \"RegisterEcho\" , \"id\" : ' + LOCAL_ID + ' ,\"region\" : ' + '\"'+ LOCAL_REGION + '\"'+ ',\"ip\" :' + '\"' + LOCAL_IP + '\"'+ ',\"port\" : ' + str(LOCAL_PORT) + '}'
	channel_producer.basic_publish(exchange = '', routing_key = AMQP_CENTER_QUEUE, body = register_message)

def msg_consumer(channel_consumer,method,header,body):
	logging.debug('msg_consumer rev body :' + str(body))
        channel_consumer.basic_ack(delivery_tag = method.delivery_tag)
	try:
		body_js = json.loads(body)
		ProName = str(body_js['Pro_Name'])
		logging.debug(' ProName == ' + ProName)

		if   'AddrList' == ProName:
			get_addrlist(body_js)
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
	channel_consumer.basic_consume( msg_consumer,queue = LOCAL_QUEUE,consumer_tag = "echo-consumer")
	channel_consumer.start_consuming()
	conn_broker_consumer.close()
	conn_broker_producer.close()

def main():
	log_init()
	logging.info('main()')
	try:
		t1 = threading.Thread(target=thread)
		t1.start()
	except:
		logging.error('Error: unable to start thread')
	
	logging.info(' LOCAL_ID: ' + LOCAL_ID + ' LOCAL_REGION: ' + LOCAL_REGION + ' LOCAL_IP: ' + LOCAL_IP + ' LOCAL_PORT: ' + str(LOCAL_PORT) + ' LOCAL_QUEUE: ' + LOCAL_QUEUE)
	register_echo()
	BUFSIZE = 1024
	ADDR = ("",LOCAL_PORT)
	udpSerSock = socket(AF_INET, SOCK_DGRAM)
	udpSerSock.bind(ADDR)
	udpSerSock.settimeout(0.01)
	start_time = datetime.datetime.now()
	while True:
		end_time = datetime.datetime.now()
		if (end_time - start_time).seconds > 29 :
			start_time = datetime.datetime.now()
			logging.info('send KeepAlive')
			keepalive_message = '{\"Pro_Name\":\"KeepAlive\",\"id\":' + LOCAL_ID  + ',\"region\": ' + '\"' + LOCAL_REGION + '\"' + '}'
			logging.debug('KeepAlive : ' + keepalive_message)
			channel_producer.basic_publish(exchange = '', routing_key = AMQP_CENTER_QUEUE, body = keepalive_message)	
		try:
			data, addr = udpSerSock.recvfrom(BUFSIZE)
			data_js = json.loads(data)
			logging.debug('Get client msg is:' + data)
			logging.debug('Received from and returned to: ' + str(addr))
			ProName = str(data_js['Pro_Name'])
			logging.info(ProName)

			if   'GetAddr' == ProName:
				logging.debug(' ProName == ' + ProName)
				rec_data = package_GetAddr_Re(data_js)
				logging.debug('rec_data : ' + rec_data)
				udpSerSock.sendto(rec_data, addr)
			else:
				logging.error(' ProName == ' + ProName)

		except Exception,e:
			if str(e) != 'timed out':
				logging.error('[main :]' + str(e))
	udpSerSock.close()

if __name__=="__main__":
	main()
