from tkinter import *
from constants import *
import app_common

# -------------------------------
# ---------- CALLBACKS ----------
# -------------------------------

def drawTree(device_entry):

    if(device_entry["io_mode"] == IO_INPUT_ONLY):
        max_voltage = device_entry["values"]["Vi max"]
    elif(device_entry["io_mode"] == IO_OUTPUT_ONLY):
        max_voltage = device_entry["values"]["Vcc"]
    else:
        max_voltage = max(device_entry["values"]["Vcc"], device_entry["values"]["Vi max"])

    # If this voltage > all_max_voltage, use this one, then update all_max_voltage outside func
    if(app_common.all_max_voltage > max_voltage): 
        scale = (DRAWING_HEIGHT-1) / app_common.all_max_voltage
    else:
        scale = (DRAWING_HEIGHT-1) / max_voltage
    
    # Draw tree stem
    if((device_entry["io_mode"] == IO_BOTH) or (device_entry["io_mode"] == IO_INPUT_ONLY)):
        device_entry["canvas"].create_rectangle( \
            (DRAWING_WIDTH_FULL/2, 2), \
            (DRAWING_WIDTH_FULL/2+4, DRAWING_HEIGHT+2), \
            fill="#000000", width=0) #Color & border width
    else:
        device_entry["canvas"].create_rectangle(
            (2, 2), \
            (6, DRAWING_HEIGHT+2), \
            fill="#000000", width=0)
    v_heights={}

    for voltage_entry in device_entry["values"]:
        # Draw each branch of tree
        pixel_height = int(scale * device_entry["values"][voltage_entry])
        branch_top = DRAWING_HEIGHT-min(pixel_height+1, (DRAWING_HEIGHT-1))+1
        branch_bottom = DRAWING_HEIGHT-max(pixel_height-1, 0)+2
        v_heights[voltage_entry] = (branch_top, branch_bottom)
        if(((voltage_entry == "Vcc") or voltage_entry[0:2]=="Vo")):
            if(device_entry["io_mode"] == IO_BOTH):
                device_entry["canvas"].create_rectangle( \
                    (DRAWING_WIDTH_FULL/2+4, branch_top), \
                    (DRAWING_WIDTH_FULL+2, branch_bottom), \
                    fill="#000000", width=0)
            else:
                device_entry["canvas"].create_rectangle( \
                    (6, branch_top), \
                    (DRAWING_WIDTH_FULL/2+4, branch_bottom), \
                    fill="#000000", width=0)
        else: #Vi side
            device_entry["canvas"].create_rectangle( \
                (2, branch_top), \
                (DRAWING_WIDTH_FULL/2, branch_bottom), \
                fill="#000000", width=0)

    if(device_entry["io_mode"] != IO_OUTPUT_ONLY):
        # Acceptable Voltage In Logic 1
        if(v_heights["Vi max"][1] < v_heights["Vih min"][0]):
            device_entry["canvas"].create_rectangle( \
                (2, v_heights["Vi max"][1]), \
                (DRAWING_WIDTH_FULL/2, v_heights["Vih min"][0]), \
                fill="#78B65E", width=0)

        #Acceptable Voltage In Logic 0
        if(v_heights["Vil max"][1] < v_heights["Vi min"][0]):
            device_entry["canvas"].create_rectangle( \
                (2, v_heights["Vil max"][1]), \
                (DRAWING_WIDTH_FULL/2, v_heights["Vi min"][0]), \
                fill="#965E5E", width=0)

    if(device_entry["io_mode"] == IO_BOTH):
        #Output Voltage Range Logic 1
        if(v_heights["Vo max"][1] < v_heights["Voh min"][0]):
            device_entry["canvas"].create_rectangle( \
                (DRAWING_WIDTH_FULL/2+4, v_heights["Vo max"][1]), \
                (DRAWING_WIDTH_FULL+2, v_heights["Voh min"][0]), \
                fill="#92E483", width=0)

        #Output Voltage Range Logic 0
        if(v_heights["Vol max"][1] < v_heights["Vo min"][0]):
            device_entry["canvas"].create_rectangle( \
                (DRAWING_WIDTH_FULL/2+4, v_heights["Vol max"][1]), \
                (DRAWING_WIDTH_FULL+2, v_heights["Vo min"][0]), \
                fill="#F95E5E", width=0)
    if(device_entry["io_mode"] == IO_OUTPUT_ONLY):
        #Output Voltage Range Logic 1
        if(v_heights["Vo max"][1] < v_heights["Voh min"][0]):
            device_entry["canvas"].create_rectangle( \
                (6, v_heights["Vo max"][1]), \
                (DRAWING_WIDTH_FULL/2+4, v_heights["Voh min"][0]), \
                fill="#92E483", width=0)

        #Output Voltage Range Logic 0
        if(v_heights["Vol max"][1] < v_heights["Vo min"][0]):
            device_entry["canvas"].create_rectangle( \
                (6, v_heights["Vol max"][1]), \
                (DRAWING_WIDTH_FULL/2+4, v_heights["Vo min"][0]), \
                fill="#F95E5E", width=0)
    # To see if we need to redraw other canvases
    return max_voltage

# -------------------------------
# ---------- WRAPPERS -----------
# -------------------------------

# def createVoltageTile():
#     entry_stringvar = StringVar()
#     entry_frame = Frame(master=device_entry_toplevel, bg="gray")
#     entry_field = Entry(entry_frame, fg="gray", textvariable=entry_stringvar)
#     entry_label = Label(entry_frame, text=display_name, bg="gray")
#     entry_dict[display_name] = entry_stringvar
    
#     entry_label.grid(column=0, columnspan=2, row=0, sticky="we")
#     entry_field.grid(column=0, row=1, sticky="we")
#     entry_stringvar.set(default_text)
#     entry_group[display_name] = entry_field
#     return entry_frame
