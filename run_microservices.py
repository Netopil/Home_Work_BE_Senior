import pika

message_path = '..\img'
message = bytes(message_path, 'utf8')
queue_name = "path_module1"

# establishing connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# creating queue
channel.queue_declare(queue=queue_name)  # queue, but message should be first go through an exchange

# default exchange identified by an empty string - specify exactly to which queue the message should go (routing_key)
channel.basic_publish(exchange='', routing_key=queue_name, body=message)
print(" [x] Sent path with images:", message.decode('utf8'))

# closing the connection - network buffers were flushed
connection.close()