"""
sudo apt install gir1.2-appindicator3-0.1  # If not already installed
"""

import os
import signal

import gi

gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import AppIndicator3, GLib, Gtk


class TrayApp:
    def __init__(self):
        # Create the indicator
        self.indicator = AppIndicator3.Indicator.new(
            "example-tray-app",
            "dialog-information",  # Default icon
            AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
        )

        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

        # Create the menu
        self.menu = Gtk.Menu()

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

    def show_window(self, _):
        """Create and show a window when requested"""
        if self.window is None:
            # Create the window only when needed
            self.window = Gtk.Window(title="Hidden GTK App Window")
            self.window.connect("delete-event", self.hide_window)
            self.window.set_default_size(400, 300)

            # Add some content
            label = Gtk.Label(label="This window was hidden until you requested it!")
            self.window.add(label)

        # Show the window and all its contents
        self.window.show_all()

    def hide_window(self, window, event):
        """Hide window instead of closing the app"""
        window.hide()
        # Return True to prevent the window from being destroyed
        return True

    def quit(self, _):
        """Quit the application"""
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
