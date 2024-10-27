from tkinter import *
from constants import *
import app_common

# -------------------------------
# ---------- CALLBACKS ----------
# -------------------------------

def drawTree(device_entry, start_x, start_y):

    v_heights={}

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
    device_entry["canvas"].create_rectangle( \
        (start_x + DRAWING_WIDTH/2-2, start_y), \
        (start_x + DRAWING_WIDTH/2+2, start_y + DRAWING_HEIGHT), \
        fill="#000000", width=0) #Color & border width
    
    # Draw greyed out region
    if(device_entry["io_mode"] == IO_INPUT_ONLY):
        device_entry["canvas"].create_rectangle( \
            (start_x + DRAWING_WIDTH/2+2, start_y), \
            (start_x + DRAWING_WIDTH, start_y + DRAWING_HEIGHT), \
            fill="#CCCCCC", width=0)
    elif(device_entry["io_mode"] == IO_OUTPUT_ONLY):
        device_entry["canvas"].create_rectangle( \
            (start_x, start_y), \
            (start_x + DRAWING_WIDTH/2-2, start_y + DRAWING_HEIGHT), \
            fill="#CCCCCC", width=0)
        

    for voltage_entry in device_entry["values"]:
        # Draw each branch of tree
        pixel_height = int(scale * device_entry["values"][voltage_entry])
        
        max_y = DRAWING_HEIGHT - 1
        branch_top = start_y + max_y-min(pixel_height+1, max_y)
        # +1 for bottom because the shape goes upto but not including the bottom edge
        branch_bottom = start_y + max_y-max(pixel_height-1, 0) + 1

        #Draw tree branches
        v_heights[voltage_entry] = (branch_top, branch_bottom)
        if(((voltage_entry == "Vcc") or voltage_entry[0:2]=="Vo")):
            #Output side
            device_entry["canvas"].create_rectangle( \
                (start_x + DRAWING_WIDTH/2+2, branch_top), \
                (start_x + DRAWING_WIDTH, branch_bottom), \
                fill="#000000", width=0)
        else:
            #Input side
            device_entry["canvas"].create_rectangle( \
                (start_x, branch_top), \
                (start_x + DRAWING_WIDTH/2 - 2, branch_bottom), \
                fill="#000000", width=0)

    #Draw filled in color sections

    if(device_entry["io_mode"] in [IO_BOTH, IO_INPUT_ONLY]):
        # Acceptable Voltage In Logic 1
        if(v_heights["Vi max"][1] < v_heights["Vih min"][0]):
            device_entry["canvas"].create_rectangle( \
                (start_x, v_heights["Vi max"][1]), \
                (start_x + DRAWING_WIDTH/2 - 2, v_heights["Vih min"][0]), \
                fill="#37AFFF", width=0)

        #Acceptable Voltage In Logic 0
        if(v_heights["Vil max"][1] < v_heights["Vi min"][0]):
            device_entry["canvas"].create_rectangle( \
                (start_x, v_heights["Vil max"][1]), \
                (start_x + DRAWING_WIDTH/2 - 2, v_heights["Vi min"][0]), \
                fill="#3737FF", width=0)

    if(device_entry["io_mode"] in [IO_BOTH, IO_OUTPUT_ONLY]):
        # Output Voltage Range Logic 1
        if(v_heights["Vo max"][1] < v_heights["Voh min"][0]):
            device_entry["canvas"].create_rectangle( \
                (start_x + DRAWING_WIDTH/2+2, v_heights["Vo max"][1]), \
                (start_x + DRAWING_WIDTH, v_heights["Voh min"][0]), \
                fill="#37AFFF", width=0)

        # Output Voltage Range Logic 0
        if(v_heights["Vol max"][1] < v_heights["Vo min"][0]):
            device_entry["canvas"].create_rectangle( \
                (start_x + DRAWING_WIDTH/2+2, v_heights["Vol max"][1]), \
                (start_x + DRAWING_WIDTH, v_heights["Vo min"][0]), \
                fill="#3737FF", width=0)

    # To see if we need to redraw other canvases
    return max_voltage

# -------------------------------
# ---------- WRAPPERS -----------
# -------------------------------

# def createVoltageTile():
#     tile_frame = Frame(master=app_common.app)
#     tile_label = Label(entry_frame)
#     entry_stringvar = StringVar()
#     entry_frame = Frame(master=device_entry_toplevel, bg="gray")
#     entry_field = Entry(entry_frame, fg="gray", textvariable=entry_stringvar)
#     entry_label = Label(entry_frame, text=display_name, bg="gray")
#     entry_dict[display_name] = entry_stringvar
    
#     entry_label.grid(column=0, columnspan=2, row=0, sticky="we")
#     entry_field.grid(column=0, row=1, sticky="we")
#     entry_stringvar.set(default_text)
#     entry_group[display_name] = entry_field
#     return tile_frame
