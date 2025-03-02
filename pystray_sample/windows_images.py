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

        # Make the window appear on top of other windows
        self.set_keep_above(True)

        # Optional: Set window to appear in all workspaces
        self.set_skip_taskbar_hint(True)  # Hide from taskbar
        self.set_skip_pager_hint(True)  # Hide from pager/workspace switcher
        self.set_urgency_hint(True)  # Add urgency hint (flashing in taskbar)
        self.set_focus_on_map(True)  # Focus window when mapped

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
        
        # Define constant display and pause durations (in milliseconds)
        self.display_duration = 1500  # 1.5 seconds to show image
        self.pause_duration = 1000  # 1 second between images
        self.running = True  # Flag to control the cycle
        self.programmatic_close = False  # Flag to track programmatic window closures

    def open_image_window(self):
        print("Attempting to open image window...")
        # Skip if we're no longer running
        if not self.running:
            print("Not running anymore, stopping cycle")
            return False  # Don't schedule again

        # Open the image in a new window
        try:
            self.image_window = ImageWindow(self.file_path)
            
            # Connect destroy signal to stop cycling when user closes window
            self.image_window.connect("destroy", self.on_window_closed)
                
            self.image_window.show_all()
            print(f"Window opened (cycle {self.cycle_count + 1})")
            
            # Set timer to close window after display duration
            GLib.timeout_add(self.display_duration, self.close_image_window)
            self.cycle_count += 1
            
        except Exception as e:
            print(f"Error loading image: {e}")
            self.finish_display_cycle()
            
        return False

    def close_image_window(self):
        print("Attempting to close image window...")
        if not self.running:
            print("Not running anymore, stopping cycle")
            return False

        if self.image_window:
            try:
                # Set flag to indicate programmatic closure
                self.programmatic_close = True

                self.image_window.destroy()
                self.image_window = None
                print(f"Window closed (after cycle {self.cycle_count})")

                # Reset flag after window is destroyed
                self.programmatic_close = False

                # Schedule the next opening after pause duration
                print(f"Scheduling next window in {self.pause_duration}ms")
                GLib.timeout_add(self.pause_duration, self.open_image_window)
            except Exception as e:
                print(f"Error closing window: {e}")
                self.programmatic_close = False
                self.running = False
        else:
            print("No window to close")

        return False
    
    def on_window_closed(self, window):
        """Handler for when user closes the window"""
        print("Window closed signal received")

        # Only stop the cycle if this wasn't a programmatic close
        if not self.programmatic_close:
            print("User closed the window, stopping cycle")
            self.running = False
            self.finish_display_cycle()
        
    def finish_display_cycle(self):
        """Call the finish callback if provided"""
        self.running = False
        if self.on_finish_callback:
            self.on_finish_callback()

        # Don't call Gtk.main_quit() here - let the parent application control that
        # Only call it when running this script directly
        if __name__ == "__main__":
            Gtk.main_quit()

    def start_cycle(self):
        """Start the display cycle"""
        print("Starting display cycle")
        self.running = True
        # Use timeout_add to start first window
        GLib.timeout_add(0, self.open_image_window)


def main():
    manager = ImageDisplayManager()
    # Start the cycle with the new method
    manager.start_cycle()
    Gtk.main()


if __name__ == "__main__":
    main()
