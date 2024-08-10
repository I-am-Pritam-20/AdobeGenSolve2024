import numpy as np


def find_symmetry_axis(points):
    center = np.mean(points, axis=0)
    centered = points - center

    angles = np.linspace(0, np.pi, 180)
    best_angle = 0
    min_error = float('inf')

    for angle in angles:
        rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                    [np.sin(angle), np.cos(angle)]])
        rotated = np.dot(centered, rotation_matrix.T)
        error = np.sum(np.abs(rotated[:, 1]))
        if error < min_error:
            min_error = error
            best_angle = angle

    return best_angle


def detect_symmetry(regularized_curves):
    symmetries = []
    for curve_type, *params in regularized_curves:
        if curve_type in ['circle', 'line']:
            symmetries.append(('radial', params))
        elif curve_type in ['rectangle', 'polyline']:
            points = params[0] if curve_type == 'rectangle' else params
            axis_angle = find_symmetry_axis(points)
            symmetries.append(('reflection', axis_angle))
    return symmetries