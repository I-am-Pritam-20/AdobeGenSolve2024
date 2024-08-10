import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev
from shapely.geometry import Polygon, Point
import csv
import svgwrite


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


def complete_curve(points, occluder):
    occluder_poly = Polygon(occluder[0])

    intersection_points = []
    for i in range(len(points)):
        if occluder_poly.contains(Point(points[i])):
            intersection_points.append(i)

    if len(intersection_points) != 2:
        return points

    start, end = intersection_points

    t = np.linspace(0, 1, 100)
    x = np.linspace(points[start][0], points[end][0], 100)
    y = (points[start][1] + points[end][1]) / 2 + (points[end][1] - points[start][1]) / 2 * np.sin(np.pi * t)

    completed_curve = np.vstack((points[:start + 1], np.column_stack((x, y)), points[end:]))

    return completed_curve


def save_csv(path_XYs, csv_path):
    with open(csv_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i, XYs in enumerate(path_XYs):
            for j, XY in enumerate(XYs):
                for k, point in enumerate(XY):
                    writer.writerow([i, j, k, point[0], point[1]])


def polylines2svg(paths_XYs, svg_path):
    W, H = 0, 0
    for path_XYs in paths_XYs:
        for XY in path_XYs:
            W, H = max(W, np.max(XY[:, 0])), max(H, np.max(XY[:, 1]))
    padding = 0.1
    W, H = int(W + padding * W), int(H + padding * H)

    dwg = svgwrite.Drawing(svg_path, profile='tiny', size=(W, H))

    colours = ['blue', 'red', 'green', 'yellow', 'purple', 'orange']  # Add more colors if needed

    for i, path in enumerate(paths_XYs):
        c = colours[i % len(colours)]
        for XY in path:
            points = [(x, y) for x, y in XY]
            dwg.add(dwg.polyline(points=points, stroke=c, fill='none', stroke_width=2))

    dwg.save()


def plot_and_save_png(path_XYs, png_path):
    plt.figure(figsize=(10, 10))
    colours = ['blue', 'red', 'green', 'yellow', 'purple', 'orange']  # Add more colors if needed
    for i, path in enumerate(path_XYs):
        c = colours[i % len(colours)]
        for XY in path:
            plt.plot(XY[:, 0], XY[:, 1], c=c, linewidth=2)
    plt.axis('equal')
    plt.axis('off')
    plt.savefig(png_path, bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close()


# Read the input CSV
input_path = "examples/occlusion1.csv"
path_XYs = read_csv(input_path)

# Assuming the first curve is the occluded one and the second is the occluder
occluded_curve = path_XYs[0][0]
occluder = path_XYs[1]

# Complete the curve
completed_curve = complete_curve(occluded_curve, occluder)

# Replace the original curve with the completed one
path_XYs[0] = [completed_curve]

# Save the result as CSV
output_csv_path = "occlusion1_sol.csv"
save_csv(path_XYs, output_csv_path)

# Generate SVG
output_svg_path = "occlusion1_sol.svg"
polylines2svg(path_XYs, output_svg_path)

# Generate PNG
output_png_path = "occlusion1_sol.png"
plot_and_save_png(path_XYs, output_png_path)

# Visualization
plt.figure(figsize=(10, 10))
plt.plot(occluded_curve[:, 0], occluded_curve[:, 1], 'b-', label='Original')
plt.plot(completed_curve[:, 0], completed_curve[:, 1], 'r-', label='Completed')
plt.plot(occluder[0][:, 0], occluder[0][:, 1], 'g-', label='Occluder')
plt.legend()
plt.axis('equal')
plt.show()

print(f"Results saved as {output_csv_path}, {output_svg_path}, and {output_png_path}")