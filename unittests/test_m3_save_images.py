import unittest
from unittest import TestCase
import os
import shutil


class Test(TestCase):
    def test_check_color_and_image_input(self):
        from m3_save_images.m3_save_images import check_color_and_image_input
        valid_path = "../img"
        invalid_path = "../imgfab7841"
        valid_image = "citrony.jpg"
        invalid_image = "citrony87465.jpg"
        valid_image_color = "White"
        invalid_image_color = "White45781"

        # self.assertTrue(check_path_and_img-_input(valid_path, valid_image) is None)
        with self.assertRaises(Exception):
            check_color_and_image_input(invalid_path, valid_image, valid_image_color)
        with self.assertRaises(SystemExit):
            check_color_and_image_input(valid_path, invalid_image, valid_image_color)
        with self.assertRaises(SystemExit):
            check_color_and_image_input(valid_path, valid_image, invalid_image_color)
        self.assertTrue(check_color_and_image_input(valid_path, valid_image, valid_image_color) is None)

    def test_save_image(self):
        from m3_save_images.m3_save_images import save_images
        folder_destination_name = "Unittest_SortedImages"
        path_source = "../img"
        image_name = ["00ff00.png", "aqua.png", "black.jpg", "yellow.png", "red2.jpg", "green.jpg"]
        image_color = ["Lime", "Aqua", "Black", "Yellow", "Red", "Green"]
        # new empty folder is needed for testing save_image() function
        if os.path.isdir(folder_destination_name):
            shutil.rmtree(folder_destination_name)
        os.mkdir(folder_destination_name)
        # creating folders
        for i in range(0, 4):
            save_images(folder_destination_name, path_source, image_name[i], image_color[i])
            self.assertEqual(''.join(os.listdir(os.path.join(folder_destination_name, image_color[i]))), image_name[i])
        save_images(folder_destination_name, path_source, image_name[i], image_color[5])
        self.assertNotEqual(''.join(os.listdir(os.path.join(folder_destination_name, image_color[i]))), image_name[5])


if __name__ == '__main__':
    unittest.main()
