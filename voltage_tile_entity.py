from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from constants import *
import app_common
import csv

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
        (2+ DRAWING_WIDTH, 2), \
        (2+ int(DRAWING_WIDTH*1.5), 2 + DRAWING_HEIGHT+8), \
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
        (2 + DRAWING_WIDTH, v_heights_out["Vo min"][1]), \
        (2 + int(DRAWING_WIDTH*1.5), v_heights_in["Vi min"][1]), \
        (2 + int(DRAWING_WIDTH*1.5), v_heights_in["Vil max"][0]), \
        (2 + DRAWING_WIDTH, v_heights_out["Vol max"][0]), \
        fill=bottom_poly_fill, outline=bottom_poly_outline, width=4)


def exportCallback():
    savename = filedialog.asksaveasfilename(initialfile = "devices.csv")
    with open(savename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for device, device_data in app_common.device_entries.items():
            writearray = [device, device_data["io_mode"], device_data["values"]["Vcc"]]
            if (device_data["io_mode"] in [IO_BOTH, IO_INPUT_ONLY]):
                writearray.extend([device_data["values"]["Vi min"], device_data["values"]["Vil max"], \
                                  device_data["values"]["Vih min"], device_data["values"]["Vi max"]])
            if (device_data["io_mode"] in [IO_BOTH, IO_OUTPUT_ONLY]):
                writearray.extend([device_data["values"]["Vo min"], device_data["values"]["Vol max"], \
                                  device_data["values"]["Voh min"], device_data["values"]["Vo max"]])

            writer.writerow(writearray)
    print(app_common.device_entries, savename)

def importCallback():
    error_list = []
    savename = filedialog.askopenfilename(initialfile = "devices.csv")
    with open(savename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            device_entry = {}
            device_entry["name"] = row[0]
            device_name = row[0]
            device_entry["name"] = device_name
            if(device_name in app_common.device_entries):
                error_list.append(f"Error for device \"{device_name}\":\n A device with this name already exists\n This device will not be imported.\n")
                continue
            device_entry["io_mode"] = int(row[1])
            device_entry["values"] = {}
            try:
                device_entry["values"]["Vcc"] = float(row[2])
                if (device_entry["io_mode"] in [IO_BOTH, IO_INPUT_ONLY]):
                    device_entry["values"]["Vi min"] = float(row[3])
                    device_entry["values"]["Vil max"] = float(row[4])
                    device_entry["values"]["Vih min"] = float(row[5])
                    device_entry["values"]["Vi max"] = float(row[6])
                elif (device_entry["io_mode"] == IO_OUTPUT_ONLY):
                    device_entry["values"]["Vo min"] = float(row[3])
                    device_entry["values"]["Vol max"] = float(row[4])
                    device_entry["values"]["Voh min"] = float(row[5])
                    device_entry["values"]["Vo max"] = float(row[6])
                
                if (device_entry["io_mode"] == IO_BOTH):
                    device_entry["values"]["Vo min"] = float(row[7])
                    device_entry["values"]["Vol max"] = float(row[8])
                    device_entry["values"]["Voh min"] = float(row[9])
                    device_entry["values"]["Vo max"] = float(row[10])
            except ValueError:
                error_list.append((f"Error for device \"{device_name}\":\n All number fields must contain valid numbers\n"
                                  "This device will not be imported.\n"))
                continue
            error_msg = validateDeviceEntryValues(device_entry)
            if(error_msg != None):
                error_list.append(f"Error for device \"{device_name}\":\n {error_msg}\n This device will not be imported.\n")
                continue
            initializeValidatedDevice(device_entry)
    if(len(error_list) > 0):
        messagebox.showinfo(title="Import Errors", message="\n\n".join(error_list))


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


# -------------------------------
# ----------- OTHERS ------------
# -------------------------------

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
                fill=VOLTAGE_1_COLOR, width=0)

        #Acceptable Voltage In Logic 0
        if(v_heights["Vil max"][1] < v_heights["Vi min"][0]):
            tile_canvas.create_rectangle( \
                (start_x, v_heights["Vil max"][1]), \
                (start_x + DRAWING_WIDTH/2 - 2, v_heights["Vi min"][0]), \
                fill=VOLTAGE_0_COLOR, width=0)

    if(device_entry["io_mode"] in [IO_BOTH, IO_OUTPUT_ONLY]):
        # Output Voltage Range Logic 1
        if(v_heights["Vo max"][1] < v_heights["Voh min"][0]):
            tile_canvas.create_rectangle( \
                (start_x + DRAWING_WIDTH/2+2, v_heights["Vo max"][1]), \
                (start_x + DRAWING_WIDTH, v_heights["Voh min"][0]), \
                fill=VOLTAGE_1_COLOR, width=0)

        # Output Voltage Range Logic 0
        if(v_heights["Vol max"][1] < v_heights["Vo min"][0]):
            tile_canvas.create_rectangle( \
                (start_x + DRAWING_WIDTH/2+2, v_heights["Vol max"][1]), \
                (start_x + DRAWING_WIDTH, v_heights["Vo min"][0]), \
                fill=VOLTAGE_0_COLOR, width=0)

    # To see if we need to redraw other canvases
    return v_heights


#TODO write docstring for this
def initializeValidatedDevice(device_entry):
    device_name = device_entry["name"]
    app_common.device_entries[device_name] = device_entry
    if(device_entry["io_mode"] in [IO_BOTH, IO_INPUT_ONLY]):
        app_common.input_device_options.append(device_name)
        app_common.input_selector.configure(value=app_common.input_device_options)
        if(app_common.input_selector.get() == ""):
            app_common.input_selector.set(device_name)
            redrawCanvas(device_name, app_common.output_selector.get())

    if(device_entry["io_mode"] in [IO_BOTH, IO_OUTPUT_ONLY]):
        app_common.output_device_options.append(device_name)
        app_common.output_selector.configure(value=app_common.output_device_options)
        if(app_common.output_selector.get() == ""):
            app_common.output_selector.set(device_name)
            redrawCanvas(app_common.input_selector.get(), device_name)

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