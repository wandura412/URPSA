import unittest
import numpy as np

from calculations.random_spherical_coords_generator import random_spherical_coordinates_generator
from spherical_grid_coordinates import spherically_converge_to_center
from atoms.atoms import Atom


class TestSphericallyConvergeAtom(unittest.TestCase):

    def test_converge_towards_origin(self):
        atom = Atom("Si", 1, 0, 0)  # Assuming initial coordinates
        size = 1
        new_position = spherically_converge_to_center(atom, size)
        expected_position = np.array([0, 0, 0])
        np.testing.assert_array_almost_equal(new_position, expected_position)

    def test_converge_atom_movement(self):
        atom = Atom("Si", 5, 5, 5)  # Assuming initial coordinates
        size = 2
        new_position = spherically_converge_to_center(atom, size)
        self.assertEqual(atom.get_coords(), new_position.tolist())

    def test_new_radius(self):

        atom = Atom("Si", *random_spherical_coordinates_generator(10))  # Assuming initial coordinates
        size = 2
        spherically_converge_to_center(atom, size)
        self.assertAlmostEqual(8, atom.distance_from_origin())

    def test_converge_with_zero_size(self):
        atom = Atom("Si", 2, 2, 2)  # Assuming initial coordinates
        size = 0
        new_position = spherically_converge_to_center(atom, size)
        self.assertEqual(atom.get_coords(), new_position.tolist())


if __name__ == '__main__':
    unittest.main()

