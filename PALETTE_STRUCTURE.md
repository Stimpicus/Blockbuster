# Character Palette Technical Documentation

## Overview

The Character Palette system uses a 1024x1024 pixel texture to store color information for various character body parts and materials. This document explains the technical structure and layout.

## File Structure

### JSON Format

The palette configuration is stored as a JSON array where each element represents a major body part or material category:

```json
[
  {
    "Torso": {
      "Start X": "0",
      "Start Y": "0",
      "Width": "64",
      "Height": "320",
      "Color": "",
      "Color 1": { ... },
      "Color 2": { ... }
    }
  },
  { "Hips": { ... } },
  { "Skin": { ... } }
]
```

### Region Properties

Each region in the palette has the following properties:

- **Start X**: X-coordinate in the 1024x1024 texture (pixels from left)
- **Start Y**: Y-coordinate in the 1024x1024 texture (pixels from top)
- **Width**: Width of the region in pixels
- **Height**: Height of the region in pixels
- **Color**: Hex color code (e.g., "#FF0000" for red, or "" for empty)

### Nested Structure

Regions can be nested to create hierarchical color schemes:

1. **Main Region** (e.g., "Torso")
   - Has position and size
   - Can have a base color
   - Contains sub-regions

2. **Color Variants** (e.g., "Color 1", "Color 2")
   - Each represents a different color slot for the region
   - Can have Shade and Highlight sub-variants
   
3. **Shade/Highlight**
   - Darker or lighter variants of the base color
   - Used for creating depth and lighting effects

## Texture Layout

The 1024x1024 texture is divided into a grid:

```
0         64        128       192       256       320       384
┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬────...
│ Torso   │Arm      │Arm      │Hand     │Hand     │Shoulder │
│         │Attire   │Attire   │Attire   │Attire   │Attire   │
│ 64x320  │Left     │Right    │Left     │Right    │Left     │
│         │64x320   │64x320   │64x320   │64x320   │64x320   │
├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
│ Hips    │Leg      │Leg      │Foot     │Foot     │Shoulder │
│         │Left     │Right    │Left     │Right    │Attire   │
│ 64x320  │64x320   │64x320   │64x320   │64x320   │Right    │
│         │         │         │         │         │64x320   │
├─────────┼─────────┼─────────┼─────────┼─────────┼─────────┤
│ Skin    │Ear      │Ear      │Eyes     │Eyes     │Face     │
│ 64x192  │Left     │Right    │Left     │Right    │Attach   │
│         │64x64    │64x64    │64x64    │64x64    │64x320   │
└─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴────...
```

### Major Regions

The palette includes these major categories:

1. **Body Parts**
   - Torso (0, 0) - 64x320
   - Hips (0, 320) - 64x320
   - Arms (Left/Right)
   - Legs (Left/Right)
   - Hands (Left/Right)
   - Feet (Left/Right)

2. **Head/Face**
   - Skin (0, 640) - 64x192
   - Eyes (multiple variants)
   - Ears (Left/Right)
   - Nose, Mouth, Lips
   - Teeth, Gums, Tongue

3. **Clothing/Armor**
   - Torso Attire
   - Arm Attire (Left/Right)
   - Hand Attire (Left/Right)
   - Shoulder Attire (Left/Right)
   - Leg Attire
   - Knee Attire (Left/Right)

4. **Accessories**
   - Head Attachment
   - Face Attachment
   - Hip Attachments (Front/Back/Left/Right)
   - Jewelry Gem

5. **Materials**
   - Leather
   - Metal
   - Cloth
   - Fabric
   - Wood
   - Paper
   - Bone
   - Flesh
   - Concrete

6. **Elements**
   - Fire
   - Water
   - Ice
   - Lava
   - Vegetation

7. **Special**
   - Reference Palette (960, 0) - 64x960
   - Cuts (960, 960) - 64x64

## Color Encoding

Colors are stored as hexadecimal RGB values:

- Format: `#RRGGBB`
- Examples:
  - `#FF0000` - Pure Red
  - `#00FF00` - Pure Green
  - `#0000FF` - Pure Blue
  - `#FFFFFF` - White
  - `#000000` - Black
  - `#FFDBAC` - Skin tone (light)
  - `""` - Empty/transparent (rendered as black in preview)

## Region Count

The current palette structure contains:
- **86** top-level regions
- **645** total color regions (including all nested variants)

## Usage in Game Engine

The 1024x1024 texture is used as a lookup table:

1. 3D models have UV coordinates that map to specific regions in this texture
2. The shader reads the color from the texture at the UV coordinate
3. This allows dynamic character customization without changing textures at runtime

## Editing Guidelines

When editing the palette:

1. **Maintain Structure**: Don't change Start X, Start Y, Width, or Height values
2. **Use Hex Colors**: Always use the #RRGGBB format
3. **Consider Variants**: Each Color should have matching Shade (darker) and Highlight (lighter) variants
4. **Test Visually**: Use the preview to ensure colors work well together
5. **Save Often**: Keep backups of working configurations

## Example Color Scheme

A typical color setup for a character might be:

```json
"Color 1": {
  "Color": "#FF5733",      // Main color (orange-red)
  "Shade": {
    "Color": "#CC4522"     // Darker shade
  },
  "Highlight": {
    "Color": "#FF8855"     // Lighter highlight
  }
}
```

This creates a nice gradient effect with the base color, darker shading, and lighter highlights.

## Reference Palette

The "Reference Palette" region (960, 0 to 1024, 960) is a special section containing:
- 15 predefined color slots
- Each with its own Shade and Highlight variants
- Useful as a color picker/reference when designing characters

## File Format Version

Current format: **Version 2**
- Based on CharacterPalette_Version2.h structure
- Maintains backward compatibility with the Unreal Engine implementation
