import os
import cv2
import sys
import shutil
import os.path


def check_color_and_image_input(path, image_name, image_color, web_colors=None):
    """check if the color input is webcolor and image is valid"""
    try:
        os.listdir(path)
    except OSError as error:
        print(error)
        raise
    if web_colors is None:
        web_colors = ["white", "silver", "gray", "black", "red", "maroon", "yellow", "olive", "lime", "green", "aqua",
                      "teal", "blue", "navy", "fuchsia", "purple"]
    if not image_color.lower() in web_colors:
        sys.exit("Not valid webcolor")
    image = cv2.imread(os.path.join(path, image_name), -1)
    if image is None:
        sys.exit("[Error]: Input is an invalid image or path is not correct")


def save_images(folder_destination_name, path_source, image_name, image_color):
    """Parameters:
    folder_destination_name - folder for saving folders with images||
    path_source - path source of images ||
    image_name - image name ||
    image_color - webcolor of image ||

    Overall description: Create folders according image colors and save images to corresponding folders
    """

    # Create folder for sorted images
    try:
        if not os.path.isdir(folder_destination_name):
            os.mkdir(folder_destination_name)
    except OSError as error:
        print(error)
    # Create webcolor folders and save images into the folders
    img_path = os.path.join(folder_destination_name, image_color)
    try:
        if not os.path.isdir(img_path):
            os.mkdir(img_path)
    except OSError as error:
        print(error)
    else:
        # Copy the content of source to destination
        img_path_source = os.path.join(path_source, image_name)
        img_path_destination = os.path.join(folder_destination_name, image_color, image_name)
        shutil.copyfile(img_path_source, img_path_destination)


def save_sorted_images():
    """Establish connection, receive message: webcolor, path and image name,
    call functions, save image according the color"""


    import pika
    file_sorted_images_name = "docker-shared/sorted-images-communication"
    queue_name = "m2_compute_to_m3_save_images"

    # establishing connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='host.docker.internal'))
    channel = connection.channel()

    # creating queue
    channel.queue_declare(queue=queue_name)

    #  Receiving messages from the queue - subscribing a callback function to a queue
    def callback(ch, method, properties, body):
        #  Receiving message
        received_webcolor_path_image_name = body.decode('utf8')
        print(" [x] Received:", received_webcolor_path_image_name, " => running module3")
        webcolor_path_image_name = received_webcolor_path_image_name.split(";")

        #  Save images
        webcolor_path_image_name[1] = "docker-shared/" + webcolor_path_image_name[1]
        check_color_and_image_input(webcolor_path_image_name[1], webcolor_path_image_name[2],
                                    webcolor_path_image_name[0])
        save_images(file_sorted_images_name, webcolor_path_image_name[1], webcolor_path_image_name[2],
                    webcolor_path_image_name[0])
        print("=> Image", webcolor_path_image_name[2], "saved to",
              os.path.join(file_sorted_images_name, webcolor_path_image_name[0], webcolor_path_image_name[2]))
        print("=> Module 3 finished...")
        print(' [*] Waiting for messages. To exit press CTRL+C')

    # callback function will receive messages from queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # Waits for data and runs callbacks whenever necessary
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        save_sorted_images()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
