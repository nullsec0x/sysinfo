# SysInfo : System Monitoring tool for both UNIX and Windows

This is a simple system monitoring tool written in Python, utilizing the `psutil` and `rich` libraries to display real-time system information in a visually appealing terminal interface.

## Features

*   **Real-time Monitoring**: Displays CPU usage (overall and per-core), memory usage, swap usage, disk I/O, network I/O, and top processes by CPU.
*   **Interactive Interface**: Uses `rich` library for a dynamic and colorful terminal UI.
*   **Cute Emojis**: Incorporates fun emojis for a more engaging experience.
*   **CPU Usage Graph**: Provides a simple ASCII-style graph of CPU history.

## Requirements

To run this sysinfo.pyou need the following Python libraries:

*   `psutil`
*   `rich`

## Installation and Usage

### For Windows Users

#### 1. Install Python

First, you need to install Python on your Windows machine. It is recommended to download the latest stable version of Python 3 from the official Python website [1].

1.  **Download the Installer**: Visit the official Python website: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/). Look for the "Windows installer" for the latest Python 3 release (e.g., Python 3.10.x).

2.  **Run the Installer**: Once the installer (`.exe` file) is downloaded, double-click it to start the installation process.

3.  **Crucial Step: Add Python to PATH**: On the first screen of the installer, make sure to check the box that says "Add Python X.Y to PATH" (where X.Y is your Python version). This step is very important as it allows you to run Python commands from any directory in your Command Prompt or PowerShell.

    > "Adding Python to PATH makes it easier to run Python scripts from the command line. Without it, you would need to specify the full path to the Python executable every time you want to run a script." - Python Installation Guide

4.  **Proceed with Installation**: You can choose "Install Now" for a typical installation or "Customize installation" if you need to change the installation directory or select specific features. For most users, "Install Now" is sufficient.

5.  **Verify Installation**: After the installation is complete, open a new Command Prompt or PowerShell window and type the following commands to verify that Python and pip (Python's package installer) are installed correctly:

    ```cmd
    python --version
    pip --version
    ```

    You should see the installed Python version (e.g., `Python 3.10.5`) and pip version (e.g., `pip 22.0.4`). If you encounter an error like "'python' is not recognized as an internal or external command," it means Python was not added to your PATH correctly. In this case, you might need to reinstall Python and ensure the "Add Python to PATH" option is checked, or manually add it to your system's environment variables.

#### 2. Install Required Libraries

The System Monitor tool depends on two Python libraries: `psutil` and `rich`. These can be easily installed using `pip`.

1.  **Navigate to the Project Directory**: Open a Command Prompt or PowerShell window and navigate to the directory where you have saved the `sysinfo.py` and `requirements.txt` files. For example, if your files are in `C:\Users\YourUser\Documents\SysInfo`:

    ```cmd
    cd C:\Users\YourUser\Documents\SysInfo
    ```

2.  **Install Libraries**: Once in the correct directory, you can install the required libraries using the `requirements.txt` file provided with the tool:

    ```cmd
    pip install -r requirements.txt
    ```

    This command will read the `requirements.txt` file and install `psutil` and `rich` automatically. You should see output indicating that the packages are being downloaded and installed successfully.

    > "The `requirements.txt` file is a standard convention in Python projects for specifying dependencies. It ensures that everyone working on the project uses the same versions of libraries, preventing compatibility issues." - Python Packaging Authority (PyPA) Documentation

    If you prefer to install them individually, you can use:

    ```cmd
    pip install psutil rich
    ```

    Verify the installation by checking the installed packages (optional):

    ```cmd
    pip list
    ```

    You should see `psutil` and `rich` listed among the installed packages.

#### 3. Run the System Monitor

Once Python and the necessary libraries are installed, you can run the `sysinfo.py` script.

1.  **Open Command Prompt or PowerShell**: Ensure you are in the directory where `sysinfo.py` is located (as done in step 2.1).

2.  **Execute the Script**: Type the following command and press Enter:

    ```cmd
    python sysinfo.py
    ```

    The system monitor will start displaying real-time system information in your terminal. The `rich` library provides a visually enhanced output, so it's recommended to use a modern terminal like Windows Terminal or PowerShell for the best experience.

    > "Modern terminals offer better support for ANSI escape codes and Unicode characters, which are extensively used by libraries like `rich` to create rich and colorful text-based user interfaces." - Rich Library Documentation

### For Linux/macOS Users

#### 1. Install Required Libraries

Open your terminal and navigate to the directory where you have saved the `sysinfo.py` and `requirements.txt` files. Then, install the required libraries using pip:

```bash
pip install -r requirements.txt
```

#### 2. Run the System Monitor

Execute the `sysinfo.py` script from your terminal:

```bash
python3 sysinfo.py
```

Ensure your terminal supports ANSI escape codes for the best display.

## Configuration

The script can be configured to show or hide the CPU history graph and other charts by modifying the `show_charts_default` variable in `sysinfo.py`.

*   `show_charts_default = True`: Displays the CPU history graph, disk usage, network I/O, and process tables.
*   `show_charts_default = False`: Hides these charts, showing only the basic CPU, memory, and swap usage.

By default, the charts are now closed.

## Troubleshooting

*   **`python` command not found (Windows)**: If you see an error like `python is not recognized as an internal or external command`, it means Python was not added to your system's PATH environment variable. Refer back to Section "For Windows Users", Step "Install Python", or manually add Python to your PATH.
*   **`python3` command not found (Linux/macOS)**: Ensure Python 3 is installed and accessible in your PATH. You might need to use `python` instead of `python3` depending on your system configuration.
*   **ModuleNotFoundError**: If you encounter `ModuleNotFoundError: No module named 'psutil'` or `No module named 'rich'`, it indicates that the required libraries were not installed correctly. Ensure `pip install -r requirements.txt` ran without errors.
*   **Display Issues**: If the output looks garbled or lacks color, ensure you are using a modern terminal emulator (Windows Terminal, PowerShell, or a modern Linux/macOS terminal) and that your terminal supports ANSI escape codes.

## License

This project is open-source and available under the MIT License.

## Author

Nullsec0x

## References

[1] Python.org. *Download Python for Windows*. Available at: [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
