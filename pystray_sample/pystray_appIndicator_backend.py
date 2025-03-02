import os
import uuid

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import AppIndicator3, GLib, Gtk
from PIL import Image, ImageDraw, ImageFont

# Global variables
counter = 0
indicator = None
INDICATOR_ID = "time-indicator"  # Fixed ID for the indicator

def create_image_with_text(width, height, text="0000"):
    """Create an icon image with text that works with AppIndicator"""
    # Create a new image with solid white background - AppIndicator works better with this
    image = Image.new("RGBA", (width, height), (255, 255, 255, 255))

    # Use a much smaller font size
    font_size = int(min(width, height) * 0.5)
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size
        )
    except IOError:
        font = ImageFont.load_default()

    # Draw text in black on white background
    dc = ImageDraw.Draw(image)

    # Calculate text width and height to center it - using textbbox instead of deprecated textsize
    left, top, right, bottom = dc.textbbox((0, 0), text, font=font)
    text_width = right - left
    text_height = bottom - top
    position = ((width - text_width) // 2, (height - text_height) // 2)

    # Draw black text on white background
    dc.text(position, text, fill=(0, 0, 0), font=font)

    # Generate a unique filename to prevent caching
    unique_id = uuid.uuid4().hex[:8]
    image_path = f"/tmp/pystray_icon_{text}_{unique_id}.png"
    image.save(image_path)

    return image_path


def update_icon_direct():
    """Update callback that uses AppIndicator directly"""
    global counter, indicator
    counter += 1

    # Create a new image with updated counter and get its path
    icon_path = create_image_with_text(64, 64, str(counter))

    # Update the icon of the existing indicator
    indicator.set_icon_full(icon_path, f"Counter: {counter}")

    print(f"Updated icon to: {counter}")
    return True  # Keep the timer running


def setup_indicator():
    """Set up the AppIndicator directly"""
    global indicator

    # Create initial icon
    initial_icon = create_image_with_text(64, 64, "1")

    # Create a single indicator with fixed ID
    indicator = AppIndicator3.Indicator.new(
        INDICATOR_ID, initial_icon, AppIndicator3.IndicatorCategory.APPLICATION_STATUS
    )

    # Set the status to active
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    # Create a menu
    menu = Gtk.Menu()
    item_quit = Gtk.MenuItem(label="Exit")
    item_quit.connect("activate", lambda _: Gtk.main_quit())
    menu.append(item_quit)
    menu.show_all()
    indicator.set_menu(menu)


if __name__ == '__main__':
    # Set up the AppIndicator
    setup_indicator()

    # Set up the timer directly with GTK - run slightly faster to compensate for any missed frames
    GLib.timeout_add(800, update_icon_direct)  # 800ms instead of 1000ms

    # Run the GTK main loop
    try:
        Gtk.main()
    except KeyboardInterrupt:
        print("Keyboard interrupt received, shutting down...")

    print("GTK main loop exited, program ending")
