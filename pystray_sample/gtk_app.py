import os
import gi
from pystray_sample_icon_from_created_image import create_image_with_text, icon

gi.require_version("Gtk", "3.0")
from gi.repository import GdkPixbuf, Gtk, Gdk, GLib


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
        
        # Get screen dimensions
        screen = Gdk.Screen.get_default()
        screen_width = screen.get_width() * 0.9  # Use 90% of screen width max
        screen_height = screen.get_height() * 0.8  # Use 80% of screen height max
        
        # Calculate window size (with padding)
        window_width = min(img_width + 30, screen_width)
        window_height = min(img_height + 50, screen_height)
        
        # Set window size based on image dimensions
        self.set_default_size(int(window_width), int(window_height))
        
        scrolled_window.add(image)


class ButtonWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Button Demo")
        self.set_border_width(10)
        self.image_window = None
        self.cycle_count = 0
        self.file_path = "/home/xuananh/Downloads/warning-sitting-a-long-time.jpg"
        
        # Define display and pause durations for each cycle (in milliseconds)
        self.display_durations = [500, 1000, 1000, -1]  # -1 means permanent
        self.pause_durations = [1500, 1500, 1500]  # time between cycles

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        button = Gtk.Button.new_with_label("Click Me")
        button.connect("clicked", self.on_click_me_clicked)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button.new_with_mnemonic("_Open")
        button.connect("clicked", self.on_open_clicked)
        hbox.pack_start(button, True, True, 0)

        button = Gtk.Button.new_with_mnemonic("_Close")
        button.connect("clicked", self.on_close_clicked)
        hbox.pack_start(button, True, True, 0)

    def on_click_me_clicked(self, button):
        print('"Click me" button was clicked')

    def open_image_window(self):
        # Open the image in a new window
        try:
            # Check if we're on the last cycle (permanent window)
            permanent = (self.cycle_count == len(self.display_durations) - 1)
            self.image_window = ImageWindow(self.file_path, permanent)
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
            error_dialog = Gtk.MessageDialog(
                parent=self,
                flags=0,
                message_type=Gtk.MessageType.ERROR,
                buttons=Gtk.ButtonsType.OK,
                text="Error loading image",
            )
            error_dialog.format_secondary_text(str(e))
            error_dialog.run()
            error_dialog.destroy()
            
        return False  # Important to return False to stop the timer from repeating
    
    def close_image_window(self):
        if self.image_window:
            self.image_window.destroy()
            print(f"Window closed (after cycle {self.cycle_count})")
            
            # If there are more cycles to go
            if self.cycle_count < len(self.display_durations):
                # Schedule the next opening with the corresponding pause duration
                pause_duration = self.pause_durations[self.cycle_count - 1]
                GLib.timeout_add(pause_duration, self.open_image_window)
            
        return False  # Important to return False to stop the timer from repeating

    def on_open_clicked(self, button):
        print('"Open" button was clicked')
        
        # Reset cycle count
        self.cycle_count = 0
        
        # Start the cycle
        self.open_image_window()

    def on_close_clicked(self, button):
        print("Closing application")
        Gtk.main_quit()


icon.run_detached()
win = ButtonWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
