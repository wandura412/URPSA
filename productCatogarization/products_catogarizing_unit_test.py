from catogarize_products import *
import unittest


class TestGetMolecules(unittest.TestCase):

    def test_simple_molecules(self):
        products = products_writer()
        atom1 = Atom('H', 0, 0, 0)
        atom2 = Atom('H', 0, 0, 1)
        atom3 = Atom('O', 3, 0, 0)
        atom4 = Atom('O', 3, 0, 0.5)
        atom5 = Atom('C', 0, 10, 0)

        atoms = [atom1, atom2, atom3, atom4, atom5]

        molecules_list = get_molecules(atoms)

        # Expecting 3 molecules: one with two H atoms, one with two O atoms, and one with one C atom
        self.assertEqual(len(molecules_list), 3, f"Expected 3 molecules, got {len(molecules_list)}")

        molecule_sizes = sorted([len(molecule.atoms) for molecule in molecules_list])
        self.assertEqual(molecule_sizes, [1, 2, 2], f"Expected molecule sizes [1, 2, 2], got {molecule_sizes}")

    def test_complex_molecules(self):
        products =products_writer()
        atom1 = Atom('H', 0, 0, 0)
        atom2 = Atom('H', 0, 0, 1)
        atom3 = Atom('O', 0.5, 0.5, 1.5)
        atom4 = Atom('C', 3, 0, 0)
        atom5 = Atom('O', 3, 0, 0.5)
        atom6 = Atom('C', 0, 10, 0)
        atom7 = Atom('N', 0, 10.1, 0)
        atom8 = Atom('N', 4, 4, 4)
        atom9 = Atom('O', 4.5, 4.5, 4)
        atom10 = Atom('H', 4.8, 4.2, 4.1)

        atoms = [atom1, atom2, atom3, atom4, atom5, atom6, atom7, atom8, atom9, atom10]

        molecules_list = get_molecules(atoms)

        # Expecting 4 molecules: H2O molecule, CO molecule, CN molecule, and an NOH molecule
        self.assertEqual(len(molecules_list), 4, f"Expected 4 molecules, got {len(molecules_list)}")

        molecule_sizes = sorted([len(molecule.atoms) for molecule in molecules_list])
        self.assertEqual(molecule_sizes, [2, 2, 3, 3], f"Expected molecule sizes [2, 2, 3, 3], got {molecule_sizes}")

    def test_edge_cases(self):
        # Edge case: No atoms
        products = products_writer()
        atoms = []
        molecules_list = get_molecules(atoms)
        self.assertEqual(len(molecules_list), 0, f"Expected 0 molecules, got {len(molecules_list)}")

        # Edge case: All atoms too far apart to form molecules
        atom1 = Atom('H', 0, 0, 0)
        atom2 = Atom('H', 100, 100, 100)
        atom3 = Atom('O', 200, 200, 200)
        atoms = [atom1, atom2, atom3]

        molecules_list = get_molecules(atoms)
        self.assertEqual(len(molecules_list), 3, f"Expected 3 separate molecules, got {len(molecules_list)}")

        molecule_sizes = sorted([len(molecule.atoms) for molecule in molecules_list])
        self.assertEqual(molecule_sizes, [1, 1, 1], f"Expected molecule sizes [1, 1, 1], got {molecule_sizes}")


class TestMoleculeFormation(unittest.TestCase):
    def test_molecule_from_coordinates2(self):
        products = products_writer()
        symbols = ['C', 'H', 'H', 'H', 'O', 'H', 'O', 'H']

        coords = [
            [1.9989194392671017, -0.6974175886799965, -2.8895532101609014],
            [1.3971087785500642, -1.2191601656228386, -3.6040520585669413],
            [1.532239234627327, -0.7446639082910222, -1.9278477645062655],
            [2.0997315143987607, 0.3253896887438954, -3.187214425185779],
            [3.29217298163273, -1.3039227321606635, -2.8221231957938233],
            [3.710559294914875, -1.2633094498311261, -3.685201095786477],
            [2.532199242017326, 2.743692951660752, -1.167543447020905],
            [2.0525833273988887, 1.9135880116385722, -1.2174869611459513]
        ]

        # Create atoms list

        atom_list = get_atom_list(symbols, coords)

        # Call get_molecules function
        molecules = get_molecules(atom_list, factor=1)

        # Assert on the number of molecules formed
        self.assertEqual(2, len(molecules), "Expected 2 molecules formed")

        # Optionally, assert on the size of each molecule
        molecule_sizes = sorted([len(molecule.atoms) for molecule in molecules])
        self.assertEqual(molecule_sizes, [2, 6], "Expected molecule sizes [2, 6]")

    def test_molecule_from_coordinates(self):
        products =products_writer()
        symbols = ['C', 'H', 'H', 'H', 'O', 'H', 'O', 'H']
        coords = [
            [0.369834, -0.573473, -1.337132],
            [0.982651, -1.172145, -0.668343],
            [-0.198803, 0.081156, -0.670123],
            [-0.243845, -1.115621, -1.980938],
            [1.273922, 0.327655, -2.170902],
            [2.206966, 0.270497, -1.853989],
            [1.639825, 0.274872, 0.050053],
            [1.22628, 0.652853, -0.799916]
        ]

        # Create atoms list
        atom_list = get_atom_list(symbols, coords)

        # Call get_molecules function
        molecules = get_molecules(atom_list, factor=0.9)

        # Assert on the number of molecules formed
        self.assertEqual(1, len(molecules), "Expected 2 molecules formed")

        # Optionally, assert on the size of each molecule
        molecule_sizes = sorted([len(molecule.atoms) for molecule in molecules])
        self.assertEqual(molecule_sizes, [8], "Expected molecule sizes [2, 6]")


if __name__ == '__main__':
    unittest.main()

