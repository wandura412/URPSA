import unittest
import numpy as np
from molecule import Molecule
from atoms.atoms import Atom

class TestMolecule(unittest.TestCase):

    def setUp(self):
        # Define some sample atoms for testing
        self.atom1 = Atom("H", 0, 0, 0)
        self.atom2 = Atom("O", 1, 1, 1)
        self.atom3 = Atom("H", 2, 2, 2)

        # Create a molecule with these atoms
        self.molecule = Molecule([self.atom1, self.atom2, self.atom3])

    def test_rotation_xy(self):
        # Apply rotation around XY plane by pi/2
        rotated_xyz = self.molecule.rotation_xy(np.pi / 2)

        # Assert that the rotated coordinates are as expected
        expected_rotated_xyz = np.array([
            [0, 0, 0],
            [-1, 1, 1],
            [-2, 2, 2]
        ])
        np.testing.assert_array_almost_equal(rotated_xyz.xyz, expected_rotated_xyz)

    def test_rotation_yz(self):
        # Apply rotation around YZ plane by pi/2
        rotated_xyz = self.molecule.rotation_yz(np.pi / 2)

        # Assert that the rotated coordinates are as expected
        expected_rotated_xyz = np.array([
            [0, 0, 0],
            [1, 1, -1],
            [2, 2, -2]
        ])
        np.testing.assert_array_almost_equal(rotated_xyz.xyz, expected_rotated_xyz)

    def test_rotation_xz(self):
        # Apply rotation around XZ plane by pi/2
        rotated_xyz = self.molecule.rotation_xz(np.pi / 2)

        # Assert that the rotated coordinates are as expected
        expected_rotated_xyz = np.array([
            [0, 0, 0],
            [1, 1, -1],
            [2, 2, -2]
        ])
        np.testing.assert_array_almost_equal(rotated_xyz.xyz, expected_rotated_xyz)

    def test_translation_x(self):
        # Apply translation along X-axis by 2 units
        translated_xyz = self.molecule.translation_x(2)

        # Assert that the translated coordinates are as expected
        expected_translated_xyz = np.array([
            [2, 0, 0],
            [3, 1, 1],
            [4, 2, 2]
        ])
        np.testing.assert_array_almost_equal(translated_xyz.xyz, expected_translated_xyz)

    def test_translation_y(self):
        # Apply translation along Y-axis by 2 units
        translated_xyz = self.molecule.translation_y(2)

        # Assert that the translated coordinates are as expected
        expected_translated_xyz = np.array([
            [0, 2, 0],
            [1, 3, 1],
            [2, 4, 2]
        ])
        np.testing.assert_array_almost_equal(translated_xyz.xyz, expected_translated_xyz)

    def test_translation_z(self):
        # Apply translation along Z-axis by 2 units
        translated_xyz = self.molecule.translation_z(2)

        # Assert that the translated coordinates are as expected
        expected_translated_xyz = np.array([
            [0, 0, 2],
            [1, 1, 3],
            [2, 2, 4]
        ])
        np.testing.assert_array_almost_equal(translated_xyz.xyz, expected_translated_xyz)


if __name__ == '__main__':
    unittest.main()

