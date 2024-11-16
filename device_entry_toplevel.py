from tkinter import *
from constants import *
import app_common
from voltage_tile_entity import validateDeviceEntryValues, initializeValidatedDevice

io_mode_selection = IO_BOTH
entry_group = {} # Give this a better name TODO

error_message = None # Label for error message
io_button = None # Button to change IO mode


# -------------------------------
# ---------- CALLBACKS ----------
# -------------------------------

def addEntryCallback():
    failed = False
    error_string = None
    new_entry = {}
    error_string = fetchNewDeviceEntry(new_entry)
    if(error_string == None):
        error_string = validateDeviceEntryValues(new_entry)
    
    if(error_string != None):
        error_message.configure(text=f"Error: {error_string}")
        error_message.grid(column=0, columnspan=4, row=3, padx=10)
        return
    
    error_message.grid_forget()
    initializeValidatedDevice(new_entry)


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

def createEntryWrapper(wrapper_master, display_name, default_text=""):
    entry_frame = Frame(master=wrapper_master, bg="gray")
    entry_field = Entry(entry_frame, fg="gray")
    entry_label = Label(entry_frame, text=display_name, bg="gray")
    
    # Grid place elements
    entry_label.grid(column=0, columnspan=2, row=0, sticky="we")
    entry_field.grid(column=0, row=1, sticky="we")

    #Initialize default texts in new entries
    entry_field.delete(0, END)
    entry_field.insert(0, default_text)

    # Add entry fields to entry_group
    entry_group[display_name] = entry_field
    return entry_frame

def createVoltageEntry(wrapper_master, display_name, default_relative_v="0", default_abs_v="0"):
    voltage_entry_frame = Frame(master=wrapper_master, bg=VOLATE_ENTRY_BG_COLOR, pady=5, padx=5)
    entry_field_rel = Entry(voltage_entry_frame, fg="gray", width=5)
    entry_field_abs = Entry(voltage_entry_frame, fg="gray", width=5)

    vcc_label = Label(voltage_entry_frame, text="×Vcc +", bg=VOLATE_ENTRY_BG_COLOR)
    v_label = Label(voltage_entry_frame, text="V", bg=VOLATE_ENTRY_BG_COLOR)
    entry_label = Label(voltage_entry_frame, text=display_name, bg=VOLATE_ENTRY_BG_COLOR)

    # Grid place elements
    entry_label.grid(column=0, columnspan=4, row=0, sticky="we")
    entry_field_rel.grid(column=0, row=1, sticky="we")
    vcc_label.grid(column=1, row=1)
    entry_field_abs.grid(column=2, row=1)
    v_label.grid(column=3, row=1)

    # Initialize default text in new entries
    entry_field_rel.delete(0, END)
    entry_field_abs.delete(0, END)
    entry_field_rel.insert(0, default_relative_v)
    entry_field_abs.insert(0, default_abs_v)

    # Add entry fields to entry_group
    entry_group[display_name] = (entry_field_rel, entry_field_abs)
    return voltage_entry_frame

# -------------------------------
# ------------ OTHER ------------ Rename this??
# -------------------------------

def spawnDeviceEntryTopLevel():
    global error_message
    global io_button

    device_entry_toplevel = Toplevel(master=app_common.app, width=200, height=200, bg="gray")
    device_entry_toplevel.geometry("+0+0")
    device_entry_toplevel.resizable(width=False, height=False)
    device_entry_toplevel.protocol("WM_DELETE_WINDOW", quit) # Quit entire program

    Vi_min_entry=createVoltageEntry(device_entry_toplevel, "Vi min", "0", "0")
    Vil_max_entry=createVoltageEntry(device_entry_toplevel, "Vil max", "0", "0.8")

    Vih_min_entry=createVoltageEntry(device_entry_toplevel, "Vih min", "0", "2")
    Vi_max_entry=createVoltageEntry(device_entry_toplevel, "Vi max", "0", "5")


    Vo_min_entry=createVoltageEntry(device_entry_toplevel, "Vo min", "0", "0")
    Vol_max_entry=createVoltageEntry(device_entry_toplevel, "Vol max", "0", "0.4")

    Voh_min_entry=createVoltageEntry(device_entry_toplevel, "Voh min", "0", "2.4")
    Vo_max_entry=createVoltageEntry(device_entry_toplevel, "Vo max", "0", "5")

    name_entry= createEntryWrapper(device_entry_toplevel, "Name", "Default Device")
    Vcc_entry=createEntryWrapper(device_entry_toplevel, "Vcc", "5")

    io_button = Button(device_entry_toplevel, fg="blue", text="IO Mode: In/Out", width=20, height=2, command=switchIOModeCallback)
    add_button = Button(device_entry_toplevel, fg="blue", text="Add Device", width=20, height=2, command=addEntryCallback)
    error_message = Label(device_entry_toplevel, fg="#5c0000", bg="#997474", justify=LEFT, width=70)

    name_entry.grid(column=0, row=0, padx=(10,5), pady=(10,0), sticky="w")
    Vcc_entry.grid(column=1, row=0, padx=(15,5), pady=(10, 0))
    io_button.grid(column=2, row=0, padx=(5,10), pady=(10, 0))
    add_button.grid(column=3, row=0, padx=(5,10), pady=(10, 0))



    Vi_min_entry.grid(column=0, row=1, padx=(10,5), pady=10)
    Vil_max_entry.grid(column=1, row=1, padx=(5,15), pady=10)

    Vih_min_entry.grid(column=0, row=2, padx=(10,5), pady=10)
    Vi_max_entry.grid(column=1, row=2, padx=(5,15), pady=10)



    Vo_min_entry.grid(column=2, row=1, padx=(15,5), pady=10)
    Vol_max_entry.grid(column=3, row=1, padx=(5,10), pady=10)

    Voh_min_entry.grid(column=2, row=2, padx=(15,5), pady=10)
    Vo_max_entry.grid(column=3, row=2, padx=(5,10), pady=10)



# TODO Write better docstring: This fetches the data from the entries and creates an entry item out of it(returns error, takes entry by reference)
def fetchNewDeviceEntry(new_entry):

    new_entry_name = entry_group["Name"].get()

    if(new_entry_name == ""):
        return "Device name not provided"
    elif(new_entry_name in app_common.device_entries):
        return "A device with this name already exists"
    
    new_entry["name"] = new_entry_name
    new_entry["values"] = {}
    new_entry["io_mode"] = io_mode_selection
    new_entry["values"]["Vcc"] = entry_group["Vcc"].get()
        
    try:
        new_entry["values"]["Vcc"] = float(entry_group["Vcc"].get())
        for entry_label in entry_group:
            if entry_label in ["Name", "Vcc"]:
                continue
            # Ignore inputs in output mode and outputs in input mode
            if(((new_entry["io_mode"] == IO_OUTPUT_ONLY) and (entry_label in ["Vi min", "Vil max", "Vih min", "Vi max"])) or
            ((new_entry["io_mode"] == IO_INPUT_ONLY) and (entry_label in ["Vo min", "Vol max", "Voh min", "Vo max"]))):
                continue
            # Voltage = A*Vcc + B
            new_entry["values"][entry_label] = (new_entry["values"]["Vcc"]*float(entry_group[entry_label][0].get())) + \
                                                float(entry_group[entry_label][1].get())

            
    except ValueError:
        return "All number fields must contain valid numbers"

