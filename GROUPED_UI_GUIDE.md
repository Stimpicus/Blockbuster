# Grouped Color Definitions - User Guide

## Overview

The Character Palette Editor now features a grouped interface that organizes color definitions into logical sets for improved usability. This makes it easier to manage colors for related items like clothing and attachments.

## Groups

### Clothing Group (10 items)
- Torso
- Arm Attire Left
- Arm Attire Right
- Hand Attire Left
- Hand Attire Right
- Hips
- Leg Left
- Leg Right
- Foot Left
- Foot Right

### Attachments Group (13 items)
- Shoulder Attire Left
- Shoulder Attire Right
- Elbow Attire Left
- Elbow Attire Right
- Knee Attire Left
- Knee Attire Right
- Hip Front Attachment
- Hip Left Attachment
- Hip Right Attachment
- Hip Back Attachment
- Head Attachment
- Face Attachment
- Back Attachment

### Other Items
All remaining items (skin, eyes, materials, etc.) are grouped under "Other Items".

## Using the Grouped Interface

### Collapsed State (Default)
By default, all groups are collapsed, showing:
- Group name with expand/collapse button (▶)
- Quick color selectors for Color 1-5 (labeled C1-C5)

This allows you to quickly apply colors to entire groups without expanding the details.

### Expanding Groups
Click the ▶ button to expand a group and see all items within it. The button changes to ▼ when expanded.

### Group-Level Color Selection
1. Click one of the Color buttons (C1-C5) in the collapsed group header
2. Choose a color from the color picker dialog
3. The color is automatically applied to all items in the group that have that color slot

### Individual Item Colors
1. Expand the group by clicking the ▶ button
2. Each item shows its own color pickers
3. Click any color button to customize that specific item's color

## Auto-Calculated Shades and Highlights

When you select a base color (Color 1-5), the editor automatically calculates:

- **Shade**: A darker variant (60% brightness) for shadowed areas
- **Highlight**: A lighter variant (140% brightness with reduced saturation) for lit areas

This uses HSV color space calculations for better visual results compared to simple RGB adjustments.

### How It Works
1. Select any Color 1-5 for an item or group
2. The Shade color is automatically calculated as a darker version
3. The Highlight color is automatically calculated as a lighter version
4. These values are updated in the palette data
5. The preview updates to show the new colors

## Manual Override
You can still manually set Shade and Highlight colors if the auto-calculated values don't match your needs:
1. Expand the group to see individual items
2. Find the Shade or Highlight entry for the color you want to adjust
3. Click its color button and choose a custom color

## Preview and Export
All existing functionality is preserved:
- **Live Preview**: The 1024x1024 preview updates automatically
- **Refresh Preview**: Click to manually update the preview
- **Export PNG**: File → Export PNG to save the palette as an image
- **Save Config**: File → Save to save your configuration

## Tips
- Use group-level colors for consistent theming across all items
- Expand groups only when you need fine-grained control
- The auto-calculated shades/highlights work best with medium-brightness colors
- Very dark or very bright colors may have less noticeable shade/highlight effects

## Examples

### Quick Theming
1. Keep all groups collapsed
2. Click C1 (Color 1) for the Clothing group
3. Choose a primary color (e.g., dark blue)
4. Click C2 for accent color (e.g., gold)
5. Repeat for Attachments group
6. All items in each group now have consistent colors

### Custom Item Colors
1. Expand the Clothing group
2. Find "Torso - Color 1"
3. Click its color button
4. Choose a custom color just for the torso
5. The torso's shade and highlight are auto-calculated
6. Other clothing items retain their group colors

## Technical Details

### Color Calculation Algorithm
- **Shade**: Converts RGB to HSV, multiplies V (value/brightness) by 0.6, converts back to RGB
- **Highlight**: Converts RGB to HSV, multiplies V by 1.4 (capped at 1.0), multiplies S (saturation) by 0.8, converts back to RGB

### Data Format
The underlying JSON format remains unchanged. All changes are compatible with existing SaveCharacterPalette.json files.

## Troubleshooting

**Q: I expanded a group but don't see the items**  
A: Make sure you clicked the ▶ button next to the group name. It should change to ▼ when expanded.

**Q: The auto-calculated colors don't look right**  
A: You can manually override any Shade or Highlight by expanding the group and clicking that specific color entry.

**Q: Can I apply different colors to individual items in a group?**  
A: Yes! Expand the group and use the individual item color pickers. Group-level colors are just a convenience feature.

**Q: What happens to items not in Clothing or Attachments?**  
A: They appear in the "Other Items" group, which works the same way but doesn't have group-level color selection.
