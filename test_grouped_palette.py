#!/usr/bin/env python3
"""
Test script for the grouped palette editor functionality
This validates the grouping logic without requiring a GUI.
"""

import json
import sys

# Test data structures
CLOTHING_GROUP = [
    'Torso', 'Arm Attire Left', 'Arm Attire Right', 
    'Hand Attire Left', 'Hand Attire Right', 'Hips', 
    'Leg Left', 'Leg Right', 'Foot Left', 'Foot Right'
]

ATTACHMENTS_GROUP = [
    'Shoulder Attire Left', 'Shoulder Attire Right', 
    'Elbow Attire Left', 'Elbow Attire Right', 
    'Knee Attire Left', 'Knee Attire Right', 
    'Hip Front Attachment', 'Hip Left Attachment', 
    'Hip Right Attachment', 'Hip Back Attachment', 
    'Head Attachment', 'Face Attachment', 'Back Attachment'
]


def test_groups():
    """Test that all expected items are in the palette data"""
    print("=== Testing Grouped Palette Editor ===\n")
    
    # Load the palette data
    try:
        with open('SaveCharacterPalette.json', 'r') as f:
            palette_data = json.load(f)
    except FileNotFoundError:
        print("Error: SaveCharacterPalette.json not found")
        return False
    
    print(f"✓ Loaded {len(palette_data)} items from palette data\n")
    
    # Extract item names
    item_names = [list(item.keys())[0] for item in palette_data]
    
    # Test Clothing group
    print("Testing Clothing group:")
    clothing_found = []
    clothing_missing = []
    for item in CLOTHING_GROUP:
        if item in item_names:
            clothing_found.append(item)
            print(f"  ✓ {item}")
        else:
            clothing_missing.append(item)
            print(f"  ✗ {item} (missing)")
    
    print(f"Found {len(clothing_found)}/{len(CLOTHING_GROUP)} clothing items\n")
    
    # Test Attachments group
    print("Testing Attachments group:")
    attachments_found = []
    attachments_missing = []
    for item in ATTACHMENTS_GROUP:
        if item in item_names:
            attachments_found.append(item)
            print(f"  ✓ {item}")
        else:
            attachments_missing.append(item)
            print(f"  ✗ {item} (missing)")
    
    print(f"Found {len(attachments_found)}/{len(ATTACHMENTS_GROUP)} attachment items\n")
    
    # Count other items
    all_grouped = set(CLOTHING_GROUP + ATTACHMENTS_GROUP)
    other_items = [name for name in item_names if name not in all_grouped]
    print(f"Other items (not in groups): {len(other_items)}")
    
    # Test that items have Color 1-5 structure
    print("\nTesting Color 1-5 structure:")
    test_item_name = 'Torso'
    for item in palette_data:
        if list(item.keys())[0] == test_item_name:
            test_item = item[test_item_name]
            colors_found = []
            for i in range(1, 6):
                color_key = f"Color {i}"
                if color_key in test_item:
                    colors_found.append(color_key)
                    # Check for Shade and Highlight
                    has_shade = "Shade" in test_item[color_key]
                    has_highlight = "Highlight" in test_item[color_key]
                    print(f"  ✓ {test_item_name}.{color_key} (Shade: {has_shade}, Highlight: {has_highlight})")
            
            print(f"Found {len(colors_found)}/5 color slots in {test_item_name}\n")
            break
    
    # Summary
    success = (len(clothing_missing) == 0 and 
               len(attachments_missing) == 0 and 
               len(colors_found) == 5)
    
    if success:
        print("=== All tests passed! ===")
        print("\nGrouping Summary:")
        print(f"  - Clothing items: {len(CLOTHING_GROUP)}")
        print(f"  - Attachment items: {len(ATTACHMENTS_GROUP)}")
        print(f"  - Other items: {len(other_items)}")
        print(f"  - Total items: {len(item_names)}")
    else:
        print("=== Some tests failed ===")
        if clothing_missing:
            print(f"Missing clothing items: {clothing_missing}")
        if attachments_missing:
            print(f"Missing attachment items: {attachments_missing}")
    
    return success


if __name__ == "__main__":
    success = test_groups()
    sys.exit(0 if success else 1)
