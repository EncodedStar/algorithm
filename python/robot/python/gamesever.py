#!/bin/python
import pika, json                                               

def main():
	AMQP_SERVER = "172.18.0.171"
	AMQP_USER = "guest"
	AMQP_PASS = "guest"
	AMQP_VHOST = "/"
	AMQP_QUEUE = "CenterMQ"

	creds_broker_producer = pika.PlainCredentials(AMQP_USER,AMQP_PASS)
	conn_params_producer = pika.ConnectionParameters(AMQP_SERVER,virtual_host = AMQP_VHOST,credentials = creds_broker_producer)
	conn_broker_producer = pika.BlockingConnection(conn_params_producer)
	channel_producer = conn_broker_producer.channel()

	channel_producer.exchange_declare(exchange = 'game-exchange', exchange_type = 'direct', passive = False, durable = True, auto_delete = False)

	channel_producer.queue_bind(exchange = 'game-exchange', queue = AMQP_QUEUE, routing_key = 'game-routing-key')
	while True:
		for num in range(0,10000000):
			pro = '''{ "Pro_Name": "UpdateAccountInfo" , "id" : 1, "account" : "old%d"}'''%(num)
			channel_producer.basic_publish(exchange = 'game-exchange', routing_key = 'game-routing-key', body = pro)

if __name__ == "__main__":
	main()



