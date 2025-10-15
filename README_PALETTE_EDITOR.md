# Character Palette Editor

A graphical user interface (GUI) application for editing character palette configuration files based on the `SaveCharacterPalette.json` template.

## Quick Start

### Windows
1. Double-click `run_palette_editor.bat`
2. The script will automatically set up Python dependencies and launch the editor

### Linux/macOS
1. Open a terminal in the project directory
2. Run: `./run_palette_editor.sh`
3. The script will automatically set up Python dependencies and launch the editor

### Manual Launch
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python palette_editor.py
```

## Features

- **Visual Color Editing**: Color picker widgets for each region/setting in the palette
- **Live Preview**: Real-time 1024x1024 PNG texture preview showing the palette layout
- **Import/Export**: Open existing configurations, create new ones, and export PNGs
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **JSON-Based**: Uses the standard SaveCharacterPalette.json structure

## Installation

### Option 1: Run from Source

1. Install Python 3.9 or later
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python palette_editor.py
   ```

### Option 2: Download Pre-built Executable

Download the latest pre-built executable from the GitHub Actions artifacts (available for Windows, macOS, and Linux).

## Usage

### Opening a Configuration

1. Launch the application
2. Go to **File → Open** or **File → New**
3. Select a `SaveCharacterPalette.json` file or create a new one from the template

### Editing Colors

1. Each color region is displayed in the left panel with:
   - Region name (e.g., "Torso - Color 1 - Shade")
   - Color preview button (click to open color picker)
   - Hex color code input field
2. Click the color preview button to choose a color using the color picker dialog
3. Or manually enter a hex color code (e.g., #FF5733) in the input field
4. Press Enter or click outside the field to apply

### Viewing the Preview

1. The right panel shows a live preview of the generated 1024x1024 PNG texture
2. Each color region is rendered at its specified position and size
3. Click **Refresh Preview** to update the preview after making changes

### Saving Your Work

- **Save Configuration**: Go to **File → Save** to save changes to the current JSON file
- **Save As**: Go to **File → Save As** to save to a new JSON file
- **Export PNG**: Go to **File → Export PNG** to export the palette as a PNG image file

## Configuration Structure

The application works with `SaveCharacterPalette.json` which defines:

- **Regions**: Body parts and materials (Torso, Hips, Skin, etc.)
- **Colors**: Each region can have multiple color entries (Color 1, Color 2, etc.)
- **Variants**: Each color can have Shade and Highlight variants
- **Position**: Start X, Start Y, Width, Height define the region's position in the 1024x1024 texture
- **Color Values**: Hex color codes (e.g., #FF0000 for red)

Example structure:
```json
{
  "Torso": {
    "Start X": "0",
    "Start Y": "0",
    "Width": "64",
    "Height": "320",
    "Color": "",
    "Color 1": {
      "Start X": "0",
      "Start Y": "0",
      "Width": "32",
      "Height": "64",
      "Color": "#FF5733",
      "Shade": {
        "Start X": "32",
        "Start Y": "0",
        "Width": "32",
        "Height": "32",
        "Color": "#CC4522"
      }
    }
  }
}
```

## GitHub Actions Workflow

The project includes a GitHub Actions workflow (`.github/workflows/build-palette-editor.yml`) that:

1. **Builds the Application**: Creates standalone executables for Windows, macOS, and Linux
2. **Tests Multiple Python Versions**: Ensures compatibility with Python 3.9, 3.10, and 3.11
3. **Uploads Artifacts**: Makes the built executables available as workflow artifacts
4. **Creates Releases**: (Optional) Automatically creates GitHub releases when tags are pushed

### Running the Workflow

The workflow runs automatically:
- On push to the main branch
- On pull requests
- Manually via workflow_dispatch

To manually trigger the workflow:
1. Go to the **Actions** tab in the GitHub repository
2. Select **Build Character Palette Editor**
3. Click **Run workflow**

### Downloading Built Executables

After the workflow completes:
1. Go to the **Actions** tab
2. Click on the completed workflow run
3. Scroll down to **Artifacts**
4. Download the executable for your platform:
   - `CharacterPaletteEditor-Windows-Python3.x`
   - `CharacterPaletteEditor-macOS-Python3.x`
   - `CharacterPaletteEditor-Linux-Python3.x`

## Development

### Building from Source

To create a standalone executable locally:

```bash
# Install PyInstaller
pip install pyinstaller

# Build the application (Linux/macOS)
pyinstaller --onefile --windowed --name CharacterPaletteEditor \
  --add-data "SaveCharacterPalette.json:." \
  palette_editor.py

# Build the application (Windows)
pyinstaller --onefile --windowed --name CharacterPaletteEditor ^
  --add-data "SaveCharacterPalette.json;." ^
  palette_editor.py
```

The executable will be created in the `dist/` directory.

### Project Structure

```
.
├── palette_editor.py              # Main application source code
├── requirements.txt               # Python dependencies
├── SaveCharacterPalette.json      # Default palette template
├── .github/
│   └── workflows/
│       └── build-palette-editor.yml  # GitHub Actions workflow
└── README_PALETTE_EDITOR.md       # This file
```

## Requirements

- Python 3.9 or later
- Pillow (PIL) for image generation
- tkinter (included with Python)

## License

This project is part of the Blockbuster repository. See the main repository for license information.

## Troubleshooting

### "Template file SaveCharacterPalette.json not found"

Make sure the `SaveCharacterPalette.json` file is in the same directory as `palette_editor.py`.

### "Failed to generate preview"

Check that:
1. All color values are valid hex codes (e.g., #FF5733)
2. Position and size values in the JSON are valid integers
3. No regions exceed the 1024x1024 texture bounds

### Application won't start on macOS

If you downloaded a pre-built executable, you may need to grant permission:
```bash
xattr -cr CharacterPaletteEditor.app
```

### Application won't start on Linux

Make the executable file executable:
```bash
chmod +x CharacterPaletteEditor
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
