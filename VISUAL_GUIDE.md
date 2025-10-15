# Visual Guide to Enhanced Palette Editor

## UI Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ File                                                                        │
│  ├─ New                                                                     │
│  ├─ Open...                                                                 │
│  ├─ Save                                                                    │
│  ├─ Save As...                                                              │
│  ├─ ──────────                                                              │
│  ├─ Import Texture PNG...    ← NEW FEATURE                                 │
│  ├─ ──────────                                                              │
│  ├─ Export PNG...                                                           │
│  └─ Exit                                                                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────┬──────────────────────────────────────────────┐
│ Color Settings               │ Preview (1024x1024)                          │
├──────────────────────────────┤                                              │
│                              │                                              │
│ ▶ Clothing                   │      ┌────────────────────────┐             │
│   Group Colors:              │      │                        │             │
│   C1: [█] #ff0000  ← NEW     │      │   Live Preview Image   │             │
│   C2: [█] #00ff00  ← NEW     │      │   Updates in Real-Time │             │
│   C3: [█] #0000ff  ← NEW     │      │                        │             │
│   C4: [█] #ffff00  ← NEW     │      │   Shows all color      │             │
│   C5: [█] #ff00ff  ← NEW     │      │   regions as defined   │
│                              │      │   in configuration     │             │
│ ▶ Attachments                │      │                        │             │
│   Group Colors:              │      └────────────────────────┘             │
│   C1: [█] #000000  ← NEW     │                                              │
│   C2: [█] #000000  ← NEW     │      [Refresh Preview]                      │
│   ... (same as above)        │                                              │
│                              │                                              │
│ ▶ Other Items                │                                              │
│                              │                                              │
└──────────────────────────────┴──────────────────────────────────────────────┘
│ Ready. Open or create a configuration file.                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Feature 1: Group-Level Hex Input

### Before (Old UI)
```
▶ Clothing
  Group Colors:
  C1: [█]     ← Only color picker button
  C2: [█]
  C3: [█]
```

### After (New UI)
```
▶ Clothing
  Group Colors:
  C1: [█] #ff0000  ← Button + Hex Input Field
  C2: [█] #00ff00  ← Button + Hex Input Field
  C3: [█] #0000ff  ← Button + Hex Input Field
```

### Usage
1. Click color button → Color picker dialog
2. OR type hex code → Press Enter
3. Both methods update all items in group

## Feature 2: Group-Level Color Propagation

### What Happens When You Select a Group Color

```
User selects "C1: #ff0000" for Clothing group
                    ↓
        ┌───────────┴───────────┐
        │                       │
    Updates ALL Items       Auto-Calculates
    in Clothing Group       Shade & Highlight
        │                       │
        ├─ Torso               ├─ Shade: #990000
        ├─ Arm Attire Left     └─ Highlight: #ff3232
        ├─ Arm Attire Right
        ├─ Hand Attire Left
        ├─ Hand Attire Right
        ├─ Hips
        ├─ Leg Left
        ├─ Leg Right
        ├─ Foot Left
        └─ Foot Right
                    ↓
        All UI widgets update visually
                    ↓
        Changes saved to configuration
```

## Feature 3: Import Texture PNG

### Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│ 1. User: File → Import Texture PNG...                              │
│ 2. Select PNG file (preferably 1024x1024)                          │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│ 3. Application analyzes each region:                               │
│                                                                     │
│    For each region (e.g., Torso.Color 1):                          │
│    ┌───────────────────────────────────────────────┐               │
│    │ a. Extract pixels from region bounds          │               │
│    │ b. Convert to hex colors                      │               │
│    │ c. Exclude #000000 and #ffffff                │               │
│    │ d. Count color occurrences                    │               │
│    │ e. Select most common color                   │               │
│    │ f. Update color entry                         │               │
│    └───────────────────────────────────────────────┘               │
│                                                                     │
│    Example:                                                         │
│    Region: Torso.Color 1 (x:0, y:0, w:32, h:64)                    │
│    Pixel colors found:                                              │
│      #ff0000: 1500 pixels  ← Most common                           │
│      #ff0011: 200 pixels                                            │
│      #fe0000: 100 pixels                                            │
│      #000000: 50 pixels (excluded)                                  │
│                                                                     │
│    Selected: #ff0000                                                │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│ 4. All color entries updated                                       │
│ 5. All UI widgets updated                                          │
│ 6. Preview refreshed                                               │
│ 7. User notified of success                                        │
└─────────────────────────────────────────────────────────────────────┘
```

## Feature 4: UI Synchronization

### Color Update Flow

```
User changes a color
        ↓
