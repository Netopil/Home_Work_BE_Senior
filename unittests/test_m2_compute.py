from unittest import TestCase
import unittest


class TestImageWebColor(TestCase):
    def test_check_path_and_img_input(self):
        from m2_compute.m2_compute import check_path_and_img_input
        valid_path = "../img"
        invalid_path = "../imgfab7841"
        valid_image = "citrony.jpg"
        invalid_image = "citrony87465.jpg"

        self.assertTrue(check_path_and_img_input(valid_path, valid_image) is None)
        with self.assertRaises(SystemExit):
            check_path_and_img_input(valid_path, invalid_image)
        with self.assertRaises(Exception):
            check_path_and_img_input(invalid_path, valid_image)

    def test_compute_color_mean(self):
        from m2_compute.m2_compute import ImageWebColor
        path = "../img"

        self.assertEqual(ImageWebColor(path, "white.jpg").compute_image_color_mean(), [100, 100, 100])
        self.assertEqual(ImageWebColor(path, "aqua.png").compute_image_color_mean(), [0, 100, 100])
        self.assertEqual(ImageWebColor(path, "fuchsia.png").compute_image_color_mean(), [100, 0, 100])
        self.assertEqual(ImageWebColor(path, "yellow.png").compute_image_color_mean(), [100, 100, 0])
        # Navy [0 0 128] is actually in percent [0, 0, 50.19607843137255]
        self.assertEqual(ImageWebColor(path, "navy-blue.png").compute_image_color_mean(), [0, 0, 50.19607843137255])

    def test_select_webcolor_for_image(self):
        from m2_compute.m2_compute import ImageWebColor
        img_color_selection = ImageWebColor("../img", "aqua.jpg")
        img_color_selection.mean_color = [0, 75, 76]
        self.assertEqual(img_color_selection.select_webcolor_for_image(), 'Aqua')
        img_color_selection.mean_color = [0, 74, 75]
        self.assertEqual(img_color_selection.select_webcolor_for_image(), 'Teal')
        img_color_selection.mean_color = [75, 76, 0]
        self.assertEqual(img_color_selection.select_webcolor_for_image(), 'Yellow')
        img_color_selection.mean_color = [74, 75, 0]
        self.assertEqual(img_color_selection.select_webcolor_for_image(), 'Olive')
        img_color_selection.mean_color = [75, 0, 76]
        self.assertEqual(img_color_selection.select_webcolor_for_image(), 'Fuchsia')
        img_color_selection.mean_color = [74, 0, 75]
        self.assertEqual(img_color_selection.select_webcolor_for_image(), 'Purple')
        img_color_selection.mean_color = [87, 88, 89]
        self.assertEqual(img_color_selection.select_webcolor_for_image(), 'White')
        img_color_selection.mean_color = [88, 86, 87]
        self.assertEqual(img_color_selection.select_webcolor_for_image(), 'Silver')


if __name__ == '__main__':
    unittest.main()
