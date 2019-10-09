import pika, json                                               

AMQP_SERVER = "localhost"
AMQP_USER = "guest"
AMQP_PASS = "guest"
AMQP_VHOST = "/"
AMQP_QUEUE = "Center_MQ"

creds_broker_producer = pika.PlainCredentials(AMQP_USER,AMQP_PASS)
conn_params_producer = pika.ConnectionParameters(AMQP_SERVER,virtual_host = AMQP_VHOST,credentials = creds_broker_producer)
conn_broker_producer = pika.BlockingConnection(conn_params_producer)
channel_producer = conn_broker_producer.channel()

channel_producer.exchange_declare(exchange = 'hexin1-exchange', exchange_type = 'direct', passive = False, durable = True, auto_delete = False)
channel_producer.exchange_declare(exchange='hexin-exchange', exchange_type='direct')
channel_producer.queue_declare(queue = 'hexin-queue')

channel_producer.queue_bind(exchange = 'hexin-exchange', queue = 'hexin-queue', routing_key = 'hexin-routing_key')
channel_producer.publish(exchange = 'hexin-exchange', routing_key = 'hexin-routing_key', body = 'hello-hexin')
channel_producer.basic_publish(exchange = '', routing_key = AMQP_QUEUE, body = 'hello-hexin')

def msg_consumer(channel_consumer,method,header,body):
	channel_consumer.basic_ack(delivery_tag=method.delivery_tag)
	print body
	channel_producer.publish(exchange = 'hexin-exchange', routing_key = 'hexin-routing_key', body = 'msg_consumer')
	return

def main():
	print "main"
	creds_broker_consumer = pika.PlainCredentials(AMQP_USER,AMQP_PASS)

	conn_params_consumer = pika.ConnectionParameters(AMQP_SERVER,virtual_host = AMQP_VHOST,credentials = creds_broker_consumer)
	conn_broker_consumer = pika.BlockingConnection(conn_params_consumer)
	channel_consumer = conn_broker_consumer.channel()

	channel_consumer.basic_consume( msg_consumer,queue = AMQP_QUEUE,consumer_tag = "test-consumer")
	channel_consumer.start_consuming()
	
	conn_broker_consumer.close()
	conn_broker_producer.close()

if __name__ == "__main__":
	main()



