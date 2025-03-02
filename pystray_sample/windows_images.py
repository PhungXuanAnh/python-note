#!/usr/bin/env python3
import os

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")  # Changed this to match GTK version
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import Gdk, GdkPixbuf, GLib, Gtk


class ImageWindow(Gtk.Window):
    def __init__(self, file_path, permanent=False):
        super().__init__(title="Image Viewer")
        self.set_border_width(10)
        self.permanent = permanent

        # Create a scrolled window to handle large images
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_hexpand(True)
        scrolled_window.set_vexpand(True)
        self.add(scrolled_window)

        # Create GTK image from file
        image = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file(file_path)
        image.set_from_pixbuf(pixbuf)

        # Get image dimensions
        img_width = pixbuf.get_width()
        img_height = pixbuf.get_height()
        
        # Get screen dimensions using non-deprecated methods
        display = Gdk.Display.get_default()
        # For different GTK versions
        screen_width = 0
        screen_height = 0

        # Try the modern approach first
        try:
            if hasattr(display, "get_primary_monitor"):
                monitor = display.get_primary_monitor()
            else:
                monitor = display.get_monitor(0)

            geometry = monitor.get_geometry()
            screen_width = geometry.width * 0.9
            screen_height = geometry.height * 0.8
        except (AttributeError, TypeError):
            # Fall back to the old method if needed
            screen = Gdk.Screen.get_default()
            screen_width = screen.get_width() * 0.9
            screen_height = screen.get_height() * 0.8
        
        # Calculate window size (with padding)
        window_width = min(img_width + 30, screen_width)
        window_height = min(img_height + 50, screen_height)
        
        # Set window size based on image dimensions
        self.set_default_size(int(window_width), int(window_height))
        
        scrolled_window.add(image)


class ImageDisplayManager:
    def __init__(self, on_finish_callback=None):
        self.image_window = None
        self.cycle_count = 0
        self.file_path = "/home/xuananh/Downloads/warning-sitting-a-long-time.jpg"
        self.on_finish_callback = on_finish_callback
        
        # Define display and pause durations for each cycle (in milliseconds)
        self.display_durations = [500, 1000, 1000, -1]  # -1 means permanent
        self.pause_durations = [1500, 1500, 1500]  # time between cycles

    def open_image_window(self):
        # Open the image in a new window
        try:
            # Check if we're on the last cycle (permanent window)
            permanent = (self.cycle_count == len(self.display_durations) - 1)
            self.image_window = ImageWindow(self.file_path, permanent)
            
            # Connect destroy signal to our handler, not directly to Gtk.main_quit
            if permanent:
                self.image_window.connect("destroy", self.on_final_window_closed)
                
            self.image_window.show_all()
            
            print(f"Window opened (cycle {self.cycle_count + 1})")
            
            # If not permanent, set timer to close window after specified duration
            if not permanent:
                # Get the display duration for this cycle in milliseconds
                display_duration = self.display_durations[self.cycle_count]
                # Convert to milliseconds for timeout_add
                GLib.timeout_add(display_duration, self.close_image_window)
            
            self.cycle_count += 1
            
        except Exception as e:
            print(f"Error loading image: {e}")
            self.finish_display_cycle()
            
        return False  # Important to return False to stop the timer from repeating
    
    def close_image_window(self):
        if self.image_window:
            self.image_window.destroy()
            print(f"Window closed (after cycle {self.cycle_count})")
            
            # If there are more cycles to go
            if self.cycle_count < len(self.display_durations):
                # Schedule the next opening with the corresponding pause duration
                pause_duration = self.pause_durations[self.cycle_count - 1]
                print(f"Scheduling next opening in {pause_duration}ms")
                GLib.timeout_add(pause_duration, self.open_image_window)
            else:
                self.finish_display_cycle()
            
        return False  # Important to return False to stop the timer from repeating
    
    def on_final_window_closed(self, window):
        """Handler for the destroy signal of the final window"""
        self.finish_display_cycle()
        
    def finish_display_cycle(self):
        """Call the finish callback if provided instead of quitting"""
        if self.on_finish_callback:
            self.on_finish_callback()


def main():
    manager = ImageDisplayManager()
    # Start the cycle
    manager.open_image_window()
    Gtk.main()


if __name__ == "__main__":
    main()
