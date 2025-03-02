"""
sudo apt install gir1.2-appindicator3-0.1  # If not already installed
"""

import os
import signal
import time

import gi

from pystray_sample.pystray_sample_icon_from_created_image import icon, create_image_with_text
from pystray_sample.windows_images import ImageDisplayManager

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import GLib, Gtk


# Global counter variable
counter = 0
image_manager = None
is_showing_image = False

def reset_counter():
    """Reset the counter to 0 and update the icon"""
    global counter, is_showing_image
    counter = 0
    is_showing_image = False
    
    # Create a new image with updated counter text
    new_image = create_image_with_text(2000, 1000, "black", str(counter))
    
    # Update the icon
    icon.icon = new_image
    
    return False  # Stop the timer from repeating

def update_counter():
    """Update counter and refresh the tray icon"""
    global counter, image_manager, is_showing_image
    
    # Don't update if already showing images
    if is_showing_image:
        return True
    
    counter += 1
    
    # Create a new image with updated counter text
    new_image = create_image_with_text(2000, 1000, "black", str(counter))
    
    # Update the icon
    icon.icon = new_image
    
    # Check if counter exceeds 5
    if counter > 5:
        is_showing_image = True
        
        # Define a callback for when ImageDisplayManager finishes
        def on_image_display_finished():
            # Reset the counter
            GLib.idle_add(reset_counter)
        
        # Create image manager instance with our callback
        image_manager = ImageDisplayManager(on_finish_callback=on_image_display_finished)
        
        # Start the image manager
        image_manager.open_image_window()
        
    # Return True to keep the timer running
    return True


def main():
    # Start the icon in detached mode
    icon.run_detached()
    
    # Set up a timer to update the counter every 1 second (1000 ms)
    GLib.timeout_add(1000, update_counter)
    
    # Handle Ctrl+C in terminal
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, Gtk.main_quit)

    # Start GTK main loop without showing any windows
    Gtk.main()


if __name__ == "__main__":
    main()
