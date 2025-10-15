#!/usr/bin/env python3
"""
Integration test for the grouped palette editor with auto-calculated shades/highlights
"""
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_auto_calculation():
    """Test that shade and highlight auto-calculation works correctly"""
    print("=== Testing Auto-Calculation Features ===\n")
    
    # Import after path is set
    from palette_editor import calculate_shade, calculate_highlight
    
    # Test cases for shade/highlight calculation
    test_colors = [
        ("#FF0000", "Red"),
        ("#00FF00", "Green"),
        ("#0000FF", "Blue"),
        ("#FFFF00", "Yellow"),
        ("#FF00FF", "Magenta"),
        ("#00FFFF", "Cyan"),
        ("#888888", "Gray"),
    ]
    
    print("Testing shade and highlight calculation:")
    all_passed = True
    for color, name in test_colors:
        shade = calculate_shade(color)
        highlight = calculate_highlight(color)
        
        # Verify shade is darker (lower RGB values)
        base_rgb = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        shade_rgb = tuple(int(shade.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        highlight_rgb = tuple(int(highlight.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        
        base_brightness = sum(base_rgb) / 3
        shade_brightness = sum(shade_rgb) / 3
        highlight_brightness = sum(highlight_rgb) / 3
        
        if shade_brightness < base_brightness and highlight_brightness >= base_brightness:
            print(f"  ✓ {name:8} {color} → Shade: {shade}, Highlight: {highlight}")
        else:
            print(f"  ✗ {name:8} {color} → FAILED")
            all_passed = False
    
    if not all_passed:
        print("\nSome tests FAILED!")
        return False
    
    print("\n✓ All shade/highlight calculations are correct\n")
    
    # Test edge cases
    print("Testing edge cases:")
    
    # Empty color
    empty_shade = calculate_shade("")
    empty_highlight = calculate_highlight("")
    if empty_shade == "#000000" and empty_highlight == "#000000":
        print("  ✓ Empty color handled correctly")
    else:
        print("  ✗ Empty color NOT handled correctly")
        all_passed = False
    
    # Very dark color
    dark_shade = calculate_shade("#111111")
    if dark_shade.startswith("#"):
        print("  ✓ Very dark color handled correctly")
    else:
        print("  ✗ Very dark color NOT handled correctly")
        all_passed = False
    
    # Very bright color
    bright_highlight = calculate_highlight("#FFFFFF")
    if bright_highlight.startswith("#"):
        print("  ✓ Very bright color handled correctly")
    else:
        print("  ✗ Very bright color NOT handled correctly")
        all_passed = False
    
    print()
    
    return all_passed


def test_file_operations():
    """Test that save/load operations still work"""
    print("Testing file operations:")
    
    # Test that SaveCharacterPalette.json exists and is valid
    if not os.path.exists("SaveCharacterPalette.json"):
        print("  ✗ SaveCharacterPalette.json not found")
        return False
    
    try:
        with open("SaveCharacterPalette.json", 'r') as f:
            data = json.load(f)
        print(f"  ✓ SaveCharacterPalette.json loaded ({len(data)} items)")
    except Exception as e:
        print(f"  ✗ Failed to load SaveCharacterPalette.json: {e}")
        return False
    
    # Verify structure
    if len(data) == 86:
        print("  ✓ Correct number of items (86)")
    else:
        print(f"  ✗ Unexpected number of items ({len(data)}, expected 86)")
        return False
    
    print()
    return True


def main():
    """Main test runner"""
    print("=" * 60)
    print("PALETTE EDITOR INTEGRATION TESTS")
    print("=" * 60)
    print()
    
    success = True
    
    # Run auto-calculation tests
    if not test_auto_calculation():
        success = False
    
    # Run file operation tests
    if not test_file_operations():
        success = False
    
    # Summary
    print("=" * 60)
    if success:
        print("ALL INTEGRATION TESTS PASSED!")
    else:
        print("SOME INTEGRATION TESTS FAILED!")
    print("=" * 60)
    
    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
