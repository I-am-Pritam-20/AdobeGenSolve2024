import unittest
import numpy as np
from src.regularize import is_straight_line, is_circle, is_rectangle

class TestRegularize(unittest.TestCase):
    def test_is_straight_line(self):
        line = np.array([[0, 0], [1, 1], [2, 2]])
        self.assertTrue(is_straight_line(line))

        not_line = np.array([[0, 0], [1, 1], [2, 3]])
        self.assertFalse(is_straight_line(not_line))

    def test_is_circle(self):
        t = np.linspace(0, 2*np.pi, 100)
        circle = np.column_stack((np.cos(t), np.sin(t)))
        self.assertTrue(is_circle(circle))

        not_circle = np.array([[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]])
        self.assertFalse(is_circle(not_circle))

    def test_is_rectangle(self):
        rectangle = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])
        self.assertTrue(is_rectangle(rectangle))

        not_rectangle = np.array([[0, 0], [1, 0], [1, 1], [0, 2]])
        self.assertFalse(is_rectangle(not_rectangle))

if __name__ == '__main__':
    unittest.main()