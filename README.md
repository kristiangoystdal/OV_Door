
# OV_Door

## Overview

OV_Door is a Python-based application for Windows, specifically designed for managing door access controls at Omega Verksted. This tool integrates seamlessly into the system tray of Windows computers, providing efficient and unobtrusive management of access controls with easy startup management.

## Features

- **System Tray Integration**: OV_Door operates from the system tray, allowing it to run quietly without disrupting your workflow.
- **User Interaction**: The application includes a user-friendly interface accessible via the system tray, facilitating easy management of access permissions.
- **Startup Management**: Ensures that OV_Door automatically launches upon system startup, providing consistent operability.

## Installation

### Prerequisites

- Compatible with Windows 10/11.

### Setup

1. Download the installer directly from [Omega Verksted Installer](https://example.com/omega_verksted_installer.exe).
2. Run `installer_omega_verksted.exe` to install the application. Make sure to check the box to launch the application after installation if desired.

### Running the Application

- Navigate to `C:\Program Files\Omega_Verksted` and run `Omega Verksted.exe`.
- To ensure the application runs at system startup, enable "Run at startup" by right-clicking the system tray icon and selecting the option.

## Contributing

We encourage community contributions! Please fork the repository and submit pull requests with your suggested changes.

### Building the Application

- For development and testing, use `BuildExe.bat` to compile the `main.py` file.
- The output will be placed in a folder named "Omega Verksted" within the `dist` directory. Ensure all files remain in the folder to maintain functionality.
