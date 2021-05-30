import cv2
import sys
import os

def get_file_names(path, extensions="all"):
    """Parameters:
    path - path with files ||
    extensions - string of extensions, e.g. "jpg, png" ||
    returns - list of files according the extensions

    Overall description: get file path and extensions and return file names in the specific path according the
    extensions. """
    file_list = []
    # check if the folder exists
    try:
        folder_list = os.listdir(path)
    except OSError as error:
        print(error)
    else:
        # get all files with extensions - empty string and with string "all"
        if (extensions.lower() in "all") or (not extensions.lower().strip()):
            for file in folder_list:
                filename, file_extension = os.path.splitext(file)
                if file_extension:
                    file_list.append(filename + file_extension)
        # get only files with required extensions
        else:
            for file in folder_list:
                filename, file_extension = os.path.splitext(file)
                splited_extensions = extensions.split(",")
                stripted_extensions = [i.strip(' ') for i in splited_extensions]
                if file_extension and (file_extension[1:] in stripted_extensions):
                    file_list.append(filename + file_extension)
        print(path.title() + " is the path.")
        print(extensions.title() + " is/are the extension/s.")
        if not file_list:
            print("Files with extensions", extensions, " haven't been found")
        else:
            print(file_list, " file list.")
    return file_list


def get_valid_images(path, file_list):
    """Parameters:
    path - path with files ||
    file_list - list of files ||
    returns - list of images

    Overall description: get file list and check if the files are images than return list of images. """

    images_in_directory = []
    unloaded_files = []
    for img_name in file_list:
        a, file_extension = os.path.splitext(img_name)
        img_path = os.path.join(path, img_name)  # path for image
        img = cv2.imread(img_path, -1)  # validate file/image by reading
        if not (img is None):
            images_in_directory.append((img_name))
        elif (img is None) and (bool(file_extension)):
            unloaded_files.append(img_name)
    if unloaded_files:
        print("Following files aren't valid images:", unloaded_files)
    return images_in_directory


def load_send_files():
    import pika

    queue_name = "path_module1"

    # establishing connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='host.docker.internal'))
    channel = connection.channel()

    # creating queue
    channel.queue_declare(queue=queue_name)

    #  Receiving messages from the queue - subscribing a callback function to a queue
    #  Note: Whenever message is received, this callback function is called by the Pika library
    def callback(ch, method, properties, body):
        image_path_relative = body.decode('utf8')
        print(" [x] Received:", image_path_relative, " => running module1")
        image_path = "docker-shared/" + image_path_relative
        file_list = get_file_names(image_path)
        images_in_directory = get_valid_images(image_path, file_list)
        print("=> Valid images in the directory: ", images_in_directory)
        #send message
        queue_m1_to_m2 = "m1_get_files_to_m2_compute"
        channel.queue_declare(queue=queue_m1_to_m2)
        for image_name in images_in_directory:
            #join image path and image name into one message
            path_image_name = [image_path_relative, image_name]
            path_image_name = ';'.join([str(elem) for elem in path_image_name])
            message_path_image_name = bytes(path_image_name, 'utf8')
            channel.basic_publish(exchange='', routing_key=queue_m1_to_m2, body=message_path_image_name)
            print(" [x] Sent message with path and image name:", message_path_image_name.decode('utf8'))
        print("=> Module 1 finished...")
        print(' [*] Waiting for messages. To exit press CTRL+C')
    # Tell RabbitMQ that this particular callback function should receive messages from our hello queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # Waits for data and runs callbacks whenever necessary
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        load_send_files()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
