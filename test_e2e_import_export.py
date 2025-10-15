#!/usr/bin/env python3
"""
End-to-end integration test for the import/export fix.
This test simulates the actual GUI workflow without requiring Tkinter.
"""

import json
import sys
import os
import tempfile
from PIL import Image
from collections import Counter


# Mock the ColorEntry class from palette_editor.py
class ColorEntry:
    """Represents a single color entry in the palette"""
    def __init__(self, name, x, y, width, height, color=""):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color if color else "#000000"
        self.widgets = None


def parse_palette_structure(data, path="", color_entries=None, parent_regions=None):
    """Recursively parse the palette structure - mirrors palette_editor.py logic"""
    if color_entries is None:
        color_entries = {}
    if parent_regions is None:
        parent_regions = set()
    
    if isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{path}.{i}" if path else str(i)
            parse_palette_structure(item, new_path, color_entries, parent_regions)
    
    elif isinstance(data, dict):
        has_position = all(k in data for k in ["Start X", "Start Y", "Width", "Height"])
        
        if has_position:
            # Check if this is a parent region
            has_sub_regions = False
            for key, value in data.items():
                if key not in ["Start X", "Start Y", "Width", "Height", "Color"]:
                    if isinstance(value, dict) and all(k in value for k in ["Start X", "Start Y", "Width", "Height"]):
                        has_sub_regions = True
                        break
            
            if has_sub_regions:
                parent_regions.add(path)
            
            # Create entry if it has Color field
            if "Color" in data:
                region_name = path.split('.')[-1] if '.' in path else path
                x = int(data["Start X"])
                y = int(data["Start Y"])
                w = int(data["Width"])
                h = int(data["Height"])
                color = data.get("Color", "#000000")
                if not color:
                    color = "#000000"
                
                entry = ColorEntry(region_name, x, y, w, h, color)
                color_entries[path] = entry
        
        # Recurse
        for key, value in data.items():
            if key not in ["Start X", "Start Y", "Width", "Height", "Color"]:
                new_path = f"{path}.{key}" if path else key
                parse_palette_structure(value, new_path, color_entries, parent_regions)
    
    return color_entries, parent_regions


