from tkinter import *
from constants import *
import app_common
from voltage_tile_entity import initializeValidatedDevice

ABSOLUTE_SCALE = 0
VCC_RELATIVE_SCALE = 1
scale_modes = {}#todo remove
entry_dict = {}
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
    entry_stringvar = StringVar()
    entry_frame = Frame(master=wrapper_master, bg="gray")
    entry_field = Entry(entry_frame, fg="gray", textvariable=entry_stringvar)
    entry_label = Label(entry_frame, text=display_name, bg="gray")
    entry_dict[display_name] = entry_stringvar
    
    entry_label.grid(column=0, columnspan=2, row=0, sticky="we")
    entry_field.grid(column=0, row=1, sticky="we")
    entry_stringvar.set(default_text)
    entry_group[display_name] = entry_field
    return entry_frame

def createVoltageEntry(wrapper_master, display_name, default_relative_v="0", default_abs_v="0"):
    relative_v_stringvar = StringVar() #TODO: see if u can combine entry_dict and entry_group by getting rid of stringvars(entry_dict) and accessing entryfields directly
    absolute_v_stringvar = StringVar()
    voltage_entry_frame = Frame(master=wrapper_master, bg=VOLATE_ENTRY_BG_COLOR, pady=5, padx=5)
    entry_field_rel = Entry(voltage_entry_frame, fg="gray", textvariable=relative_v_stringvar, width=5)
    entry_field_abs = Entry(voltage_entry_frame, fg="gray", textvariable=absolute_v_stringvar, width=5)

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



# Write better docstring: This fetches the data from the entries and creates an entry item out of it(returns error, takes entry by reference)
def fetchNewDeviceEntry(new_entry): #TODO when called pass in {}

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

# TODO write docstring for this
def validateDeviceEntryValues(device_entry):
    if(device_entry["io_mode"] != IO_OUTPUT_ONLY): # in-out / in only
        if((device_entry["values"]["Vi min"] > device_entry["values"]["Vil max"])): #Vi min > Vil max
            return "Vi min must be <= Vil max(Vi min=" + \
                str(device_entry["values"]["Vi min"]) + ", Vil max=" + str(device_entry["values"]["Vil max"]) + ")"
        
        elif((device_entry["values"]["Vil max"] >= device_entry["values"]["Vih min"])): #Vil max >= Vih min
            return "Vil max must be < Vih min(Vil max=" + \
                str(device_entry["values"]["Vil max"]) + ", Vih min=" + str(device_entry["values"]["Vih min"]) + ")"
        
        elif((device_entry["values"]["Vih min"] > device_entry["values"]["Vi max"])): #Vih min > Vi max
            return "Vih min must be <= Vi max(Vih min=" + \
                str(device_entry["values"]["Vih min"]) + ", Vi max=" + str(device_entry["values"]["Vi max"]) + ")"

    if(device_entry["io_mode"] != IO_INPUT_ONLY): # in-out / out only
        if((device_entry["values"]["Vo min"] > device_entry["values"]["Vol max"])): #Vo min > Vol max
            return "Vo min must be <= Vol max(Vo min=" + \
                str(device_entry["values"]["Vo min"]) + ", Vol max=" + str(device_entry["values"]["Vol max"]) + ")"
        
        elif((device_entry["values"]["Vol max"] >= device_entry["values"]["Voh min"])): #Vol max >= Voh min
            return "Vol max must be < Voh min(Vol max=" + \
                str(device_entry["values"]["Vol max"]) + ", Voh min=" + str(device_entry["values"]["Voh min"]) + ")"
        
        elif((device_entry["values"]["Voh min"] > device_entry["values"]["Vo max"])): #Voh min > Vo max
            return "Voh min must be <= Vo max(Voh min=" + \
                str(device_entry["values"]["Voh min"]) + ", Vo max=" + str(device_entry["values"]["Vo max"]) + ")"
        
        elif((device_entry["values"]["Vo max"] > device_entry["values"]["Vcc"])): #Vo max > Vcc
            return "Vo max must be <= Vcc(Vo max=" + \
                str(device_entry["values"]["Vo max"]) + ", Vcc=" + str(device_entry["values"]["Vcc"]) + ")"