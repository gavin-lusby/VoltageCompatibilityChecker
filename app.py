from tkinter import *
from device_entry_toplevel import createDeviceEntryTopLevel
import app_common

app_common.app.geometry("500x500+0+220")
createDeviceEntryTopLevel()


app_common.app.mainloop()