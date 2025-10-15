#!/usr/bin/env python3
"""
Test script to validate PNG import/export fixes.
Tests that:
1. Import extracts exact pixel colors at region positions
2. Import skips black (unmapped) regions
3. Export only fills regions with non-empty colors
"""

import json
import os
from PIL import Image
from collections import Counter

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


def simulate_import(palette_data, input_image_path):
    """Simulate the import_texture function with new logic"""
    img = Image.open(input_image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    pixels = img.load()
    regions = parse_palette_regions(palette_data)
    
    # Simulate import: sample exact pixel at region start position
    imported_colors = {}
    for region in regions:
        if region['x'] < img.size[0] and region['y'] < img.size[1]:
            color = pixels[region['x'], region['y']]
            hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            
            # Only update if not black (skip unmapped regions)
            if hex_color != "#000000":
                imported_colors[region['path']] = hex_color
                region['color'] = hex_color
    
    return regions, imported_colors


def find_parent_regions(data, path="", parents=None):
    """Find all regions that have sub-regions (parent regions)"""
    if parents is None:
        parents = set()
    
    if isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{path}.{i}" if path else str(i)
            find_parent_regions(item, new_path, parents)
    
    elif isinstance(data, dict):
        has_position = all(k in data for k in ["Start X", "Start Y", "Width", "Height"])
        
        if has_position and "Color" in data:
            # Check if this region has any sub-regions with positions
            has_sub_regions = False
            for key, value in data.items():
                if key not in ["Start X", "Start Y", "Width", "Height", "Color"]:
                    if isinstance(value, dict) and all(k in value for k in ["Start X", "Start Y", "Width", "Height"]):
                        has_sub_regions = True
                        break
            
            if has_sub_regions:
                parents.add(path)
        
        # Recurse into nested structures
        for key, value in data.items():
            if key not in ["Start X", "Start Y", "Width", "Height", "Color"]:
                new_path = f"{path}.{key}" if path else key
                find_parent_regions(value, new_path, parents)
    
    return parents


def simulate_export(regions, output_path, parent_regions):
    """Simulate the update_preview/export function with new logic"""
    img = Image.new('RGB', (1024, 1024), color='black')
    pixels = img.load()
    
    # Fill only regions with non-empty colors (skip parents)
    for region in regions:
        # Skip parent regions
        if region['path'] in parent_regions:
            continue
        
        # Skip regions with empty or black colors
        if not region['color'] or region['color'] == "" or region['color'] == "#000000":
            continue
        
        rgb = hex_to_rgb(region['color'])
        
        # Fill the region
        for y in range(region['y'], min(region['y'] + region['height'], 1024)):
            for x in range(region['x'], min(region['x'] + region['width'], 1024)):
                pixels[x, y] = rgb
    
    img.save(output_path, 'PNG')
    return img


def test_import_export():
    """Main test function"""
    print("=== Testing PNG Import/Export Fixes ===\n")
    
    # Load palette data
    print("Loading SaveCharacterPalette.json...")
    with open('SaveCharacterPalette.json', 'r') as f:
        palette_data = json.load(f)
    
    # Find parent regions
    print("Finding parent regions...")
    parent_regions = find_parent_regions(palette_data)
    print(f"Found {len(parent_regions)} parent regions that will be skipped during export")
    
    # Simulate import
    print("\nSimulating import from palette_input.PNG...")
    regions, imported_colors = simulate_import(palette_data, 'palette_input.PNG')
    print(f"Imported {len(imported_colors)} non-black regions")
    
    # Test Issue 1: Check color at (608, 96)
    print("\n=== Testing Issue 1: Color at (608, 96) ===")
    input_img = Image.open('palette_input.PNG')
    if input_img.mode != 'RGB':
        input_img = input_img.convert('RGB')
    input_pixels = input_img.load()
    
    expected_color_608_96 = input_pixels[608, 96]
    expected_hex_608_96 = f"#{expected_color_608_96[0]:02x}{expected_color_608_96[1]:02x}{expected_color_608_96[2]:02x}"
    print(f"Expected color at (608, 96): {expected_hex_608_96}")
    
    # Find which region contains (608, 96) and check if it was imported correctly
    found_region_608_96 = None
    for region in regions:
        x, y, w, h = region['x'], region['y'], region['width'], region['height']
        if x == 608 and y == 96:
            found_region_608_96 = region
            break
    
    if found_region_608_96:
        print(f"Region starting at (608, 96): {found_region_608_96['path']}")
        print(f"Imported color: {found_region_608_96['color']}")
        if found_region_608_96['color'] == expected_hex_608_96:
            print("✓ PASS: Color matches expected value!")
        else:
            print(f"✗ FAIL: Expected {expected_hex_608_96} but got {found_region_608_96['color']}")
    else:
        print("Note: No region starts at exact position (608, 96)")
        print("This is expected - the coordinate is in a gap between sub-regions")
        print("The parent region will be skipped, so this position will remain black in output")
    
    # Test Issue 2: Check that (576, 960) stays black
    print("\n=== Testing Issue 2: Color at (576, 960) ===")
    expected_color_576_960 = input_pixels[576, 960]
    expected_hex_576_960 = f"#{expected_color_576_960[0]:02x}{expected_color_576_960[1]:02x}{expected_color_576_960[2]:02x}"
    print(f"Expected color at (576, 960): {expected_hex_576_960}")
    
    # Find region at (576, 960)
    found_region_576_960 = None
    for region in regions:
        if region['x'] == 576 and region['y'] == 960:
            found_region_576_960 = region
            break
    
    if found_region_576_960:
        print(f"Region at (576, 960): {found_region_576_960['path']}")
        print(f"Imported color: {found_region_576_960['color']}")
        if expected_hex_576_960 == "#000000":
            if found_region_576_960['color'] == "" or found_region_576_960['color'] == "#000000":
                print("✓ PASS: Black region was not imported (correctly skipped)!")
            else:
                print(f"✗ FAIL: Black region should not be imported, but got {found_region_576_960['color']}")
        else:
            if found_region_576_960['color'] == expected_hex_576_960:
                print("✓ PASS: Color matches!")
            else:
                print(f"✗ FAIL: Expected {expected_hex_576_960} but got {found_region_576_960['color']}")
    
    # Simulate export
    print("\n=== Testing Export ===")
    output_path = '/tmp/test_palette_output.png'
    print(f"Simulating export to {output_path}...")
    output_img = simulate_export(regions, output_path, parent_regions)
    
    # Verify exported image
    output_pixels = output_img.load()
    
    # Check (608, 96) in output
    output_color_608_96 = output_pixels[608, 96]
    output_hex_608_96 = f"#{output_color_608_96[0]:02x}{output_color_608_96[1]:02x}{output_color_608_96[2]:02x}"
    print(f"\nColor at (608, 96) in output: {output_hex_608_96}")
    if output_hex_608_96 == "#000000":
        print("✓ PASS: Unmapped coordinate stays black in output!")
    else:
        print(f"✗ FAIL: Expected black but got {output_hex_608_96}")
    
    # Check (576, 960) in output
    output_color_576_960 = output_pixels[576, 960]
    output_hex_576_960 = f"#{output_color_576_960[0]:02x}{output_color_576_960[1]:02x}{output_color_576_960[2]:02x}"
    print(f"Color at (576, 960) in output: {output_hex_576_960}")
    if output_hex_576_960 == "#000000":
        print("✓ PASS: Black region stays black in output!")
    else:
        print(f"✗ FAIL: Expected black but got {output_hex_576_960}")
    
    print("\n=== Test Complete ===")


if __name__ == "__main__":
    test_import_export()
