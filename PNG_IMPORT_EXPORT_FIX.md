# PNG Import/Export Fix Documentation

## Problem Summary

The PNG import/export feature in the Blockbuster Character Palette Editor had two critical issues:

### Issue #1: Incorrect Color in Gaps Between Sub-Regions
- **Location**: Coordinate (608, 96)
- **Expected**: Should remain black (unmapped region)
- **Actual**: Filled with #efefef (incorrect color from parent region)
- **Cause**: Import function was extracting dominant color from entire parent region instead of sampling exact pixels

### Issue #2: Coloring Black/Unmapped Regions
- **Location**: Coordinate (576, 960)
- **Expected**: Should remain black (input is black at this pixel)
- **Actual**: Filled with #e41ae3 (dominant color from non-black parts of region)
- **Cause**: Import function was including all pixels (including black ones) when calculating dominant color

## Root Cause Analysis

### Old (Buggy) Behavior

The `import_texture()` function in `palette_editor.py` worked as follows:

1. For each region (including parent regions), scan ALL pixels in the region bounds
2. Collect all non-black, non-white pixels
3. Calculate the dominant (most common) color from those pixels
4. Assign that dominant color to the region

Problems with this approach:
- Parent regions (like "Knee Attire Left") cover large areas (e.g., 64x320 pixels)
- The dominant color from such a large area doesn't represent any specific sub-region
- Gaps between sub-regions would be filled with the parent's dominant color
- Black pixels at specific coordinates were ignored, but the region still got colored

### New (Fixed) Behavior

The updated `import_texture()` function now:

1. For each region, sample ONLY the exact pixel at the region's start position (x, y)
2. If that pixel is black (#000000), skip the region (don't import it)
3. Otherwise, use that exact pixel's color for the region

Additionally, the `update_preview()` and `export_png()` functions now:

1. Skip parent regions (only fill leaf regions that don't have sub-regions)
2. Skip regions with empty or black colors
3. This ensures gaps remain black and unmapped areas aren't filled

## Implementation Details

### Files Modified

#### palette_editor.py

1. **Added parent region tracking**:
   ```python
   # In __init__
   self.parent_regions = set()  # Set of paths for parent regions
   
   # In load_palette_data
   self.parent_regions = self._find_parent_regions(self.palette_data)
   ```

2. **New method to identify parent regions**:
   ```python
   def _find_parent_regions(self, data, path="", parents=None):
       """Recursively find all regions that have sub-regions"""
       # Returns set of paths for regions that have sub-regions
   ```

3. **Updated import_texture()**:
   ```python
   # OLD: Extract all non-black pixels and find dominant
   region_colors = []
   for y in range(entry.y, min(entry.y + entry.height, img.size[1])):
       for x in range(entry.x, min(entry.x + entry.width, img.size[0])):
           color = pixels[x, y]
           hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
           if hex_color not in ["#000000", "#ffffff"]:
               region_colors.append(hex_color)
   if region_colors:
       color_counter = Counter(region_colors)
       dominant_color = color_counter.most_common(1)[0][0]
       entry.color = dominant_color
   
   # NEW: Sample exact pixel at region start
   if entry.x < img.size[0] and entry.y < img.size[1]:
       color = pixels[entry.x, entry.y]
       hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
       if hex_color != "#000000":  # Skip black regions
           entry.color = hex_color
   ```

4. **Updated update_preview()**:
   ```python
   # NEW: Skip parent regions and empty colors
   for path, entry in self.color_entries.items():
       if path in self.parent_regions:  # Skip parents
           continue
       if not entry.color or entry.color == "" or entry.color == "#000000":  # Skip empty
           continue
       # ... fill region ...
   ```

### Tests Added

1. **test_import_export_fix.py**: Unit tests for the fix logic
   - Tests exact pixel sampling
   - Tests black region skipping
   - Tests parent region identification

2. **test_e2e_import_export.py**: End-to-end integration test
   - Simulates full import/export workflow
   - Validates both issues are fixed
   - Tests control regions to ensure no regression

## Test Results

### Before Fix
```
Position (608, 96):
  Input: #224a67
  Output: #efefef  ✗ WRONG

Position (576, 960):
  Input: #000000
  Output: #e41ae3  ✗ WRONG
```

### After Fix
```
Position (608, 96):
  Input: #224a67
  Output: #000000  ✓ CORRECT (gap remains unmapped)

Position (576, 960):
  Input: #000000
  Output: #000000  ✓ CORRECT (black region preserved)
```

### Existing Tests
All existing tests continue to pass:
- test_palette_editor.py ✓
- test_enhancements.py ✓
- test_grouped_palette.py ✓

## Impact

### What Changed
- Import now uses exact pixel sampling instead of dominant color across regions
- Black/unmapped regions are correctly skipped during import
- Parent regions are no longer filled during export
- Gaps between sub-regions remain black (unmapped)

### What Stayed The Same
- All normal color regions continue to work correctly
- Auto-calculation of shades and highlights still works
- Group color application still works
- All existing functionality is preserved

## Migration Notes

No migration needed. The changes are backward compatible:
- Existing configuration files work unchanged
- Existing textures can be imported with better fidelity
- Export behavior is more accurate (but different from buggy version)

## Future Improvements

Potential enhancements that could build on this fix:

1. Option to import dominant color vs exact pixel (for flexibility)
2. Visual indication in UI of which regions are parent vs leaf
3. Validation warnings when gaps are detected in coordinate space
4. Option to auto-fill gaps with interpolated colors from neighbors

## References

- GitHub Issue: https://github.com/Stimpicus/Blockbuster/issues/4
- SaveCharacterPalette.json: https://github.com/Stimpicus/Blockbuster/blob/ba0365c0fb1ff59bbc68e2fdfe707e75e9f3a387/SaveCharacterPalette.json
