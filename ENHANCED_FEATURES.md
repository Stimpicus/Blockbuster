# Enhanced Palette Editor Features

This document describes the new features added to the Character Palette Editor.

## New Features

### 1. Hex Code Input for Group-Level Colors

**What it does:** Adds hex input fields alongside color picker buttons for group-level color selections (Clothing and Attachments groups).

**How to use:**
1. Locate a group header (e.g., "Clothing" or "Attachments")
2. You'll see "Group Colors:" with C1 through C5 buttons
3. Each button now has a small text field next to it
4. You can either:
   - Click the color button to use the color picker dialog
   - Type a hex color code directly (e.g., `#ff0000` or `ff0000`)
   - Press Enter or click elsewhere to apply

**Benefits:**
- Faster color entry when you know the exact hex code
- Easier to copy/paste colors between projects
- More precise color control

### 2. Group-Level Color Updates

**What it does:** When you select a color at the group level, it now properly updates and saves all lower-tier (individual region) color values.

**How it works:**
1. Select a group color (e.g., Color 1 for "Clothing")
2. The color is applied to ALL items in that group (Torso, Arm Attire Left, etc.)
3. Shade and Highlight colors are automatically calculated
4. All UI widgets update visually to show the new colors
5. Changes are saved to the configuration

**Visual Feedback:**
- The group-level color button background changes to the selected color
- All individual region color buttons update
- All hex input fields update
- The preview updates immediately

### 3. Import Texture PNG

**What it does:** Allows you to import an existing texture PNG and automatically extract the dominant color from each defined region.

**How to use:**
1. Go to **File → Import Texture PNG...**
2. Select a PNG file (preferably 1024x1024)
3. The application will:
   - Analyze each defined region in the configuration
   - Calculate the dominant color (most frequently occurring)
   - Exclude pure black (#000000) and pure white (#ffffff)
   - Update all color fields with the detected colors
4. Review the results and make any manual adjustments needed

**Use Cases:**
- Starting from an existing texture
- Copying a color scheme from another texture
- Quickly prototyping variations of existing designs

**Technical Details:**
- Uses pixel-by-pixel analysis within each region's boundaries
- Counts color occurrences using a histogram
- Selects the most common color that isn't black or white
- Updates both the internal data and UI widgets

### 4. Enhanced UI Synchronization

**What it does:** Ensures all UI elements stay in sync when colors change, whether from:
- Color picker dialog
- Hex input field
- Group-level color selection
- Imported texture

**Improvements:**
- Color buttons always show current color
- Hex input fields always show current hex code
- Shade and Highlight auto-update when base colors change
- Preview updates in real-time

## Feature Retention

All previous features remain intact:

✓ Grouped/Collapsed UI for Clothing and Attachments
✓ Auto-calculation of Shade and Highlight colors
✓ Live PNG preview (1024x1024)
✓ Configuration file import/export (JSON)
✓ PNG export

## Code Changes Summary

### Files Modified
- `palette_editor.py` - Main application code

### Key Changes

1. **Added imports:**
   - `Counter` from collections for dominant color detection

2. **Enhanced ColorEntry class:**
   - Added `widgets` property to store (button, entry) tuple
   - Enables direct UI updates without searching for widgets

3. **Updated group color picker creation:**
   - Added hex input fields for each group color
   - Stored widget references in `group_color_widgets` dict
   - Bound Enter and FocusOut events to update handler

4. **Enhanced color update methods:**
   - `apply_group_color()` - Applies color to all group items and updates UI
   - `update_group_color_from_entry()` - Handles hex input for group colors
   - `update_color_widgets()` - Helper to update UI widgets for given paths
   - `choose_color()` - Now updates shade/highlight UI widgets
   - `update_color_from_entry()` - Now updates shade/highlight UI widgets

5. **Added import texture feature:**
   - `import_texture()` - Main method for importing and analyzing PNG
   - Uses PIL to load and analyze image
   - Extracts dominant color per region
   - Excludes black and white colors
   - Updates all affected UI widgets

6. **Menu updates:**
   - Added "Import Texture PNG..." to File menu

## Testing

### Unit Tests
Run `test_enhancements.py` to verify:
- Color calculation functions (shade/highlight)
- Dominant color extraction algorithm
- Configuration structure validation

```bash
python test_enhancements.py
```

### Demo Script
Run `demo_palette_editor.py` to see a demonstration:
- Creates a sample configuration with colors
- Generates a PNG texture from the configuration
- Shows shade/highlight calculations

```bash
python demo_palette_editor.py
```

## Usage Examples

### Example 1: Setting Colors for a Group
```
1. Expand "Clothing" group
2. In the group header, find "C1" (Color 1)
3. Click the color button or type "#ff0000" in the hex field
4. All Clothing items (Torso, Arms, Legs, etc.) get red as Color 1
5. Shades and highlights auto-calculate
6. Save the configuration
```

### Example 2: Importing from Existing Texture
```
1. Open or create a configuration
2. Go to File → Import Texture PNG...
3. Select your existing texture file
4. Review the imported colors
5. Make manual adjustments as needed
6. Save the configuration
7. Export as PNG if desired
```

### Example 3: Quick Color Copy
```
1. Select a color in one field
2. Copy the hex code from the text field
3. Paste into other hex fields
4. Press Enter to apply
```

## Technical Notes

### Color Exclusion Logic
When importing textures, the application excludes:
- `#000000` (pure black) - Often used as empty/transparent
- `#ffffff` (pure white) - Often used as empty/transparent

This ensures meaningful colors are detected rather than background colors.

### Dominant Color Algorithm
1. Extract all pixels in a region
2. Convert each pixel to hex format
3. Filter out black and white
4. Count occurrences of each color
5. Return the most common color

### Auto-Calculation
When a base color (Color 1-5) is set:
- **Shade**: Reduces brightness by 40% (factor 0.6)
- **Highlight**: Increases brightness by 40% (factor 1.4) and reduces saturation by 20%

This creates visually pleasing shade and highlight variants automatically.
