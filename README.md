# Adobe
For the Adobe GenSolve Hackathon
# Curvetopia

## Overview

This project provides a set of tools to process, analyze, and visualize curves described in CSV files. It includes functionalities for regularizing curves, detecting symmetries, completing curves, and saving the processed data as plots and SVG files.

## Project Structure

- `main.py`: The main script to process input CSV files and generate output plots and SVGs.
- `src/`: Contains the utility and core processing modules.
  - `utils.py`: Utility functions for reading CSVs, saving plots, and converting paths to SVGs.
  - `regularize.py`: Functions to regularize curves by identifying shapes like lines, circles, and rectangles.
  - `symmetry.py`: Functions to detect symmetries in regularized curves.
  - `completion.py`: Functions to complete curves by connecting their endpoints if necessary.

## Installation

### Prerequisites

- Python 3.x
- `numpy`: For numerical operations.
- `matplotlib`: For plotting curves.
- `svgwrite`: For saving curves as SVG files.
- `cairosvg`: For converting SVGs to other formats (if needed).

### Installation Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/ashutoshachary/Adobe.git
    cd Adobe
    cd solution_adobe
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required Python packages:

    ```bash
    pip install numpy matplotlib svgwrite cairosvg
    ```

## Usage

### Input Data

Input data should be in CSV format. Each CSV file should contain rows of points belonging to different paths. The format should be:


Where:
- `path_id` distinguishes different paths.
- `curve_id` distinguishes different curves within a path.
- `x`, `y` are the coordinates of the points.

### Running the Script

1. Place your CSV files in the `examples` directory.

2. Run the script:

    ```bash
    python main.py
    ```

3. The script will process each CSV file, generating plots and SVGs in the `output` directory.

### Output

For each input file, the following outputs are generated:

- **Input Plot**: Visual representation of the input paths (e.g., `input_plot.png`).
- **Output Plot**: Visual representation of the completed and regularized paths (e.g., `output_plot.png`).
- **Output SVG**: Scalable vector graphic representing the processed paths (e.g., `output.svg`).
- **Symmetry Detection**: Information about detected symmetries in the paths is printed to the console.

### Example

For a CSV file named `example.csv`, the following files will be generated:

- `output/example_input_plot.png`
- `output/example_output_plot.png`
- `output/example_output.svg`

### For Testing 
  ```bash
    cd tests
    python regularize.py
    ```

### Ignore
    main3.py

### main2.py
  More optimized solution for the Occlusion1 

