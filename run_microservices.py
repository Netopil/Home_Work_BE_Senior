import pika

message_path = 'img'
extensions = 'all'
#example of another variants:
#extensions = 'jpg'
#extensions = 'jpg,png'
#extensions = ''

path_extensions = [message_path, extensions]
message_path_extensions = ';'.join([str(elem) for elem in path_extensions])
message = bytes(message_path_extensions, 'utf8')
queue_name = "path_module1"

# establishing connection
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# creating queue
channel.queue_declare(queue=queue_name)  # queue, but message should be first go through an exchange

# default exchange identified by an empty string - specify exactly to which queue the message should go (routing_key)
channel.basic_publish(exchange='', routing_key=queue_name, body=message)
print(" [x] Sent path with images;extensions:", message.decode('utf8'))

# closing the connection - network buffers were flushed
connection.close()