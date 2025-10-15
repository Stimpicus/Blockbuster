#!/usr/bin/env python3
"""
Character Palette Editor
A GUI application for editing SaveCharacterPalette.json configuration files
with live PNG preview generation.
"""

import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
from PIL import Image, ImageTk
import os
from typing import Dict, Any, List, Tuple
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


class ColorEntry:
    """Represents a single color entry in the palette"""
    def __init__(self, name: str, x: int, y: int, width: int, height: int, color: str = ""):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color if color else "#000000"


class PaletteEditor:
    """Main application class for the character palette editor"""
    
    # Define color groups
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
    
    def __init__(self, root):
        self.root = root
        self.root.title("Character Palette Editor")
        self.root.geometry("1400x900")
        
        self.config_file = None
        self.palette_data = []
        self.color_entries = {}  # Maps path -> ColorEntry
        self.preview_image = None
        self.preview_photo = None
        self.group_frames = {}  # Maps group name -> frame widget
        self.group_expanded = {}  # Maps group name -> bool
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_config)
        file_menu.add_command(label="Open...", command=self.open_config)
        file_menu.add_command(label="Save", command=self.save_config)
        file_menu.add_command(label="Save As...", command=self.save_config_as)
        file_menu.add_separator()
        file_menu.add_command(label="Export PNG...", command=self.export_png)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Main container
        main_container = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel - Color pickers
        left_frame = ttk.Frame(main_container)
        main_container.add(left_frame, weight=1)
        
        ttk.Label(left_frame, text="Color Settings", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Scrollable frame for color pickers
        canvas = tk.Canvas(left_frame)
        scrollbar = ttk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Right panel - Preview
        right_frame = ttk.Frame(main_container)
        main_container.add(right_frame, weight=1)
        
        ttk.Label(right_frame, text="Preview (1024x1024)", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Preview canvas
        self.preview_canvas = tk.Canvas(right_frame, width=600, height=600, bg='white')
        self.preview_canvas.pack(pady=10)
        
        # Refresh button
        ttk.Button(right_frame, text="Refresh Preview", command=self.update_preview).pack(pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready. Open or create a configuration file.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def new_config(self):
        """Create a new configuration from template"""
        template_path = os.path.join(os.path.dirname(__file__), "SaveCharacterPalette.json")
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                self.palette_data = json.load(f)
            self.config_file = None
            self.load_palette_data()
            self.status_var.set("New configuration created from template")
        else:
            messagebox.showerror("Error", "Template file SaveCharacterPalette.json not found")
    
    def open_config(self):
        """Open an existing configuration file"""
        filename = filedialog.askopenfilename(
            title="Open Configuration",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.palette_data = json.load(f)
                self.config_file = filename
                self.load_palette_data()
                self.status_var.set(f"Loaded: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def save_config(self):
        """Save the current configuration"""
        if self.config_file:
            self.save_to_file(self.config_file)
        else:
            self.save_config_as()
    
    def save_config_as(self):
        """Save the configuration to a new file"""
        filename = filedialog.asksaveasfilename(
            title="Save Configuration As",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.save_to_file(filename)
            self.config_file = filename
    
    def save_to_file(self, filename):
        """Save the configuration data to a file"""
        try:
            # Update palette_data with current color values
            self.update_palette_data_from_entries()
            
            with open(filename, 'w') as f:
                json.dump(self.palette_data, f, indent=2)
            self.status_var.set(f"Saved: {os.path.basename(filename)}")
            messagebox.showinfo("Success", "Configuration saved successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def update_palette_data_from_entries(self):
        """Update the palette data structure with values from color entries"""
        for path, entry in self.color_entries.items():
            parts = path.split('.')
            current = self.palette_data
            
            # Navigate to the right position in the nested structure
            for i, part in enumerate(parts[:-1]):
                if part.isdigit():
                    current = current[int(part)]
                else:
                    current = current[part]
            
            # Update the color value
            last_part = parts[-1]
            if last_part.isdigit():
                current[int(last_part)]["Color"] = entry.color
            else:
                current[last_part]["Color"] = entry.color
    
    def load_palette_data(self):
        """Load the palette data and create color picker widgets"""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        self.color_entries.clear()
        self.group_frames.clear()
        self.group_expanded = {}
        
        # Create grouped sections
        self.create_group_section("Clothing", self.CLOTHING_GROUP)
        self.create_group_section("Attachments", self.ATTACHMENTS_GROUP)
        
        # Create section for all other items
        other_items = []
        for item in self.palette_data:
            item_name = list(item.keys())[0]
            if item_name not in self.CLOTHING_GROUP and item_name not in self.ATTACHMENTS_GROUP:
                other_items.append(item_name)
        
        if other_items:
            self.create_other_items_section(other_items)
        
        # Update preview
        self.update_preview()
    
    def create_group_section(self, group_name: str, item_names: List[str]):
        """Create a collapsible section for a group"""
        # Main frame for the group
        group_container = ttk.Frame(self.scrollable_frame, relief=tk.RIDGE, borderwidth=2)
        group_container.pack(fill=tk.X, padx=5, pady=5)
        
        # Header with expand/collapse button
        header_frame = ttk.Frame(group_container)
        header_frame.pack(fill=tk.X)
        
        # Expand/collapse button
        self.group_expanded[group_name] = False
        expand_var = tk.StringVar(value="▶")
        expand_btn = ttk.Button(
            header_frame, 
            textvariable=expand_var, 
            width=3,
            command=lambda: self.toggle_group(group_name, expand_var)
        )
        expand_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Group name label
        ttk.Label(header_frame, text=group_name, font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Group color pickers (Color 1-5)
        color_frame = ttk.Frame(header_frame)
        color_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(color_frame, text="Group Colors:").pack(side=tk.LEFT, padx=5)
        
        for i in range(1, 6):
            color_id = f"Color {i}"
            btn_frame = ttk.Frame(color_frame)
            btn_frame.pack(side=tk.LEFT, padx=2)
            
            ttk.Label(btn_frame, text=f"C{i}:", font=('Arial', 8)).pack(side=tk.LEFT)
            color_btn = tk.Button(
                btn_frame,
                bg="#000000",
                width=3,
                height=1,
                command=lambda g=group_name, c=color_id: self.choose_group_color(g, c)
            )
            color_btn.pack(side=tk.LEFT)
            color_btn.group_color_id = color_id
        
        # Content frame (collapsed by default)
        content_frame = ttk.Frame(group_container)
        self.group_frames[group_name] = {
            'expand_var': expand_var,
            'content_frame': content_frame,
            'header_frame': header_frame
        }
        
        # Add items to the group
        for item_name in item_names:
            # Find the item in palette_data
            for idx, item in enumerate(self.palette_data):
                if list(item.keys())[0] == item_name:
                    self.parse_palette_structure(
                        item, 
                        str(idx), 
                        content_frame,
                        level=0,
                        group_name=group_name
                    )
                    break
    
    def toggle_group(self, group_name: str, expand_var: tk.StringVar):
        """Toggle expansion/collapse of a group"""
        self.group_expanded[group_name] = not self.group_expanded[group_name]
        
        if self.group_expanded[group_name]:
            expand_var.set("▼")
            self.group_frames[group_name]['content_frame'].pack(fill=tk.BOTH, expand=True)
        else:
            expand_var.set("▶")
            self.group_frames[group_name]['content_frame'].pack_forget()
    
    def choose_group_color(self, group_name: str, color_id: str):
        """Choose a color for all items in a group"""
        color = colorchooser.askcolor(title=f"Choose {color_id} for {group_name}")
        
        if color[1]:  # color[1] is the hex value
            # Apply to all items in the group
            if group_name == "Clothing":
                item_names = self.CLOTHING_GROUP
            elif group_name == "Attachments":
                item_names = self.ATTACHMENTS_GROUP
            else:
                return
            
            # Apply the color to all matching items
            for path, entry in self.color_entries.items():
                # Check if this entry belongs to an item in the group and matches the color ID
                for item_name in item_names:
                    if item_name in path and color_id in path:
                        entry.color = color[1]
                        # Also auto-calculate shade and highlight
                        if "Shade" in path:
                            entry.color = calculate_shade(color[1])
                        elif "Highlight" in path:
                            entry.color = calculate_highlight(color[1])
            
            self.update_preview()
            self.status_var.set(f"Applied {color_id} to all items in {group_name}")
    
    def create_other_items_section(self, item_names: List[str]):
        """Create a section for non-grouped items"""
        # Main frame for other items
        other_container = ttk.Frame(self.scrollable_frame, relief=tk.RIDGE, borderwidth=2)
        other_container.pack(fill=tk.X, padx=5, pady=5)
        
        # Header with expand/collapse button
        header_frame = ttk.Frame(other_container)
        header_frame.pack(fill=tk.X)
        
        # Expand/collapse button
        self.group_expanded['Other'] = False
        expand_var = tk.StringVar(value="▶")
        expand_btn = ttk.Button(
            header_frame, 
            textvariable=expand_var, 
            width=3,
            command=lambda: self.toggle_group('Other', expand_var)
        )
        expand_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Group name label
        ttk.Label(header_frame, text="Other Items", font=('Arial', 11, 'bold')).pack(side=tk.LEFT, padx=5)
        
        # Content frame (collapsed by default)
        content_frame = ttk.Frame(other_container)
        self.group_frames['Other'] = {
            'expand_var': expand_var,
            'content_frame': content_frame,
            'header_frame': header_frame
        }
        
        # Add items to the section
        for item_name in item_names:
            # Find the item in palette_data
            for idx, item in enumerate(self.palette_data):
                if list(item.keys())[0] == item_name:
                    self.parse_palette_structure(
                        item, 
                        str(idx), 
                        content_frame,
                        level=0,
                        group_name='Other'
                    )
                    break
    
    def parse_palette_structure(self, data: Any, path: str, parent_frame: ttk.Frame, level: int = 0, group_name: str = None):
        """Recursively parse the palette structure and create widgets"""
        if isinstance(data, list):
            for i, item in enumerate(data):
                new_path = f"{path}.{i}" if path else str(i)
                self.parse_palette_structure(item, new_path, parent_frame, level, group_name)
        
        elif isinstance(data, dict):
            # Check if this dict has position and color info
            has_position = all(k in data for k in ["Start X", "Start Y", "Width", "Height"])
            
            if has_position:
                # This is a color region
                region_name = path.split('.')[-1] if '.' in path else path
                
                # Get the region name from the parent key
                parts = path.split('.')
                if len(parts) >= 2:
                    # Get actual region name from data structure
                    region_name = self.get_region_name_from_path(parts)
                
                # Create a color entry if it has a Color field
                if "Color" in data:
                    x = int(data["Start X"])
                    y = int(data["Start Y"])
                    w = int(data["Width"])
                    h = int(data["Height"])
                    color = data.get("Color", "#000000")
                    if not color:
                        color = "#000000"
                    
                    entry = ColorEntry(region_name, x, y, w, h, color)
                    self.color_entries[path] = entry
                    
                    # Create UI widget
                    self.create_color_picker_widget(parent_frame, region_name, path, color, level)
            
            # Recurse into nested structures
            for key, value in data.items():
                if key not in ["Start X", "Start Y", "Width", "Height", "Color"]:
                    new_path = f"{path}.{key}" if path else key
                    self.parse_palette_structure(value, new_path, parent_frame, level + 1, group_name)
    
    def get_region_name_from_path(self, parts: List[str]) -> str:
        """Get human-readable region name from path parts"""
        # Filter out numeric indices and get meaningful names
        names = [p for p in parts if not p.isdigit()]
        return " - ".join(names) if names else "Unknown"
    
    def create_color_picker_widget(self, parent: ttk.Frame, name: str, path: str, color: str, level: int):
        """Create a color picker widget for a region"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, padx=(level * 20, 5), pady=2)
        
        # Label
        label = ttk.Label(frame, text=name, width=40, anchor=tk.W)
        label.pack(side=tk.LEFT, padx=5)
        
        # Color display button
        color_btn = tk.Button(
            frame,
            bg=color,
            width=10,
            command=lambda: self.choose_color(path, color_btn)
        )
        color_btn.pack(side=tk.LEFT, padx=5)
        
        # Color code entry
        color_entry = ttk.Entry(frame, width=10)
        color_entry.insert(0, color)
        color_entry.pack(side=tk.LEFT, padx=5)
        
        # Bind entry changes
        color_entry.bind('<Return>', lambda e: self.update_color_from_entry(path, color_entry, color_btn))
        color_entry.bind('<FocusOut>', lambda e: self.update_color_from_entry(path, color_entry, color_btn))
        
        # Store references
        color_btn.color_entry_widget = color_entry
    
    def choose_color(self, path: str, button: tk.Button):
        """Open color chooser dialog"""
        current_color = self.color_entries[path].color
        color = colorchooser.askcolor(title="Choose color", initialcolor=current_color)
        
        if color[1]:  # color[1] is the hex value
            self.color_entries[path].color = color[1]
            button.configure(bg=color[1])
            button.color_entry_widget.delete(0, tk.END)
            button.color_entry_widget.insert(0, color[1])
            
            # Auto-calculate shade and highlight if this is a base color (Color 1-5)
            if any(f"Color {i}" in path for i in range(1, 6)):
                # Find and update corresponding Shade and Highlight
                base_path = path
                shade_path = f"{base_path}.Shade"
                highlight_path = f"{base_path}.Highlight"
                
                if shade_path in self.color_entries:
                    shade_color = calculate_shade(color[1])
                    self.color_entries[shade_path].color = shade_color
                
                if highlight_path in self.color_entries:
                    highlight_color = calculate_highlight(color[1])
                    self.color_entries[highlight_path].color = highlight_color
            
            self.update_preview()
    
    def update_color_from_entry(self, path: str, entry: ttk.Entry, button: tk.Button):
        """Update color from manual entry"""
        color_value = entry.get().strip()
        
        # Validate hex color
        if not color_value.startswith('#'):
            color_value = '#' + color_value
        
        try:
            # Try to use the color
            button.configure(bg=color_value)
            self.color_entries[path].color = color_value
            
            # Auto-calculate shade and highlight if this is a base color (Color 1-5)
            if any(f"Color {i}" in path for i in range(1, 6)):
                # Find and update corresponding Shade and Highlight
                base_path = path
                shade_path = f"{base_path}.Shade"
                highlight_path = f"{base_path}.Highlight"
                
                if shade_path in self.color_entries:
                    shade_color = calculate_shade(color_value)
                    self.color_entries[shade_path].color = shade_color
                
                if highlight_path in self.color_entries:
                    highlight_color = calculate_highlight(color_value)
                    self.color_entries[highlight_path].color = highlight_color
            
            self.update_preview()
        except tk.TclError:
            messagebox.showerror("Error", f"Invalid color value: {color_value}")
            entry.delete(0, tk.END)
            entry.insert(0, self.color_entries[path].color)
    
    def update_preview(self):
        """Generate and display the PNG preview"""
        try:
            # Create 1024x1024 image
            img = Image.new('RGB', (1024, 1024), color='black')
            pixels = img.load()
            
            # Fill regions with colors
            for path, entry in self.color_entries.items():
                # Convert hex to RGB
                color_hex = entry.color.lstrip('#')
                r, g, b = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))
                
                # Fill the region
                for y in range(entry.y, min(entry.y + entry.height, 1024)):
                    for x in range(entry.x, min(entry.x + entry.width, 1024)):
                        pixels[x, y] = (r, g, b)
            
            self.preview_image = img
            
            # Scale down for display (max 600x600)
            display_img = img.copy()
            display_img.thumbnail((600, 600), Image.Resampling.LANCZOS)
            
            self.preview_photo = ImageTk.PhotoImage(display_img)
            
            # Update canvas
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(300, 300, image=self.preview_photo, anchor=tk.CENTER)
            
            self.status_var.set("Preview updated")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate preview: {str(e)}")
    
    def export_png(self):
        """Export the current palette as a PNG file"""
        if not self.preview_image:
            self.update_preview()
        
        if self.preview_image:
            filename = filedialog.asksaveasfilename(
                title="Export PNG",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            if filename:
                try:
                    self.preview_image.save(filename, 'PNG')
                    self.status_var.set(f"Exported: {os.path.basename(filename)}")
                    messagebox.showinfo("Success", "PNG exported successfully")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to export PNG: {str(e)}")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = PaletteEditor(root)
    
    # Load default template if it exists
    template_path = os.path.join(os.path.dirname(__file__), "SaveCharacterPalette.json")
    if os.path.exists(template_path):
        try:
            with open(template_path, 'r') as f:
                app.palette_data = json.load(f)
            app.load_palette_data()
            app.status_var.set("Loaded default template")
        except:
            pass
    
    root.mainloop()


if __name__ == "__main__":
    main()
