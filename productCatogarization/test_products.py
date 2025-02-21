import unittest
from unittest.mock import MagicMock
from catogarize_products import products_writer, Atom, Molecule, get_atom_list, get_molecules


class TestMoleculeFunctions(unittest.TestCase):

    def test_get_atom_list(self):
        products = products_writer()
        symbols = ['H', 'O', 'H']
        opt_coords = [(0, 0, 0), (0, 1, 0), (1, 0, 0)]

        atom_list = get_atom_list(symbols, opt_coords)

        self.assertEqual(len(atom_list), 3, "Expected 3 atoms in the list")
        self.assertEqual(atom_list[0].symbol, 'H')
        self.assertEqual(atom_list[1].symbol, 'O')
        self.assertEqual(atom_list[2].symbol, 'H')

    def test_find_the_formation_of_products(self):
        # Mocking outputfile_list with objects having is_converged and scf_done properties
        products = products_writer()
        mock_file_1 = MagicMock(is_converged=0, scf_done=5)
        mock_file_2 = MagicMock(is_converged=1, scf_done=3)
        mock_file_3 = MagicMock(is_converged=0, scf_done=2)

        file_list = [mock_file_1, mock_file_2, mock_file_3]

        index = products.find_the_formation_of_products(file_list)
        self.assertEqual(index, 2, "Expected index 2 as the minimum energy point")

    def test_get_molecules(self):
        products=products_writer()
        atom1 = Atom('H', 0, 0, 0)
        atom2 = Atom('H', 0, 0, 1)
        atom3 = Atom('O', 3, 0, 0)
        atom4 = Atom('C', 0, 10, 0)

        atoms = [atom1, atom2, atom3, atom4]

        # Assuming get_molecules uses the distance and c_radius properties to group atoms into molecules
        molecules = get_molecules(atoms, factor=1)

        self.assertEqual(len(molecules), 3, "Expected 3 molecules formed")
        molecule_sizes = sorted([len(molecule.atoms) for molecule in molecules])
        self.assertEqual(molecule_sizes, [1, 1, 2], "Expected molecule sizes [1, 1, 2]")

    def test_add_products(self):
        # Mocking atoms and outputfile_list
        products = products_writer()
        mock_atom1 = Atom('H', 0, 0, 0)
        mock_atom2 = Atom('H', 0, 0, 1)
        atom_symbols = [mock_atom1.symbol,mock_atom2.symbol]

        mock_outputfile = MagicMock()
        mock_outputfile.opt_coords = [[0, 0, 0], [0, 0, 1]]
        mock_outputfile.is_converged = 0
        mock_outputfile.scf_done = 5
        outputfile_list = [mock_outputfile]

        # Mocking the methods used inside add_products
        find_the_formation_of_products = MagicMock(return_value=0)
        Molecule.calculate_RMSD = MagicMock(return_value=0.1)

        products.add_products(atom_symbols, outputfile_list)

        Molecule.calculate_RMSD.assert_called()  # Ensure calculate_RMSD was called

if __name__ == '__main__':
    unittest.main()