def simulate_import(color_entries, input_image_path):
    """Simulate import_texture() - mirrors palette_editor.py logic"""
    img = Image.open(input_image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    pixels = img.load()
    updated_count = 0
    
    # Process each region
    for path, entry in color_entries.items():
        # Sample exact pixel at region's start position
        if entry.x < img.size[0] and entry.y < img.size[1]:
            color = pixels[entry.x, entry.y]
            hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            
            # Only update if not black (skip unmapped regions)
            if hex_color != "#000000":
                entry.color = hex_color
                updated_count += 1
    
    return updated_count


def simulate_export(color_entries, parent_regions, output_path):
    """Simulate update_preview() and export_png() - mirrors palette_editor.py logic"""
    img = Image.new('RGB', (1024, 1024), color='black')
    pixels = img.load()
    
    # Fill regions with colors (skip parent regions and empty colors)
    for path, entry in color_entries.items():
        # Skip parent regions
        if path in parent_regions:
            continue
        
        # Skip empty or black colors
        if not entry.color or entry.color == "" or entry.color == "#000000":
            continue
        
        # Convert hex to RGB
        color_hex = entry.color.lstrip('#')
        try:
            r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
        except (ValueError, IndexError):
            # Skip invalid color values
            continue
        
        # Fill the region
        for y in range(entry.y, min(entry.y + entry.height, 1024)):
            for x in range(entry.x, min(entry.x + entry.width, 1024)):
                pixels[x, y] = (r, g, b)
    
    img.save(output_path, 'PNG')
    return img


def main():
    """Main test function"""
    print("=== End-to-End Import/Export Integration Test ===\n")
    
    # Load palette data
    palette_path = "SaveCharacterPalette.json"
    if not os.path.exists(palette_path):
        print(f"ERROR: {palette_path} not found")
        return 1
    
    print(f"Loading {palette_path}...")
    with open(palette_path, 'r') as f:
        palette_data = json.load(f)
    
    # Parse palette structure
    print("Parsing palette structure...")
    color_entries, parent_regions = parse_palette_structure(palette_data)
    print(f"  Total regions: {len(color_entries)}")
    print(f"  Parent regions: {len(parent_regions)}")
    print(f"  Leaf regions: {len(color_entries) - len(parent_regions)}")
    
    # Simulate import
    input_path = "palette_input.PNG"
    if not os.path.exists(input_path):
        print(f"ERROR: {input_path} not found")
        return 1
    
    print(f"\nImporting from {input_path}...")
    updated_count = simulate_import(color_entries, input_path)
    print(f"  Imported {updated_count} regions with non-black colors")
    
    # Simulate export
    output_path = os.path.join(tempfile.gettempdir(), 'integration_test_output.png')
    print(f"\nExporting to {output_path}...")
    output_img = simulate_export(color_entries, parent_regions, output_path)
    print(f"  Export complete")
    
    # Validate the output
    print("\n=== Validation ===")
    
    # Load input for comparison
    input_img = Image.open(input_path)
    if input_img.mode != 'RGB':
        input_img = input_img.convert('RGB')
    input_pixels = input_img.load()
    output_pixels = output_img.load()
    
    # Test Issue 1: (608, 96) should be black in output
    print("\n1. Testing Issue #1: Gap at (608, 96)")
    input_color_608_96 = input_pixels[608, 96]
    input_hex_608_96 = f"#{input_color_608_96[0]:02x}{input_color_608_96[1]:02x}{input_color_608_96[2]:02x}"
    output_color_608_96 = output_pixels[608, 96]
    output_hex_608_96 = f"#{output_color_608_96[0]:02x}{output_color_608_96[1]:02x}{output_color_608_96[2]:02x}"
    
    print(f"   Input color at (608, 96): {input_hex_608_96}")
    print(f"   Output color at (608, 96): {output_hex_608_96}")
    
    if output_hex_608_96 == "#000000":
        print("   ✓ PASS: Gap remains black (unmapped)")
    else:
        print(f"   ✗ FAIL: Expected black, got {output_hex_608_96}")
        return 1
    
    # Test Issue 2: (576, 960) should be black in output
    print("\n2. Testing Issue #2: Black region at (576, 960)")
    input_color_576_960 = input_pixels[576, 960]
    input_hex_576_960 = f"#{input_color_576_960[0]:02x}{input_color_576_960[1]:02x}{input_color_576_960[2]:02x}"
    output_color_576_960 = output_pixels[576, 960]
    output_hex_576_960 = f"#{output_color_576_960[0]:02x}{output_color_576_960[1]:02x}{output_color_576_960[2]:02x}"
    
    print(f"   Input color at (576, 960): {input_hex_576_960}")
    print(f"   Output color at (576, 960): {output_hex_576_960}")
    
    if output_hex_576_960 == "#000000":
        print("   ✓ PASS: Black region stays black")
    else:
        print(f"   ✗ FAIL: Expected black, got {output_hex_576_960}")
        return 1
    
    # Test some actual colored regions to make sure they work
    print("\n3. Testing sample colored regions")
    
    # Dynamically find a few non-black, non-parent regions with colors
    test_regions = []
    for path, entry in color_entries.items():
        if (path not in parent_regions and 
            entry.color and 
            entry.color != "#000000" and
            len(test_regions) < 3):
            test_regions.append(path)
    
    if not test_regions:
        print("   Warning: No colored leaf regions found for testing")
    else:
        all_passed = True
        for path in test_regions:
            entry = color_entries[path]
            # Check if output matches the imported color
            output_color = output_pixels[entry.x, entry.y]
            output_hex = f"#{output_color[0]:02x}{output_color[1]:02x}{output_color[2]:02x}"
            
            print(f"   Region {path}")
            print(f"     Position: ({entry.x}, {entry.y})")
            print(f"     Imported: {entry.color}")
            print(f"     Output: {output_hex}")
            
            if output_hex == entry.color:
                print(f"     ✓ PASS")
            else:
                print(f"     ✗ FAIL: Mismatch")
                all_passed = False
        
        if not all_passed:
            return 1
    
    print("\n=== All Tests Passed! ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
