import numpy as np


def is_straight_line(points, tolerance=0.01):
    if len(points) < 3:
        return True

    vec1 = points[1] - points[0]
    for i in range(2, len(points)):
        vec2 = points[i] - points[0]
        if np.abs(np.cross(vec1, vec2)) > tolerance:
            return False
    return True


def is_circle(points, tolerance=0.01):
    if len(points) < 5:
        return False

    center = np.mean(points, axis=0)
    radii = np.linalg.norm(points - center, axis=1)
    return np.std(radii) / np.mean(radii) < tolerance


def is_rectangle(points, tolerance=0.01):
    if len(points) != 4:
        return False

    edges = np.roll(points, -1, axis=0) - points
    lengths = np.linalg.norm(edges, axis=1)
    angles = np.abs(np.degrees(np.arctan2(edges[:, 1], edges[:, 0])) % 90)

    return (np.std(lengths[:2]) / np.mean(lengths[:2]) < tolerance and
            np.std(lengths[2:]) / np.mean(lengths[2:]) < tolerance and
            np.all(np.abs(angles - 45) < tolerance * 90))


def regularize_curves(paths_XYs):
    regularized = []
    for path in paths_XYs:
        for curve in path:
            if is_straight_line(curve):
                regularized.append(('line', curve[0], curve[-1]))
            elif is_circle(curve):
                center = np.mean(curve, axis=0)
                radius = np.mean(np.linalg.norm(curve - center, axis=1))
                regularized.append(('circle', center, radius))
            elif is_rectangle(curve):
                regularized.append(('rectangle', curve))
            else:
                regularized.append(('polyline', curve))
    return regularized