from tkinter import *
from device_entry_toplevel import spawnDeviceEntryTopLevel
from voltage_tile_entity import spawnVoltageTile
import app_common

app_common.app.geometry("500x500+0+220")
spawnDeviceEntryTopLevel()
spawnVoltageTile()

app_common.app.mainloop()