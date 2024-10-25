from tkinter import *
from constants import *
import app_common
from voltage_tile_entity import drawTree

ABSOLUTE_SCALE = 0
VCC_RELATIVE_SCALE = 1
scale_modes = {}
entry_dict = {}
io_mode_selection = IO_BOTH
entry_group = {}

# -------------------------------
# ---------- CALLBACKS ----------
# -------------------------------

def vccEntryCallback(voltage_entry_button, display_name):
    if(scale_modes[display_name] == ABSOLUTE_SCALE):
        scale_modes[display_name] = VCC_RELATIVE_SCALE
        voltage_entry_button.configure(text="×Vcc")

    else:
        scale_modes[display_name] = ABSOLUTE_SCALE
        voltage_entry_button.configure(text="V")

def addEntryCallback():
    failed = False
    new_entry = {}
    new_entry["Name"] = entry_dict["Name"].get()
    new_entry["values"] = {}
    new_entry["io_mode"] = io_mode_selection
    try:
        # No need to keep track of Vcc for IO only inputs
        if(new_entry["io_mode"] != IO_INPUT_ONLY):
            new_entry["values"]["Vcc"] = float(entry_dict["Vcc"].get())
        for entry_label in entry_dict:
            if entry_label in ["Name", "Vcc"]:
                continue
            # Ignore inputs in output mode and outputs in input mode
            if(((new_entry["io_mode"] == IO_OUTPUT_ONLY) and (entry_label in ["Vi min", "Vil max", "Vih min", "Vi max"])) or
               ((new_entry["io_mode"] == IO_INPUT_ONLY) and (entry_label in ["Vo min", "Vol max", "Voh min", "Vo max"]))):
                continue
            read_value = float(entry_dict[entry_label].get())
            if(scale_modes[entry_label] == ABSOLUTE_SCALE):
                new_entry["values"][entry_label] = read_value
            else:
                new_entry["values"][entry_label] = read_value*new_entry["Vcc"]

            
    except ValueError:
        failed = True
        error_message.configure(text="Error: All number fields must contain valid numbers")
    if(not failed):
        error_string = None
        if(new_entry["io_mode"] != IO_OUTPUT_ONLY):
            if((new_entry["values"]["Vi min"] > new_entry["values"]["Vil max"])):
                error_string = "Vi min must be <= Vil max(Vi min=" + \
                    str(new_entry["values"]["Vi min"]) + ", Vil max=" + str(new_entry["values"]["Vil max"]) + ")"
            
            elif((new_entry["values"]["Vil max"] >= new_entry["values"]["Vih min"])):
                error_string = "Vil max must be < Vih min(Vil max=" + \
                    str(new_entry["values"]["Vil max"]) + ", Vih min=" + str(new_entry["values"]["Vih min"]) + ")"
            
            elif((new_entry["values"]["Vih min"] > new_entry["values"]["Vi max"])):
                error_string = "Vih min must be <= Vi max(Vih min=" + \
                    str(new_entry["values"]["Vih min"]) + ", Vi max=" + str(new_entry["values"]["Vi max"]) + ")"
        if(new_entry["io_mode"] != IO_INPUT_ONLY):
            if((new_entry["values"]["Vo min"] > new_entry["values"]["Vol max"])):
                error_string = "Vo min must be <= Vol max(Vo min=" + \
                    str(new_entry["values"]["Vo min"]) + ", Vol max=" + str(new_entry["values"]["Vol max"]) + ")"
            
            elif((new_entry["values"]["Vol max"] >= new_entry["values"]["Voh min"])):
                error_string = "Vol max must be < Voh min(Vol max=" + \
                    str(new_entry["values"]["Vol max"]) + ", Voh min=" + str(new_entry["values"]["Voh min"]) + ")"
            
            elif((new_entry["values"]["Voh min"] > new_entry["values"]["Vo max"])):
                error_string = "Voh min must be <= Vo max(Voh min=" + \
                    str(new_entry["values"]["Voh min"]) + ", Vo max=" + str(new_entry["values"]["Vo max"]) + ")"
            
            elif((new_entry["values"]["Vo max"] > new_entry["values"]["Vcc"])):
                error_string = "Vo max must be <= Vcc(Vo max=" + \
                    str(new_entry["values"]["Vo max"]) + ", Vcc=" + str(new_entry["values"]["Vcc"]) + ")"

        if(error_string != None):
            error_message.configure(text=error_string)
            error_message.grid(column=0, columnspan=4, row=3, padx=10)
        else:
            app_common.device_entries.append(new_entry)
            print(app_common.device_entries)
            error_message.grid_forget()
            if(new_entry["io_mode"] == IO_BOTH):
                canvas_width = DRAWING_WIDTH_FULL
            else:
                canvas_width = DRAWING_WIDTH_FULL/2+2
            new_canvas = Canvas(app_common.app, width=canvas_width, height=DRAWING_HEIGHT, bg="yellow")
            new_canvas.pack(side=LEFT)
            entry_max_voltage = drawTree(new_canvas, app_common.device_entries[len(app_common.device_entries)-1])
            app_common.voltage_tile_entitites.append(new_canvas)
            if(entry_max_voltage > app_common.all_max_voltage):
                app_common.all_max_voltage = entry_max_voltage
                for i in range(len(app_common.device_entries) - 1):
                    app_common.voltage_tile_entitites[i].delete("all")
                    drawTree(app_common.voltage_tile_entitites[i], app_common.device_entries[i])

