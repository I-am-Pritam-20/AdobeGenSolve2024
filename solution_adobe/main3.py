import numpy as np
import matplotlib.pyplot as plt
import svgwrite
import cairosvg
from sklearn.linear_model import LinearRegression
from scipy.interpolate import interp1d
from scipy.spatial.distance import cdist

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

def plot(paths_XYs, title='Shapes'):
    fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))
    for i, XYs in enumerate(paths_XYs):
        for XY in XYs:
            ax.plot(XY[:, 0], XY[:, 1], linewidth=2)
    ax.set_aspect('equal')
    ax.set_title(title)
    plt.show()

def polylines2svg(paths_XYs, svg_path):
    dwg = svgwrite.Drawing(svg_path, profile='tiny', shape_rendering='crispEdges')
    group = dwg.g()
    for path in paths_XYs:
        path_data = []
        for XY in path:
            path_data.append(("M", (XY[0, 0], XY[0, 1])))
            for j in range(1, len(XY)):
                path_data.append(("L", (XY[j, 0], XY[j, 1])))
            if not np.allclose(XY[0], XY[-1]):
                path_data.append(("Z", None))
        group.add(dwg.path(d=path_data, fill='none', stroke='black', stroke_width=2))
    dwg.add(group)
    dwg.save()
    cairosvg.svg2png(url=svg_path, write_to=svg_path.replace('.svg', '.png'))

def is_straight_line(points):
    X = points[:, 0].reshape(-1, 1)
    y = points[:, 1]
    model = LinearRegression().fit(X, y)
    return model.score(X, y) > 0.99

def is_circle(points):
    center = np.mean(points, axis=0)
    distances = np.linalg.norm(points - center, axis=1)
    return np.std(distances) < 0.05

def is_ellipse(points):
    center = np.mean(points, axis=0)
    distances = np.linalg.norm(points - center, axis=1)
    mean_distance = np.mean(distances)
    diff = distances - mean_distance
    variance = np.var(diff)
    return variance < 0.05

def is_rectangle(points):
    def angle_between(v1, v2):
        cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        cos_theta = np.clip(cos_theta, -1.0, 1.0)
        angle = np.arccos(cos_theta)
        return np.degrees(angle)

    vectors = np.diff(points, axis=0)
    vectors = np.vstack([vectors, vectors[0]])
    angles = [angle_between(vectors[i], vectors[i+1]) for i in range(len(vectors)-1)]
    right_angles = [angle for angle in angles if abs(angle - 90) < 10 or abs(angle - 270) < 10]
    return len(right_angles) == 4

def is_polygon(points):
    vectors = np.diff(points, axis=0)
    vectors = np.vstack([vectors, vectors[0]])
    angles = []
    for i in range(len(vectors)-1):
        v1 = vectors[i]
        v2 = vectors[i+1]
        angle = np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0])
        angle = np.degrees(angle) % 360
        angles.append(angle)
    mean_angle = np.mean(angles)
    return np.allclose(angles, mean_angle, atol=10)

def is_star(points):
    center = np.mean(points, axis=0)
    vectors = points - center
    angles = np.arctan2(vectors[:, 1], vectors[:, 0])
    angles = np.sort((angles + 2 * np.pi) % (2 * np.pi))
    diffs = np.diff(angles)
    mean_diff = np.mean(diffs)
    return np.allclose(diffs, mean_diff, atol=0.1)

def identify_shapes(paths):
    shapes = []
    for path in paths:
        if is_straight_line(path[0]):
            shapes.append('Straight Line')
        elif is_circle(path[0]):
            shapes.append('Circle')
        elif is_ellipse(path[0]):
            shapes.append('Ellipse')
        elif is_rectangle(path[0]):
            shapes.append('Rectangle')
        elif is_polygon(path[0]):
            shapes.append('Polygon')
        elif is_star(path[0]):
            shapes.append('Star')
        else:
            shapes.append('Unknown Shape')
    return shapes


def is_reflection_symmetric(points):
    midpoint = np.mean(points, axis=0)
    reflected_points = 2 * midpoint - points
    return np.allclose(points, reflected_points[::-1], atol=0.1)

def is_rotational_symmetric(points):
    center = np.mean(points, axis=0)
    angles = np.arctan2(points[:, 1] - center[1], points[:, 0] - center[0])
    return np.allclose(np.sort(angles), np.sort((angles + np.pi) % (2 * np.pi)), atol=0.1)

def identify_symmetry(paths):
    symmetries = []
    for path in paths:
        if is_reflection_symmetric(path[0]):
            symmetries.append('Reflection Symmetry')
        elif is_rotational_symmetric(path[0]):
            symmetries.append('Rotational Symmetry')
        else:
            symmetries.append('No Symmetry')
    return symmetries


def has_gaps(points):
    distances = cdist(points[:-1], points[1:])
    return np.any(distances > 1.0)

def fill_gaps(points):
    x = points[:, 0]
    y = points[:, 1]
    f = interp1d(x, y, kind='cubic')
    x_new = np.linspace(x.min(), x.max(), num=len(x)*10)
    y_new = f(x_new)
    return np.column_stack((x_new, y_new))

def complete_curves(paths):
    completed_paths = []
    for path in paths:
        if has_gaps(path[0]):
            completed_path = fill_gaps(path[0])
            completed_paths.append([completed_path])
        else:
            completed_paths.append(path)
    return completed_paths


def process_example(input_csv, output_csv, title):
    paths = read_csv(input_csv)
    print(f"Processing {input_csv}...")

    # Identify and regularize shapes
    shapes = identify_shapes(paths)
    print("Shapes Identified:", shapes)

    # Identify symmetry
    symmetries = identify_symmetry(paths)
    print("Symmetries Identified:", symmetries)

    # Complete curves
    completed_paths = complete_curves(paths)
    print("Completed Paths Processed.")

    # Visualize
    plot(completed_paths, title=title)

    # Save SVG
    svg_path = output_csv.replace('.csv', '.svg')
    polylines2svg(completed_paths, svg_path)
    print(f"SVG saved to {svg_path}")

    # Save output CSV
    with open(output_csv, 'w') as f:
        for i, path in enumerate(completed_paths):
            for XY in path:
                for point in XY:
                    f.write(f"{i},{point[0]},{point[1]}\n")
    print(f"Output CSV saved to {output_csv}")

def main():
    examples = [
        ("examples/frag0.csv", "frag0_sol.csv", "Fragmented Example 0"),
        ("examples/frag1.csv", "frag1_sol.csv", "Fragmented Example 1"),
        ("examples/frag2.csv", "frag2_sol.csv", "Fragmented Example 2"),
        ("examples/isolated.csv", "isolated_sol.csv", "Isolated Example"),
        ("examples/occlusion1.csv", "occlusion1_sol.csv", "Occlusion Example 1"),
        ("examples/occlusion2.csv", "occlusion2_sol.csv", "Occlusion Example 2")
    ]

    for input_csv, output_csv, title in examples:
        process_example(input_csv, output_csv, title)

if __name__ == "__main__":
    main()
