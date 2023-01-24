import pika

server = "localhost"
port = 5672
vhost = "/"
username = "guest"
password = "guest"
exchangeName = "testEx"

try:
    # connect
    credentials = pika.PlainCredentials(username, password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=server, port=port, virtual_host=vhost, credentials=credentials,
                                  heartbeat=60))
    channel = connection.channel()

    # send message
    # for fanout type exchange, routing key is useless
    properties = pika.spec.BasicProperties(content_type="text/plain", delivery_mode=1)
    channel.basic_publish(exchange=exchangeName, routing_key="", body=b"Hello World!", properties=properties)

    # disconnect
    connection.close()
except Exception as e:
    print(e)
