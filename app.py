from tkinter import *
from device_entry_toplevel import spawnDeviceEntryTopLevel
from voltage_tile_entity import spawnVoltageTile
import app_common

app_common.app.geometry("500x500+0+220")
spawnDeviceEntryTopLevel()
spawnVoltageTile()

app_common.app.mainloop()

"""TODO:
noise margin calculation
Add trapezoid red/green indicating if devices are compatible
add red text hightlighting(if possible) to dropdown to
indicate device to be selected will not be compatible
with currently selected OTHER device
Add save to CSV feature
Add import from CSV feature
cleanup import/export
Add voltage linear equation instead of only VCC or only constant (x*Vcc + y)"""