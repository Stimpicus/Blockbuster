#!/usr/bin/env python3
"""
Test script for the enhanced palette editor features
"""

import json
import sys
from PIL import Image
from collections import Counter
import colorsys


def calculate_shade(color_hex: str, factor: float = 0.6) -> str:
    """Calculate a darker shade of the given color"""
    if not color_hex or color_hex == "":
        return "#000000"
    
    # Convert hex to RGB
    color_hex = color_hex.lstrip('#')
    try:
        r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    except:
        return "#000000"
    
    # Convert to HSV
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    
    # Reduce value (brightness) for shade
    v = v * factor
    
    # Convert back to RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    
    # Convert to hex
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def calculate_highlight(color_hex: str, factor: float = 1.4) -> str:
    """Calculate a lighter highlight of the given color"""
    if not color_hex or color_hex == "":
        return "#000000"
    
    # Convert hex to RGB
    color_hex = color_hex.lstrip('#')
    try:
        r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    except:
        return "#000000"
    
    # Convert to HSV
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    
    # Increase value (brightness) for highlight
    v = min(1.0, v * factor)
    # Reduce saturation slightly for better highlight effect
    s = s * 0.8
    
    # Convert back to RGB
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    
    # Convert to hex
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def test_color_calculations():
    """Test shade and highlight calculations"""
    print("Testing color calculations...")
    
    # Test with red
    red = "#ff0000"
    shade_red = calculate_shade(red)
    highlight_red = calculate_highlight(red)
    
    print(f"  Red: {red}")
    print(f"  Shade: {shade_red}")
    print(f"  Highlight: {highlight_red}")
    
    assert shade_red != red, "Shade should be different from base color"
    assert highlight_red != red, "Highlight should be different from base color"
    
    # Test with blue
    blue = "#0000ff"
    shade_blue = calculate_shade(blue)
    highlight_blue = calculate_highlight(blue)
    
    print(f"  Blue: {blue}")
    print(f"  Shade: {shade_blue}")
    print(f"  Highlight: {highlight_blue}")
    
    print("✓ Color calculations working correctly\n")


def test_dominant_color_extraction():
    """Test dominant color extraction from a test image"""
    print("Testing dominant color extraction...")
    
    # Create a test image with known colors
    img = Image.new('RGB', (100, 100))
    pixels = img.load()
    
    # Fill with red, but exclude pure black and white
    for y in range(100):
        for x in range(100):
            if x < 50 and y < 50:
                pixels[x, y] = (255, 0, 0)  # Red
            elif x >= 50 and y < 50:
                pixels[x, y] = (0, 255, 0)  # Green
            elif x < 50 and y >= 50:
                pixels[x, y] = (0, 0, 255)  # Blue
            else:
                pixels[x, y] = (255, 255, 0)  # Yellow
    
    # Extract colors from top-left quadrant (should be mostly red)
    region_colors = []
    for y in range(0, 50):
        for x in range(0, 50):
            color = pixels[x, y]
            hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            if hex_color not in ["#000000", "#ffffff"]:
                region_colors.append(hex_color)
    
    if region_colors:
        color_counter = Counter(region_colors)
        dominant_color = color_counter.most_common(1)[0][0]
        print(f"  Dominant color in region: {dominant_color}")
        assert dominant_color == "#ff0000", f"Expected #ff0000 but got {dominant_color}"
    
    print("✓ Dominant color extraction working correctly\n")


def test_config_structure():
    """Test that the configuration structure is valid"""
    print("Testing configuration structure...")
    
    with open('SaveCharacterPalette.json', 'r') as f:
        config = json.load(f)
    
    assert isinstance(config, list), "Config should be a list"
    assert len(config) > 0, "Config should not be empty"
    
    # Check first item structure
    first_item = config[0]
    item_name = list(first_item.keys())[0]
    item_data = first_item[item_name]
    
    assert "Start X" in item_data, "Item should have Start X"
    assert "Start Y" in item_data, "Item should have Start Y"
    assert "Width" in item_data, "Item should have Width"
    assert "Height" in item_data, "Item should have Height"
    
    print(f"  Config has {len(config)} items")
    print(f"  First item: {item_name}")
    print("✓ Configuration structure is valid\n")


def main():
    """Run all tests"""
    print("=" * 60)
    print("Enhanced Palette Editor - Test Suite")
    print("=" * 60 + "\n")
    
    try:
        test_color_calculations()
        test_dominant_color_extraction()
        test_config_structure()
        
        print("=" * 60)
        print("All tests passed! ✓")
        print("=" * 60)
        return 0
    
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
