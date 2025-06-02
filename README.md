# IR Overlays

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

## Project Overview

IR Overlays is a telemetry visualisation tool designed for use with IRacing. It provides real-time, customisable overlays that display useful telemetry data during gameplay. The application was built with a focus on performance, efficiency and user experience.

### Key Features

-   Overlays: Input Telemetry, Radar, and more.
-   Drag and drop overlays into desired positions.
-   Save overlay positions and configurations between sessions.
-   Developed using Python and the PySide6 GUI framework.

## Table of Contents

-   [Installation](#installation)
-   [Development Environment Setup](#development-environment-setup)
-   [Contributing](#contributing)
-   [License](#license)
-   [Contact](#contact)

## Installation

### Download Pre-built Release

To use IR Overlays without building from source:

1. Simply go to the [Releases](https://github.com/ajs/ir-overlays/releases) page.
2. Download the latest `.exe` file for Windows.
3. Run the executable file.

### Building from Source

To build IR Overlays from source:

#### Prerequisites

-   Python (v3.13.3 or later)

#### Build Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/ajs/ir-overlays.git
    cd ir-overlays
    ```

2. Create virtual environment and install dependencies:

    ```bash
    python -m venv venv
    venv/scripts/activate
    pip install -r requirements.txt
    ```

3. Install Pyinstaller:

    ```bash
    pip install pyinstaller
    ```

4. Run the build command:

    ```bash
    pyinstaller "IR Overlays.spec"
    ```

5. The built executable can be found in the `dist/` directory.

## Development Environment Setup

To set up the development environment for IR Overlays:

1. Ensure you have all prerequisites installed and virtual environment created (see [Building from Source](#building-from-source)).

2. Start the program:

    ```bash
    python src/main.py
    ```

## Contributing

Feel free to contribute improvements and submit pull requests.

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
