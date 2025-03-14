#!/usr/bin/env python3
# filepath: /home/xuananh/repo/python-note/pystray_sample/gtk_tray_app_1.py
import os
import signal
import tempfile

import cairo
import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import AppIndicator3, GdkPixbuf, GLib, Gtk


class TrayApp:
    def __init__(self):
        self.count = 2134
        self.temp_icon_path = os.path.join(
            tempfile.gettempdir(), "tray_counter_icon.png"
        )

        # Create initial icon with counter
        self.update_icon()

        # Create the indicator with our custom icon
        self.indicator = AppIndicator3.Indicator.new(
            "example-tray-app",
            self.temp_icon_path,
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )

        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        # Create the menu
        self.menu = Gtk.Menu()

        # Add a menu item to show counter value
        self.counter_item = Gtk.MenuItem(label=f"Counter: {self.count}")
        self.counter_item.set_sensitive(False)  # Make it non-clickable
        self.menu.append(self.counter_item)

        # Add a menu item to reset counter
        item_reset = Gtk.MenuItem(label="Reset Counter")
        item_reset.connect("activate", self.reset_counter)
        self.menu.append(item_reset)

        # Add a menu item to show a window
        item_show = Gtk.MenuItem(label="Show Window")
        item_show.connect("activate", self.show_window)
        self.menu.append(item_show)

        # Add a separator
        self.menu.append(Gtk.SeparatorMenuItem())

        # Add a quit item
        item_quit = Gtk.MenuItem(label="Quit")
        item_quit.connect("activate", self.quit)
        self.menu.append(item_quit)

        # Show all menu items
        self.menu.show_all()

        # Set the menu
        self.indicator.set_menu(self.menu)

        # We'll store our window here, but won't create it yet
        self.window = None

        # Set up a timer to increment the counter every second
        GLib.timeout_add_seconds(1, self.increment_counter)

    def create_counter_icon(self):
        """Create a icon with the counter value"""
        # Create a slightly larger surface to fit 4 digits
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 32, 24)
        context = cairo.Context(surface)

        # Fill with a background color
        context.set_source_rgb(0.2, 0.2, 0.8)  # Blue background
        context.rectangle(0, 0, 32, 24)
        context.fill()

        # Draw counter value
        context.set_source_rgb(1, 1, 1)  # White text
        context.select_font_face(
            "Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD
        )
        
        # Use a smaller font to fit 4 digits
        text = str(self.count)  # No limit - display full count
        
        # Adjust font size based on number length
        if len(text) <= 2:
            context.set_font_size(14)
        elif len(text) == 3:
            context.set_font_size(11)
        else:
            context.set_font_size(9)  # Smaller font for 4 digits

        # Center the text
        x_bearing, y_bearing, width, height, x_advance, y_advance = (
            context.text_extents(text)
        )
        x = (32 - width) / 2 - x_bearing
        y = (24 + height) / 2

        context.move_to(x, y)
        context.show_text(text)

        # Save to a temporary file
        surface.write_to_png(self.temp_icon_path)
        return self.temp_icon_path

    def update_icon(self):
        """Update the icon with current counter value"""
        # Create a new unique path for each icon to prevent caching
        self.temp_icon_path = os.path.join(tempfile.gettempdir(), f"tray_counter_icon_{self.count}.png")
        
        self.create_counter_icon()
        if hasattr(self, 'indicator'):
            # Try to force icon refresh
            self.indicator.set_icon_full(self.temp_icon_path, f"Counter: {self.count}")
            # Give GTK a chance to process events
            while Gtk.events_pending():
                Gtk.main_iteration_do(False)

    def increment_counter(self):
        """Increment the counter and update the icon"""
        self.count += 1
        print(f"Updating counter to: {self.count}")
        
        # Update menu item first
        self.counter_item.set_label(f"Counter: {self.count}")
        
        # Then update icon
        self.update_icon()
        
        # Return True to keep the timer running
        return True

    def reset_counter(self, _):
        """Reset counter to zero"""
        self.count = 0
        self.update_icon()
        self.counter_item.set_label(f"Counter: {self.count}")

    def show_window(self, _):
        """Create and show a window when requested"""
        if self.window is None:
            # Create the window only when needed
            self.window = Gtk.Window(title="Counter Window")
            self.window.connect("delete-event", self.hide_window)
            self.window.set_default_size(250, 150)

            # Create a vertical box
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            vbox.set_margin_top(10)
            vbox.set_margin_bottom(10)
            vbox.set_margin_start(10)
            vbox.set_margin_end(10)
            self.window.add(vbox)

            # Add counter label
            self.window_counter_label = Gtk.Label(label=f"Current count: {self.count}")
            vbox.pack_start(self.window_counter_label, True, True, 0)

            # Add button to update the label
            update_button = Gtk.Button(label="Update Counter Display")
            update_button.connect("clicked", self.update_window_counter)
            vbox.pack_start(update_button, False, False, 0)

        # Update the counter display before showing
        self.window_counter_label.set_text(f"Current count: {self.count}")

        # Show the window and all its contents
        self.window.show_all()

    def update_window_counter(self, button):
        """Update the counter display in the window"""
        self.window_counter_label.set_text(f"Current count: {self.count}")

    def hide_window(self, window, event):
        """Hide window instead of closing the app"""
        window.hide()
        # Return True to prevent the window from being destroyed
        return True

    def quit(self, _):
        """Quit the application"""
        # Clean up the temporary icon file
        if os.path.exists(self.temp_icon_path):
            try:
                os.remove(self.temp_icon_path)
            except:
                pass
        Gtk.main_quit()


def main():
    # Initialize GTK
    app = TrayApp()

    # Handle Ctrl+C in terminal
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, Gtk.main_quit)

    # Start GTK main loop without showing any windows
    Gtk.main()


if __name__ == "__main__":
    main()
