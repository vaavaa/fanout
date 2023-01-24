import pika
import time
import argparse

server = "localhost"
port = 5672
vhost = "/"
username = "guest"
password = "guest"
exchangeName = "testEx"
queueName = "testQ1"


# callback funtion on receiving messages
def on_message(channel, method, properties, body):
    print(body)


def run(qname=queueName, mname=exchangeName):
    qname = ''.join(str(str_item) for str_item in qname)
    mname = ''.join(str(str_item) for str_item in mname)
    while True:
        try:
            # connect
            credentials = pika.PlainCredentials(username, password)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=server, port=port, virtual_host=vhost, credentials=credentials,
                                          heartbeat=60))
            channel = connection.channel()

            # declare exchange and queue, bind them and consume messages
            # for fanout type exchange, routing key is useless
            channel.exchange_declare(exchange=exchangeName, exchange_type="fanout", auto_delete=True)
            channel.queue_declare(queue=qname, exclusive=True, auto_delete=True)
            channel.queue_bind(exchange=exchangeName, queue=qname)
            channel.basic_consume(on_message_callback=on_message, queue=qname, auto_ack=True)
            channel.start_consuming()
        except Exception as e:
            # reconnect on exception
            print(f'Exception handled, reconnecting...\nDetail:\n {e}')
            try:
                connection.close()
            except:
                pass
            time.sleep(5)


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mname', nargs='*', type=str, default='testmnameQ1',
                        help='Название очереди для этого консюмера')
    parser.add_argument('--qname', nargs='*', type=str, default='testQ1',
                        help='Название очереди для этого консюмера')
    opt = parser.parse_args()
    return opt


if __name__ == "__main__":
    opt = parse_opt()
    run(**vars(opt))
