from tkinter import *
from tkinter import ttk
from constants import *
import app_common
from file_ops import *

tile_frame = Frame(master=app_common.app)
tile_canvas = Canvas(master=tile_frame, width=DRAWING_WIDTH*2.5, height=DRAWING_HEIGHT+8, bg=APP_BG_COLOR)

# -------------------------------
# ---------- CALLBACKS ----------
# -------------------------------

def updateSelector(event=None):
    redrawCanvas(app_common.input_selector.get(), app_common.output_selector.get())

def redrawCanvas(device_input_name, device_output_name):

    if(device_input_name != ""):
        device_entry_input = app_common.device_entries[device_input_name]
    if(device_output_name != ""):
        device_entry_output = app_common.device_entries[device_output_name]

    max_voltage_in = 0
    max_voltage_out = 0

    if(device_input_name != ""):
        if(device_entry_input["io_mode"] == IO_INPUT_ONLY):
            max_voltage_in = device_entry_input["values"]["Vi max"]
        elif(device_entry_input["io_mode"] == IO_OUTPUT_ONLY):
            max_voltage_in = device_entry_input["values"]["Vcc"]
        else:
            max_voltage_in = max(device_entry_input["values"]["Vcc"], device_entry_input["values"]["Vi max"])

    if(device_output_name != ""):
        if(device_entry_output["io_mode"] == IO_INPUT_ONLY):
            max_voltage_out = device_entry_output["values"]["Vi max"]
        elif(device_entry_output["io_mode"] == IO_OUTPUT_ONLY):
            max_voltage_out = device_entry_output["values"]["Vcc"]
        else:
            max_voltage_out = max(device_entry_output["values"]["Vcc"], device_entry_output["values"]["Vi max"])
    
    max_voltage = max(max_voltage_in, max_voltage_out)

    if(device_output_name != ""): # For some reason, you need an X and Y offset of 2 pixels
        v_heights_out = drawTree(device_entry_output, 2, 2+4, max_voltage)
    if(device_input_name != ""):
        v_heights_in = drawTree(device_entry_input, int(DRAWING_WIDTH*1.5+2), 2+4, max_voltage)
        
    if((device_output_name != "") and (device_input_name != "")):
        #Erase canvas center region:
        tile_canvas.create_rectangle( \
        (DRAWING_WIDTH+2, 2), \
        (int(DRAWING_WIDTH*1.5+2), 2 + DRAWING_HEIGHT+8), \
        fill=APP_BG_COLOR, width=0)

        if(device_entry_output["values"]["Vo max"] > device_entry_input["values"]["Vi max"] or \
           device_entry_output["values"]["Voh min"] < device_entry_input["values"]["Vih min"]):
            top_poly_fill = "#F59191"
            top_poly_outline = "#CC0000"
        else:
            top_poly_fill = "#91F591"
            top_poly_outline = "#00CC00"

        if(device_entry_output["values"]["Vol max"] > device_entry_input["values"]["Vil max"] or \
           device_entry_output["values"]["Vo min"] < device_entry_input["values"]["Vi min"]):
            bottom_poly_fill = "#F59191"
            bottom_poly_outline = "#CC0000"
        else:
            bottom_poly_fill = "#91F591"
            bottom_poly_outline = "#00CC00"

        #Draw High input polygon
        tile_canvas.create_polygon( \
        (DRAWING_WIDTH+2, v_heights_out["Vo max"][0]), \
        (int(DRAWING_WIDTH*1.5+2), v_heights_in["Vi max"][0]), \
        (int(DRAWING_WIDTH*1.5+2), v_heights_in["Vih min"][1]), \
        (DRAWING_WIDTH+2, v_heights_out["Voh min"][1]), \
        fill=top_poly_fill, outline=top_poly_outline, width=4)
        
        #Draw Low input polygon
        tile_canvas.create_polygon( \
        (DRAWING_WIDTH+2, v_heights_out["Vo min"][1]), \
        (int(DRAWING_WIDTH*1.5+2), v_heights_in["Vi min"][1]), \
        (int(DRAWING_WIDTH*1.5+2), v_heights_in["Vil max"][0]), \
        (DRAWING_WIDTH+2, v_heights_out["Vol max"][0]), \
        fill=bottom_poly_fill, outline=bottom_poly_outline, width=4)

        



    