def switchIOModeCallback():
    global io_mode_selection
    if(io_mode_selection == IO_BOTH):
        io_button.configure(fg="red", text="IO Mode: Only In")
        io_mode_selection = IO_INPUT_ONLY
        entry_group["Vo min"].configure(state="disabled")
        entry_group["Vol max"].configure(state="disabled")
        entry_group["Voh min"].configure(state="disabled")
        entry_group["Vo max"].configure(state="disabled")
    elif(io_mode_selection == IO_INPUT_ONLY):
        io_button.configure(fg="green", text="IO Mode: Only Out")
        io_mode_selection = IO_OUTPUT_ONLY
        entry_group["Vi min"].configure(state="disabled")
        entry_group["Vil max"].configure(state="disabled")
        entry_group["Vih min"].configure(state="disabled")
        entry_group["Vi max"].configure(state="disabled")
        entry_group["Vo min"].configure(state="normal")
        entry_group["Vol max"].configure(state="normal")
        entry_group["Voh min"].configure(state="normal")
        entry_group["Vo max"].configure(state="normal")
    else:
        io_button.configure(fg="blue", text="IO Mode: In/Out")
        io_mode_selection = IO_BOTH
        entry_group["Vi min"].configure(state="normal")
        entry_group["Vil max"].configure(state="normal")
        entry_group["Vih min"].configure(state="normal")
        entry_group["Vi max"].configure(state="normal")

        
# -------------------------------
# ---------- WRAPPERS -----------
# -------------------------------

def createEntryWrapper(display_name, default_text=""):
    entry_stringvar = StringVar()
    entry_frame = Frame(master=device_entry_toplevel, bg="gray")
    entry_field = Entry(entry_frame, fg="gray", textvariable=entry_stringvar)
    entry_label = Label(entry_frame, text=display_name, bg="gray")
    entry_dict[display_name] = entry_stringvar
    
    entry_label.grid(column=0, columnspan=2, row=0, sticky="we")
    entry_field.grid(column=0, row=1, sticky="we")
    entry_stringvar.set(default_text)
    entry_group[display_name] = entry_field
    return entry_frame

def createVoltageEntry(display_name, default_text="0"):
    scale_modes[display_name] = ABSOLUTE_SCALE
    voltage_entry_frame = createEntryWrapper(display_name, default_text)
    voltage_entry_button = Button(voltage_entry_frame, fg="green", text="V", width=4)
    callback = lambda : vccEntryCallback(voltage_entry_button, display_name)
    voltage_entry_button.configure(command=callback)
    voltage_entry_button.grid(column=1, row=1)
    return voltage_entry_frame

device_entry_toplevel = Toplevel(master=app_common.app, width=200, height=200, bg="gray")
device_entry_toplevel.geometry("+0+0")
device_entry_toplevel.resizable(width=False, height=False)
device_entry_toplevel.protocol("WM_DELETE_WINDOW", quit) # Quit entire program

Vi_min_entry=createVoltageEntry("Vi min", "0")
Vil_max_entry=createVoltageEntry("Vil max", "0.8")

Vih_min_entry=createVoltageEntry("Vih min", "2")
Vi_max_entry=createVoltageEntry("Vi max", "5")


Vo_min_entry=createVoltageEntry("Vo min", "0")
Vol_max_entry=createVoltageEntry("Vol max", "0.4")

Voh_min_entry=createVoltageEntry("Voh min", "2.4")
Vo_max_entry=createVoltageEntry("Vo max", "5")

name_entry= createEntryWrapper("Name")
Vcc_entry=createEntryWrapper("Vcc", "5")
io_button = Button(device_entry_toplevel, fg="blue", text="IO Mode: In/Out", width=20, height=2, command=switchIOModeCallback)
add_button = Button(device_entry_toplevel, fg="blue", text="Add Device", width=20, height=2, command=addEntryCallback)
error_message = Label(device_entry_toplevel, fg="#5c0000", bg="#997474", justify=LEFT, width=70)

name_entry.grid(column=0, row=0, padx=(10,5), pady=(10,0), sticky="w")
Vcc_entry.grid(column=1, row=0, padx=(15,5), pady=(10, 0))
io_button.grid(column=2, row=0, padx=(5,10), pady=(10, 0))
add_button.grid(column=3, row=0, padx=(5,10), pady=(10, 0))

Vi_min_entry.grid(column=0, row=1, padx=(10,5), pady=(10, 0))
Vil_max_entry.grid(column=1, row=1, padx=(5,15), pady=(10, 0))

Vih_min_entry.grid(column=0, row=2, padx=(10,5), pady=(0, 10))
Vi_max_entry.grid(column=1, row=2, padx=(5,15), pady=(0, 10))

Vo_min_entry.grid(column=2, row=1, padx=(15,5), pady=(10, 0))
Vol_max_entry.grid(column=3, row=1, padx=(5,10), pady=(10, 0))

Voh_min_entry.grid(column=2, row=2, padx=(15,5), pady=(0, 10))
Vo_max_entry.grid(column=3, row=2, padx=(5,10), pady=(0, 10))
