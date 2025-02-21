from matplotlib import pyplot as plt


def plot_the_graph(outputFiles, input_file_directory , file_name="output.jpg"):
    data = [float(f.scf_done) for f in outputFiles if f.scf_done != "could not found"]
    plt.plot(data)
    plt.ylabel("Energy/AU")
    plt.xlabel("Step")
    plt.savefig(f"{input_file_directory}/" + file_name)
    plt.clf()


def plot_scatter(outputFiles, input_file_directory , file_name="scatter.jpg"):
    x_coords = []
    y_coords = []
    for index, j in enumerate(outputFiles):
        if j.is_converged == 0:
            x_coords.append(index+1)
            y_coords.append(float(j.scf_done))
            print(index,j.scf_done)

    plt.scatter(x_coords,y_coords)
    plt.ylabel("Energy/AU")
    plt.xlabel("Step")
    plt.savefig(f"{input_file_directory}/" + file_name)
    plt.clf()

