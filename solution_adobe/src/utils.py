import numpy as np
import matplotlib.pyplot as plt
import svgwrite


def save_plot(paths_XYs, filename):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    colours = ['red', 'green', 'blue', 'orange', 'purple', 'cyan']

    if isinstance(paths_XYs[0], np.ndarray):  # If it's a list of 2D arrays
        for i, XY in enumerate(paths_XYs):
            c = colours[i % len(colours)]
            ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
    else:  # If it's a list of lists of 2D arrays
        for i, XYs in enumerate(paths_XYs):
            c = colours[i % len(colours)]
            for XY in XYs:
                ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)

    ax.set_aspect('equal')

    plt.savefig(filename)
    plt.close(fig)

def plot(paths_XYs, filename=None):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    colours = ['red', 'green', 'blue', 'orange', 'purple', 'cyan']

    if isinstance(paths_XYs[0], np.ndarray):  # If it's a list of 2D arrays
        for i, XY in enumerate(paths_XYs):
            c = colours[i % len(colours)]
            ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
    else:
        for i, XYs in enumerate(paths_XYs):
            c = colours[i % len(colours)]
            for XY in XYs:
                ax.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)

    ax.set_aspect('equal')

    if filename:
        plt.savefig(filename)
        plt.close(fig)
    else:
        plt.show()


def read_csv(csv_path):
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    path_XYs = []
    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []
        for j in np.unique(npXYs[:, 0]):
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)
        path_XYs.append(XYs)
    return path_XYs





def polylines2svg(paths_XYs, svg_path):
    W, H = 0, 0

    def update_dimensions(XY):
        nonlocal W, H
        if XY.ndim == 2:
            W = max(W, np.max(XY[:, 0]))
            H = max(H, np.max(XY[:, 1]))
        elif XY.ndim == 1:
            W = max(W, XY[0])
            H = max(H, XY[1])

    if isinstance(paths_XYs[0], np.ndarray):  # If it's a list of 2D arrays
        for XY in paths_XYs:
            update_dimensions(XY)
    else:  # If it's a list of lists of 2D arrays
        for path_XYs in paths_XYs:
            for XY in path_XYs:
                update_dimensions(XY)

    padding = 0.1
    W, H = int(W + padding * W), int(H + padding * H)

    dwg = svgwrite.Drawing(svg_path, size=(f"{W}px", f"{H}px"))
    colours = ['red', 'green', 'blue', 'orange', 'purple', 'cyan']

    if isinstance(paths_XYs[0], np.ndarray):  # If it's a list of 2D arrays
        for i, XY in enumerate(paths_XYs):
            c = colours[i % len(colours)]
            points = [tuple(point) for point in XY]
            dwg.add(dwg.polyline(points=points, stroke=c, fill='none', stroke_width=2))
    else:  # If it's a list of lists of 2D arrays
        for i, path_XYs in enumerate(paths_XYs):
            c = colours[i % len(colours)]
            for XY in path_XYs:
                points = [tuple(point) for point in XY]
                dwg.add(dwg.polyline(points=points, stroke=c, fill='none', stroke_width=2))

    dwg.save()