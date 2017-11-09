#!/usr/bin/env python  
import gobject  
import dbus  
from dbus.mainloop.glib import DBusGMainLoop  

def filter_cb(bus, message):
    if message.get_member() != "ActiveChanged":
        return
    args = message.get_args_list()
    if args[0] == True:
        print("Lock Screen")
    else:
        print("Unlock Screen")

DBusGMainLoop(set_as_default=True)
bus = dbus.SessionBus()
bus.add_match_string("type='signal',interface='org.gnome.ScreenSaver'")
bus.add_message_filter(filter_cb)
mainloop = gobject.MainLoop()
mainloop.run()