import unittest
from calculations.random_spherical_coords_generator import random_spherical_coordinates_generator


class TestRandomSphericalCoordinatesGenerator(unittest.TestCase):

    def test_boundary_min_radius(self):
        x, y, z = random_spherical_coordinates_generator(0)
        self.assertAlmostEqual(x, 0)
        self.assertAlmostEqual(y, 0)
        self.assertAlmostEqual(z, 0)

    def test_boundary_large_radius(self):
        radius = 1000
        x, y, z = random_spherical_coordinates_generator(radius)
        self.assertTrue(-radius <= x <= radius)
        self.assertTrue(-radius <= y <= radius)
        self.assertTrue(-radius <= z <= radius)

    def test_zero_radius(self):
        x, y, z = random_spherical_coordinates_generator(1)
        self.assertTrue(-1 <= x <= 1)
        self.assertTrue(-1 <= y <= 1)
        self.assertTrue(-1 <= z <= 1)

    def test_repeated_calls(self):
        radius = 5.1
        for _ in range(10):
            x1, y1, z1 = random_spherical_coordinates_generator(radius)
            x2, y2, z2 = random_spherical_coordinates_generator(radius)
            self.assertNotAlmostEqual(x1, x2)
            self.assertNotAlmostEqual(y1, y2)
            self.assertNotAlmostEqual(z1, z2)

    def test_equation_satisfaction(self):
        radius = 10.5
        x, y, z = random_spherical_coordinates_generator(radius)
        self.assertAlmostEqual(x ** 2 + y ** 2 + z ** 2, radius ** 2, places=9)


if __name__ == '__main__':
    unittest.main()
