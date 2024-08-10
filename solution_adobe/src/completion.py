import numpy as np

def complete_curves(paths_XYs):
    completed = []
    for path in paths_XYs:
        for curve in path:
            if np.allclose(curve[0], curve[-1]):
                completed.append(curve)
            else:
                # Simple completion by connecting start and end points
                completed_curve = np.vstack([curve, curve[0]])
                completed.append(completed_curve)
    return completed