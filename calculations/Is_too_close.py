def is_too_close_spherical(atoms1, atoms2, stop_distance_fac):
    """
    Checks if any two atoms from two different molecules are too close to each other.

    This function compares the distances between all pairs of atoms from two different molecules.
    If any pair of atoms is within a critical distance — determined by the sum of their covalent
    radii scaled by `stop_distance_fac` — the function returns False, indicating that the atoms are
    too close. Otherwise, it returns True.

    :param atoms1: A list of `Atom` objects from the first molecule.
    :param atoms2: A list of `Atom` objects from the second molecule.
    :param stop_distance_fac: A scaling factor to adjust the threshold distance for considering atoms
                              as too close (float).
    :return: True if no atoms are too close; False if any atoms are within the critical distance.
    """
    for i in atoms1:
        for j in atoms2:
            if i.distance_between(j) < (
                    i.c_radius + j.c_radius) * stop_distance_fac:
                # Debugging output: prints the distance and the atoms that are too close
                #print(i.distance_between(j), i, j)
                return False
    return True




def is_not_highly_repulsive_spherically(sys, stop_distance_fac=0.5):
    """
    Checks if the atoms of different molecules in the system are not too close to each other.

    This function iterates through all pairs of molecules in the system and verifies
    that no two atoms from different molecules are within a highly repulsive distance.
    The check is performed using a spherical distance criterion with a scaling factor.

    :param sys: The system object containing a list of molecules.
    :param stop_distance_fac: A scaling factor to adjust the threshold distance for repulsion (float).
                              Default is 0.5.
    :return: True if no atoms are within the highly repulsive distance; False otherwise.
    """
    for molecule_1 in sys.molecules:
        for molecule_2 in sys.molecules:
            if molecule_2 == molecule_1:
                # Skip comparing the molecule with itself
                continue
            if not is_too_close_spherical(molecule_2.atoms, molecule_1.atoms, stop_distance_fac):
                return False

    return True



