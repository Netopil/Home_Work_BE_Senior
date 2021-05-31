from unittest import TestCase
import unittest


class TestLoadSendImages(TestCase):
    def test_get_file_names(self):
        """Testing returned list of files according valid/invalid path and extensions"""

        from m1_get_files.m1_get_files import get_file_names
        valid_path = "../img"  # set valid path
        invalid_path = "../imgfab7841"
        invalid_extension = "jp871g"
        all_files = ['00ff00.png', 'Aeroklub_otazky.docx', 'aqua.png', 'black.jpg', 'black.png', 'blue.png',
                     'citrony.jpg', 'fuchsia.png', 'gray.jpg', 'gray.png', 'green.jpg', 'green.png', 'img_invalid.png',
                     'JanNetopilCV_ENG.pdf', 'lime2.jpg', 'maron.jpg', 'maroon.png', 'navy-blue.png', 'navy.jpg',
                     'olive.png', 'olive2.png', 'purple.png', 'red2.jpg', 'silver.png', 'teal.png', 'white.jpg',
                     'yellow.png']

        self.assertEqual(get_file_names(valid_path, "jpg"),
                         ['black.jpg', 'citrony.jpg', 'gray.jpg', 'green.jpg', 'lime2.jpg', 'maron.jpg', 'navy.jpg',
                          'red2.jpg', 'white.jpg'])
        self.assertEqual(get_file_names(valid_path, "pdf"), ["JanNetopilCV_ENG.pdf"])
        self.assertEqual(get_file_names(valid_path, "all"), all_files)
        self.assertEqual(get_file_names(valid_path, ""), all_files)
        self.assertEqual(get_file_names(valid_path, "jpg, png"),
                         ['00ff00.png', 'aqua.png', 'black.jpg', 'black.png', 'blue.png', 'citrony.jpg', 'fuchsia.png',
                          'gray.jpg', 'gray.png', 'green.jpg', 'green.png', 'img_invalid.png', 'lime2.jpg', 'maron.jpg',
                          'maroon.png', 'navy-blue.png', 'navy.jpg', 'olive.png', 'olive2.png', 'purple.png',
                          'red2.jpg', 'silver.png', 'teal.png', 'white.jpg', 'yellow.png'])
        self.assertEqual(get_file_names(valid_path), all_files)
        self.assertTrue(
            len(get_file_names(valid_path, "jpg, png, jp8855b")) > 0)  # correct path/folder, more extensions
        self.assertTrue(len(get_file_names(valid_path, "jpgg")) == 0)  # correct path/folder, incorrect extension
        self.assertTrue(len(get_file_names(valid_path, invalid_extension)) == 0)  # same if the folder is empty
        self.assertTrue(len(get_file_names(invalid_path, "jpg")) == 0)  # folder/path doesn't exist

    def test_get_valid_images(self):
        """Testing returned valid images according valid/invalid path and files"""

        from m1_get_files.m1_get_files import get_valid_images
        valid_path = "../img"  # should be set valid path
        invalid_path = "../aba46"  # add
        empty_file_list = ""
        file_list_valid_images = ["aqua.png", "black.jpg"]
        file_list_corupted_image = ["img_invalid.png"]
        file_list_valid_files = ["citrony.jpg", "JanNetopilCV_ENG.pdf", "Aeroklub_otazky.docx"]
        file_list_valid_invalid = ["citrony.jpg", "JanNe0478topilCV_ENG.pdf", "Aeroklub_otazky.docx"]
        file_list_invalid_images = ["aq187ua.png", "bl145ack.jpg"]
        file_list_invalid_files = ["Ja784nNetopilCV_ENG.pdf", "Aeroklub_otaz461ky.docx"]

        self.assertEqual(get_valid_images(valid_path, file_list_valid_images), ["aqua.png", "black.jpg"])
        self.assertEqual(get_valid_images(valid_path, file_list_valid_files), ["citrony.jpg"])

        self.assertTrue(len(get_valid_images(valid_path, file_list_valid_images)) > 0)  # image list isn't empty
        self.assertTrue(len(get_valid_images(valid_path, file_list_valid_files)) > 0)
        self.assertTrue(len(get_valid_images(valid_path, file_list_valid_invalid)) > 0)
        self.assertTrue(len(get_valid_images(valid_path, file_list_corupted_image)) == 0)  # empty image list
        self.assertTrue(len(get_valid_images(invalid_path, file_list_valid_files)) == 0)
        self.assertTrue(len(get_valid_images(valid_path, file_list_invalid_images)) == 0)
        self.assertTrue(len(get_valid_images(valid_path, file_list_invalid_files)) == 0)
        self.assertTrue(len(get_valid_images(valid_path, empty_file_list)) == 0)


if __name__ == '__main__':
    unittest.main()
