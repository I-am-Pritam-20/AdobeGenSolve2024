import os
from src.utils import read_csv, save_plot, polylines2svg
from src.regularize import regularize_curves
from src.symmetry import detect_symmetry
from src.completion import complete_curves

def process_file(input_file, output_dir):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_svg = os.path.join(output_dir, f"{base_name}_output.svg")
    input_plot = os.path.join(output_dir, f"{base_name}_input_plot.png")
    output_plot = os.path.join(output_dir, f"{base_name}_output_plot.png")

    # Read input
    paths_XYs = read_csv(input_file)

    # Save input plot
    save_plot(paths_XYs, input_plot)

    # Regularize curves
    regularized = regularize_curves(paths_XYs)

    # Detect symmetry
    symmetries = detect_symmetry(regularized)

    # Complete curves
    completed = complete_curves(paths_XYs)

    # Save output plot
    save_plot(completed, output_plot)

    # Save as SVG
    polylines2svg(completed, output_svg)

    print(f"Processed {input_file}:")
    print(f"  Input plot saved as: {input_plot}")
    print(f"  Output plot saved as: {output_plot}")
    print(f"  Output SVG saved as: {output_svg}")
    print(f"  Detected symmetries: {symmetries}")
    print()

def main():
    input_dir = "examples"
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    csv_files = [f for f in os.listdir(input_dir) if f.endswith('.csv')]

    for csv_file in csv_files:
        input_file = os.path.join(input_dir, csv_file)
        process_file(input_file, output_dir)

if __name__ == "__main__":
    main()