┌───────┴────────────────────────────────────────┐
│                                                │
│  Via Color Picker    Via Hex Input    Via Group Selection
│        ↓                   ↓                   ↓
│   choose_color()  update_color_from_entry()  apply_group_color()
│        ↓                   ↓                   ↓
└────────┴───────────────────┴───────────────────┘
                    ↓
        Update ColorEntry.color
                    ↓
        ┌───────────┴───────────┐
        │                       │
   If base color          Update UI widgets
   (Color 1-5)                  ↓
        ↓               update_color_widgets()
   Calculate                    ↓
   Shade & Highlight      For each path:
        ↓                 - Update button bg
   Update entries         - Update hex entry text
        ↓
   Update widgets
        │
        └───────────┬───────────┘
                    ↓
            update_preview()
                    ↓
        User sees changes immediately
```

## Individual Region Color Picker (Unchanged)

When a group is expanded, individual regions still have their own controls:

```
▼ Clothing  ← Expanded
  Group Colors: C1: [█] #ff0000 ...
  
  Individual Items:
  
  Torso
    ├─ Torso - Color 1        [█] #ff0000  ← Button + Hex Input
    ├─ Torso - Color 1 - Shade    [█] #990000  ← Auto-calculated
    ├─ Torso - Color 1 - Highlight [█] #ff3232  ← Auto-calculated
    ├─ Torso - Color 2        [█] #00ff00
    └─ ...
  
  Arm Attire Left
    ├─ Arm Attire Left - Color 1  [█] #ff0000  ← Same as group
    └─ ...
```

## Color Auto-Calculation

### Algorithm

```
Base Color: #ff0000 (Red)
        │
        ├─ Shade (60% brightness)
        │  ├─ Convert to HSV: (0°, 100%, 100%)
        │  ├─ Reduce V: (0°, 100%, 60%)
        │  └─ Convert to RGB: #990000
        │
        └─ Highlight (140% brightness, 80% saturation)
           ├─ Convert to HSV: (0°, 100%, 100%)
           ├─ Increase V: (0°, 100%, 100%) [capped at 100%]
           ├─ Reduce S: (0°, 80%, 100%)
           └─ Convert to RGB: #ff3232
```

## Example Use Cases

### Use Case 1: Quick Color Scheme
```
1. Open or create configuration
2. Set C1-C5 for Clothing group using hex inputs
3. All clothing items get those colors instantly
4. Shade/Highlight auto-calculated
5. Save and export PNG
```

### Use Case 2: Copy from Existing Texture
```
1. Open or create configuration
2. File → Import Texture PNG...
3. Select existing character texture
4. All colors extracted automatically
5. Fine-tune individual colors if needed
6. Save configuration
```

### Use Case 3: Consistent Color Palette
```
1. Create configuration
2. Use group colors to ensure consistency
3. Clothing all uses same color scheme
4. Attachments use complementary colors
5. Export for use in game
```

## Technical Details

### Data Flow

```
palette_data (JSON)
        ↓
ColorEntry objects (Internal model)
        ↓
Widgets (UI layer)
        ↓
User interactions
        ↓
Update ColorEntry.color
        ↓
Update widgets (sync UI)
        ↓
Update preview (visual feedback)
        ↓
Save to palette_data (persist)
```

### Widget References

```
ColorEntry object:
  - name: "Torso - Color 1"
  - x, y, width, height: Region bounds
  - color: "#ff0000"
  - widgets: (color_btn, hex_entry) ← NEW: Direct UI access
```

This allows instant UI updates without searching for widgets!
