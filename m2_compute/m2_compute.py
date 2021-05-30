import numpy as np
import os
import sys
import cv2


# from m1_get_files import load_set_files
class ImageWebColor:
    """Class ImageWebColor"""

    def __init__(self, path, image_name, bits_per_color_channel=8):
        """Initialize image name and bits per color channel, read image

        Note: possibility to change color depth"""
        self.web_colors_definition = [("White", [100, 100, 100]), ("Silver", [75, 75, 75]),
                                      ("Gray", [50, 50, 50]), ("Black", [0, 0, 0]),
                                      ("Red", [100, 0, 0]), ("Maroon", [50, 0, 0]),
                                      ("Yellow", [100, 100, 0]), ("Olive", [50, 50, 0]),
                                      ("Lime", [0, 100, 0]), ("Green", [0, 50, 0]),
                                      ("Aqua", [0, 100, 100]), ("Teal", [0, 50, 50]),
                                      ("Blue", [0, 0, 100]), ("Navy", [0, 0, 50]),
                                      ("Fuchsia", [100, 0, 100]), ("Purple", [50, 0, 50])]
        self.image_name = image_name
        self.image = cv2.imread(os.path.join(path, self.image_name), -1)
        self.bits_per_color_channel = bits_per_color_channel
        self.mean_color = None

    def compute_image_color_mean(self):
        """Parameters:
        returns - compute mean color
        """

        # check image dimensions1
        if self.image.ndim < 3:
            img_mean_blue_channel = img_mean_green_channel = img_mean_red_channel = np.mean(self.image[:, :])
        else:
            img_mean_blue_channel = np.mean(self.image[:, :, 0])  # get color mean - channel Blue
            img_mean_green_channel = np.mean(self.image[:, :, 1])  # get color mean - channel Green
            img_mean_red_channel = np.mean(self.image[:, :, 2])  # get color mean - channel Red

        # color channels in percent according to color depth
        img_mean_color = [(img_mean_red_channel / ((2 ** self.bits_per_color_channel) - 1)) * 100,
                          (img_mean_green_channel / ((2 ** self.bits_per_color_channel) - 1)) * 100,
                          (img_mean_blue_channel / ((2 ** self.bits_per_color_channel) - 1)) * 100]
        self.mean_color = img_mean_color
        return img_mean_color

    def select_webcolor_for_image(self):
        """Parameters:
        img_mean_color - average color value
        web_colors_definition - define web colors for selection
        returns - selected web color for image
        """
        if not self.mean_color:
            self.compute_image_color_mean()
        web_colors_definition_values = []
        # get values form tuple
        for values in self.web_colors_definition:
            web_colors_definition_values.append(values[1])
        web_colors = np.array(web_colors_definition_values)
        img_mean_color_np = np.array(self.mean_color)
        distances = np.sqrt(np.sum((web_colors - img_mean_color_np) ** 2, axis=1))
        smallest_distance_index = np.where(distances == np.amin(distances))
        smallest_distance_index = smallest_distance_index[0]
        smallest_distance = web_colors[smallest_distance_index]
        print(self.image_name, self.web_colors_definition[int(smallest_distance_index[0])][0], smallest_distance,
              img_mean_color_np)
        # return closest webcolor
        return self.web_colors_definition[int(smallest_distance_index[0])][0]


def check_path_and_img_input(path, image_name):
    """check if image can be read"""
    try:
        os.listdir(path)
    except OSError as error:
        print(error)
        raise

    img_path = os.path.join(path, image_name)
    image = cv2.imread(img_path, -1)
    if image is None:
        sys.exit("[Error]: Input is an invalid image or path is not correct")


def get_image_web_color():
    import pika
    queue_name = "m1_get_files_to_m2_compute"

    # establishing connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='host.docker.internal'))
    channel = connection.channel()

    # creating queue
    channel.queue_declare(queue=queue_name)

    #  Receiving messages from the queue - subscribing a callback function to a queue
    #  Note: Whenever message is received, this callback function is called by the Pika library
    def callback(ch, method, properties, body):
        received_path_image_name = body.decode('utf8')
        print(" [x] Received:", received_path_image_name, " => running module2")
        path_image_name = received_path_image_name.split(";")
        path_image_name_relative = path_image_name[0]
        path_image_name[0] = "docker-shared/" + path_image_name[0]
        # valid inputs, compute webcolor for the image
        check_path_and_img_input(path_image_name[0], path_image_name[1])
        image_24bit = ImageWebColor(path_image_name[0], path_image_name[1])
        selected_webcolor = image_24bit.select_webcolor_for_image()
        print("=> Selected webcolor: ", selected_webcolor, " for image: ", path_image_name[1])
        # create message
        queue_m2_to_m3 = "m2_compute_to_m3_save_images"
        channel.queue_declare(queue=queue_m2_to_m3)

        webcolor_path_image_name = [selected_webcolor, path_image_name_relative, path_image_name[1]]
        webcolor_path_image_name = ';'.join([str(elem) for elem in webcolor_path_image_name])
        message_webcolor_path_image_name = bytes(webcolor_path_image_name, 'utf8')
        # send message
        channel.basic_publish(exchange='', routing_key=queue_m2_to_m3, body=message_webcolor_path_image_name)
        print(" [x] Sent message with webcolor, path, image name:", message_webcolor_path_image_name.decode('utf8'))
        print("=> Module 2 finished...")
        print(' [*] Waiting for messages. To exit press CTRL+C')

    # Tell RabbitMQ that this particular callback function should receive messages from our hello queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    # Waits for data and runs callbacks whenever necessary
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        get_image_web_color()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

