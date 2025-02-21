from random import uniform
from math import pi, cos, sin


def random_spherical_coordinates_generator(r: float):
    """ function generates coordinates that fits to the equation X^2 + Y^2 + Z^2 = R^2
    when input parameter radius was given
    :param r: radius of spherical coordinates (float)
    :return: coordinates of random spherical coordinates
    """
    x = uniform(-r, r)
    y_max = (r ** 2 - x ** 2) ** 0.5
    y = uniform(-y_max, y_max)
    z = (r ** 2 - x ** 2 - y ** 2) ** 0.5
    return x, y, z


def generate_random_point_on_sphere(r: float):
    """
    Generates a random point uniformly distributed on the surface of a sphere.

    :param r: Radius of the sphere (float).
    :return: A tuple (x, y, z) representing the coordinates of the random point on the sphere.
    """

    z = uniform(-r, r)
    phi = uniform(-2 * pi, 2 * pi)
    x = (r ** 2 - z ** 2) ** 0.5 * cos(phi)
    y = (r ** 2 - z ** 2) ** 0.5 * sin(phi)
    return x, y, z


def exact_equidistributed_point_generator(r, N):
    """
    this function returns a list of x,y,z symmetric coordinates with a length of N
    :param r:
    :param N:
    :return [[][]....]:
    """
    coordinates = []
    N_count = 0
    a = (4 * pi * r ** 2) / N
    d = a ** 0.5
    M_theta = round(pi / d)
    d_theta = pi / M_theta
    d_phi = a / d_theta

    for m in range(M_theta):
        theta = pi * (m + 0.5) / M_theta
        M_phi = round(2 * pi * sin(theta) / d_phi)
        for n in range(M_phi):
            phi = 2 * pi * n / d_phi
            coordinates.append(spherical_coordinates_to_xyz(r, theta, phi))
            N_count += 1
    return coordinates


def spherical_coordinates_to_xyz(r, theta, phi):
    x = r * sin(theta) * cos(phi)
    y = r * sin(theta) * sin(phi)
    z = r * cos(theta)
    return [x, y, z]


if __name__ == "__main__":
    print(exact_equidistributed_point_generator(2, 100))

