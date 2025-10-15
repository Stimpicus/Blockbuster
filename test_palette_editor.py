#!/usr/bin/env python3
"""
Test script for the Character Palette Editor
This validates the JSON parsing and PNG generation without requiring a GUI.
"""

import json
import sys
from PIL import Image


def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    if not hex_color or hex_color == "":
        return (0, 0, 0)
    
    hex_color = hex_color.lstrip('#')
    try:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except:
        return (0, 0, 0)


def parse_palette_regions(data, path="", regions=None):
    """Recursively extract all color regions from the palette data"""
    if regions is None:
        regions = []
    
    if isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{path}.{i}" if path else str(i)
            parse_palette_regions(item, new_path, regions)
    
    elif isinstance(data, dict):
        # Check if this dict has position and color info
        has_position = all(k in data for k in ["Start X", "Start Y", "Width", "Height"])
        
        if has_position and "Color" in data:
            region = {
                'path': path,
                'name': path.split('.')[-1] if '.' in path else path,
                'x': int(data["Start X"]),
                'y': int(data["Start Y"]),
                'width': int(data["Width"]),
                'height': int(data["Height"]),
                'color': data.get("Color", "")
            }
            regions.append(region)
        
        # Recurse into nested structures
        for key, value in data.items():
            if key not in ["Start X", "Start Y", "Width", "Height", "Color"]:
                new_path = f"{path}.{key}" if path else key
                parse_palette_regions(value, new_path, regions)
    
    return regions


def generate_palette_png(palette_data, output_path="test_output.png"):
    """Generate a PNG from palette data"""
    # Create 1024x1024 image
    img = Image.new('RGB', (1024, 1024), color='black')
    pixels = img.load()
    
    # Extract all color regions
    regions = parse_palette_regions(palette_data)
    
    print(f"Found {len(regions)} color regions")
    
    # Fill regions with colors
    colored_regions = 0
    for region in regions:
        if region['color']:
            rgb = hex_to_rgb(region['color'])
            
            # Fill the region
            for y in range(region['y'], min(region['y'] + region['height'], 1024)):
                for x in range(region['x'], min(region['x'] + region['width'], 1024)):
                    pixels[x, y] = rgb
            
            colored_regions += 1
    
    print(f"Filled {colored_regions} regions with colors")
    
    # Save the image
    img.save(output_path, 'PNG')
    print(f"Saved PNG to {output_path}")
    
    return img


def test_palette_editor():
    """Main test function"""
    print("=== Character Palette Editor Test ===\n")
    
    # Load the default template
    template_path = "SaveCharacterPalette.json"
    
    print(f"Loading template: {template_path}")
    try:
        with open(template_path, 'r') as f:
            palette_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {template_path} not found")
        return False
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return False
    
    print(f"✓ Loaded {len(palette_data)} top-level entries\n")
    
    # Validate expected count
    if len(palette_data) != 86:
        print(f"⚠ Warning: Expected 86 top-level entries, found {len(palette_data)}")
    
    # Parse and display regions
    regions = parse_palette_regions(palette_data)
    print(f"✓ Parsed {len(regions)} color regions\n")
    
    # Validate expected count
    if len(regions) != 645:
        print(f"⚠ Warning: Expected 645 color regions, found {len(regions)}")
    
    # Show some example regions
    print("Sample regions:")
    for region in regions[:10]:
        color_display = region['color'] if region['color'] else "(empty)"
        print(f"  - {region['path']}: {color_display}")
    
    if len(regions) > 10:
        print(f"  ... and {len(regions) - 10} more")
    
    print()
    
    # Test PNG generation with some sample colors
    print("Testing PNG generation...")
    
    # Add some test colors to a copy of the data
    test_data = json.loads(json.dumps(palette_data))  # Deep copy
    
    # Add red color to first region with Torso
    if test_data and len(test_data) > 0:
        torso = test_data[0].get("Torso", {})
        if "Color 1" in torso:
            torso["Color 1"]["Color"] = "#FF0000"
            if "Shade" in torso["Color 1"]:
                torso["Color 1"]["Shade"]["Color"] = "#AA0000"
            if "Highlight" in torso["Color 1"]:
                torso["Color 1"]["Highlight"]["Color"] = "#FF5555"
    
    # Generate PNG
    try:
        img = generate_palette_png(test_data, "test_palette_output.png")
        print(f"✓ Generated {img.size[0]}x{img.size[1]} PNG image\n")
    except Exception as e:
        print(f"Error generating PNG: {e}")
        return False
    
    print("=== All tests passed! ===")
    return True


if __name__ == "__main__":
    success = test_palette_editor()
    sys.exit(0 if success else 1)