def drawTree(device_entry, start_x, start_y, max_voltage):

    v_heights={}

    # How much to scale drawing by based on max_voltage(ie what the top of drawing should be)
    scale = (DRAWING_HEIGHT-1) / max_voltage

    #Erase Canvas region
    tile_canvas.create_rectangle( \
        (start_x, start_y), \
        (start_x + DRAWING_WIDTH, start_y + DRAWING_HEIGHT), \
        fill=APP_BG_COLOR, width=0)
    # Draw tree stem
    tile_canvas.create_rectangle( \
        (start_x + DRAWING_WIDTH/2-2, start_y), \
        (start_x + DRAWING_WIDTH/2+2, start_y + DRAWING_HEIGHT), \
        fill="#000000", width=0) #Color & border width
    
    # Draw greyed out region
    if(device_entry["io_mode"] == IO_INPUT_ONLY):
        tile_canvas.create_rectangle( \
            (start_x + DRAWING_WIDTH/2+2, start_y), \
            (start_x + DRAWING_WIDTH, start_y + DRAWING_HEIGHT), \
            fill="#CCCCCC", width=0)
    elif(device_entry["io_mode"] == IO_OUTPUT_ONLY):
        tile_canvas.create_rectangle( \
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
            tile_canvas.create_rectangle( \
                (start_x + DRAWING_WIDTH/2+2, branch_top), \
                (start_x + DRAWING_WIDTH, branch_bottom), \
                fill="#000000", width=0)
        else:
            #Input side
            tile_canvas.create_rectangle( \
                (start_x, branch_top), \
                (start_x + DRAWING_WIDTH/2 - 2, branch_bottom), \
                fill="#000000", width=0)

    #Draw filled in color sections

    if(device_entry["io_mode"] in [IO_BOTH, IO_INPUT_ONLY]):
        # Acceptable Voltage In Logic 1
        if(v_heights["Vi max"][1] < v_heights["Vih min"][0]):
            tile_canvas.create_rectangle( \
                (start_x, v_heights["Vi max"][1]), \
                (start_x + DRAWING_WIDTH/2 - 2, v_heights["Vih min"][0]), \
                fill="#37AFFF", width=0)

        #Acceptable Voltage In Logic 0
        if(v_heights["Vil max"][1] < v_heights["Vi min"][0]):
            tile_canvas.create_rectangle( \
                (start_x, v_heights["Vil max"][1]), \
                (start_x + DRAWING_WIDTH/2 - 2, v_heights["Vi min"][0]), \
                fill="#3737FF", width=0)

    if(device_entry["io_mode"] in [IO_BOTH, IO_OUTPUT_ONLY]):
        # Output Voltage Range Logic 1
        if(v_heights["Vo max"][1] < v_heights["Voh min"][0]):
            tile_canvas.create_rectangle( \
                (start_x + DRAWING_WIDTH/2+2, v_heights["Vo max"][1]), \
                (start_x + DRAWING_WIDTH, v_heights["Voh min"][0]), \
                fill="#37AFFF", width=0)

        # Output Voltage Range Logic 0
        if(v_heights["Vol max"][1] < v_heights["Vo min"][0]):
            tile_canvas.create_rectangle( \
                (start_x + DRAWING_WIDTH/2+2, v_heights["Vol max"][1]), \
                (start_x + DRAWING_WIDTH, v_heights["Vo min"][0]), \
                fill="#3737FF", width=0)

    # To see if we need to redraw other canvases
    return v_heights

# -------------------------------
# ---------- WRAPPERS -----------
# -------------------------------

def spawnVoltageTile():
    tile_canvas.grid(column=0, row=0, columnspan=2)


    app_common.output_selector = ttk.Combobox(tile_frame, value=[])
    app_common.input_selector = ttk.Combobox(tile_frame, value=[])
    app_common.output_selector.bind("<<ComboboxSelected>>", updateSelector)
    app_common.input_selector.bind("<<ComboboxSelected>>", updateSelector)
    export_button = Button(tile_frame, text="Export", command=exportCallback)
    import_button = Button(tile_frame, text="Import", command=importCallback)

    Label(tile_frame, text="Output Device").grid(column=0,row=1)
    Label(tile_frame, text="Input Device").grid(column=1,row=1)
    app_common.output_selector.grid(column=0,row=2)
    app_common.input_selector.grid(column=1, row=2)
    export_button.grid(column=0,row=3)
    import_button.grid(column=1, row=3)
    tile_frame.pack()
    return tile_frame
