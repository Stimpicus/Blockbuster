#!/usr/bin/env python3
"""
Demo script to show the palette editor functionality
Creates sample configuration and PNG files
"""

import json
import sys
from PIL import Image
import colorsys


def calculate_shade(color_hex: str, factor: float = 0.6) -> str:
    """Calculate a darker shade of the given color"""
    if not color_hex or color_hex == "":
        return "#000000"
    
    color_hex = color_hex.lstrip('#')
    try:
        r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    except:
        return "#000000"
    
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    v = v * factor
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def calculate_highlight(color_hex: str, factor: float = 1.4) -> str:
    """Calculate a lighter highlight of the given color"""
    if not color_hex or color_hex == "":
        return "#000000"
    
    color_hex = color_hex.lstrip('#')
    try:
        r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
    except:
        return "#000000"
    
    h, s, v = colorsys.rgb_to_hsv(r/255.0, g/255.0, b/255.0)
    v = min(1.0, v * factor)
    s = s * 0.8
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def create_demo_palette():
    """Create a demo palette with some colors"""
    print("Creating demo palette...")
    
    # Load template
    with open('SaveCharacterPalette.json', 'r') as f:
        config = json.load(f)
    
    # Set some colors for demonstration
    demo_colors = {
        'Torso': {
            'Color 1': '#ff0000',  # Red
            'Color 2': '#00ff00',  # Green
            'Color 3': '#0000ff',  # Blue
            'Color 4': '#ffff00',  # Yellow
            'Color 5': '#ff00ff',  # Magenta
        },
        'Hips': {
            'Color 1': '#00ffff',  # Cyan
            'Color 2': '#ff8800',  # Orange
            'Color 3': '#8800ff',  # Purple
            'Color 4': '#88ff00',  # Lime
            'Color 5': '#ff0088',  # Pink
        }
    }
    
    # Apply colors to configuration
    for item in config:
        item_name = list(item.keys())[0]
        
        if item_name in demo_colors:
            item_data = item[item_name]
            colors = demo_colors[item_name]
            
            for color_id, hex_color in colors.items():
                if color_id in item_data:
                    # Set base color
                    item_data[color_id]['Color'] = hex_color
                    
                    # Calculate and set shade
                    if 'Shade' in item_data[color_id]:
                        shade_color = calculate_shade(hex_color)
                        item_data[color_id]['Shade']['Color'] = shade_color
                        print(f"  {item_name} - {color_id}: {hex_color} -> Shade: {shade_color}")
                    
                    # Calculate and set highlight
                    if 'Highlight' in item_data[color_id]:
                        highlight_color = calculate_highlight(hex_color)
                        item_data[color_id]['Highlight']['Color'] = highlight_color
                        print(f"  {item_name} - {color_id}: {hex_color} -> Highlight: {highlight_color}")
    
    # Save demo configuration
    with open('demo_palette.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n✓ Demo palette saved to demo_palette.json")
    return config


def generate_png_from_config(config, output_file='demo_texture.png'):
    """Generate a PNG from the configuration"""
    print(f"\nGenerating {output_file}...")
    
    # Create 1024x1024 image
    img = Image.new('RGB', (1024, 1024), color='black')
    pixels = img.load()
    
    regions_filled = 0
    
    # Process each item
    for item in config:
        item_name = list(item.keys())[0]
        item_data = item[item_name]
        
        # Process all color regions recursively
        def fill_region(data, prefix=""):
            nonlocal regions_filled
            
            if isinstance(data, dict):
                # Check if this has position and color
                has_position = all(k in data for k in ["Start X", "Start Y", "Width", "Height"])
                
                if has_position and "Color" in data and data.get("Color"):
                    color_hex = data["Color"].lstrip('#')
                    try:
                        r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
                        x = int(data["Start X"])
                        y = int(data["Start Y"])
                        w = int(data["Width"])
                        h = int(data["Height"])
                        
                        # Fill the region
                        for py in range(y, min(y + h, 1024)):
                            for px in range(x, min(x + w, 1024)):
                                pixels[px, py] = (r, g, b)
                        
                        regions_filled += 1
                    except:
                        pass
                
                # Recurse
                for key, value in data.items():
                    if key not in ["Start X", "Start Y", "Width", "Height", "Color"]:
                        fill_region(value, f"{prefix}.{key}" if prefix else key)
        
        fill_region(item_data, item_name)
    
    # Save the image
    img.save(output_file, 'PNG')
    print(f"✓ Generated {output_file} with {regions_filled} colored regions")


def main():
    """Run the demo"""
    print("=" * 60)
    print("Palette Editor Demo")
    print("=" * 60 + "\n")
    
    try:
        # Create demo palette
        config = create_demo_palette()
        
        # Generate PNG
        generate_png_from_config(config)
        
        print("\n" + "=" * 60)
        print("Demo completed successfully!")
        print("Files created:")
        print("  - demo_palette.json (configuration)")
        print("  - demo_texture.png (generated texture)")
        print("=" * 60)
        
        return 0
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
