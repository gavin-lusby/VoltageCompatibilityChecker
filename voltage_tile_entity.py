from tkinter import *
from constants import *
import app_common


def drawTree(drawing_canvas, device_entry):

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
        drawing_canvas.create_polygon((DRAWING_WIDTH_FULL/2, 2), (DRAWING_WIDTH_FULL/2+4, 2), (DRAWING_WIDTH_FULL/2+4, DRAWING_HEIGHT+2), (DRAWING_WIDTH_FULL/2, DRAWING_HEIGHT+2))
    else:
        drawing_canvas.create_polygon((2, 2), (6, 2), (6, DRAWING_HEIGHT+2), (2, DRAWING_HEIGHT+2))
    v_heights={}

    for voltage_entry in device_entry["values"]:
        # Draw each branch of tree
        pixel_height = int(scale * device_entry["values"][voltage_entry])
        branch_top = DRAWING_HEIGHT-min(pixel_height+1, (DRAWING_HEIGHT-1))+1
        branch_bottom = DRAWING_HEIGHT-max(pixel_height-1, 0)+2
        v_heights[voltage_entry] = (branch_top, branch_bottom)
        print(voltage_entry, ": ", v_heights[voltage_entry]) #TODO remove
        if(((voltage_entry == "Vcc") or voltage_entry[0:2]=="Vo")):
            if(device_entry["io_mode"] == IO_BOTH):
                drawing_canvas.create_polygon((DRAWING_WIDTH_FULL/2+4, branch_top), (DRAWING_WIDTH_FULL+2, branch_top), (DRAWING_WIDTH_FULL+2, branch_bottom), (DRAWING_WIDTH_FULL/2+4, branch_bottom))
            else:
                drawing_canvas.create_polygon((6, branch_top), (DRAWING_WIDTH_FULL/2+4, branch_top), (DRAWING_WIDTH_FULL/2+4, branch_bottom), (6, branch_bottom))
        else: #Vi side
            drawing_canvas.create_polygon((2, branch_top), (DRAWING_WIDTH_FULL/2, branch_top), (DRAWING_WIDTH_FULL/2, branch_bottom), (2, branch_bottom))

    if(device_entry["io_mode"] != IO_OUTPUT_ONLY):
        # Acceptable Voltage In Logic 1
        if(v_heights["Vi max"][1] < v_heights["Vih min"][0]):
            drawing_canvas.create_polygon( \
                (2, v_heights["Vi max"][1]), \
                (DRAWING_WIDTH_FULL/2, v_heights["Vi max"][1]), \
                (DRAWING_WIDTH_FULL/2, v_heights["Vih min"][0]), \
                (2, v_heights["Vih min"][0]), \
                fill="#78B65E")

        #Acceptable Voltage In Logic 0
        if(v_heights["Vil max"][1] < v_heights["Vi min"][0]):
            drawing_canvas.create_polygon( \
                (2, v_heights["Vil max"][1]), \
                (DRAWING_WIDTH_FULL/2, v_heights["Vil max"][1]), \
                (DRAWING_WIDTH_FULL/2, v_heights["Vi min"][0]), \
                (2, v_heights["Vi min"][0]), \
                fill="#965E5E")

    if(device_entry["io_mode"] == IO_BOTH):
        #Output Voltage Range Logic 1
        if(v_heights["Vo max"][1] < v_heights["Voh min"][0]):
            drawing_canvas.create_polygon( \
                (DRAWING_WIDTH_FULL/2+4, v_heights["Vo max"][1]), \
                (DRAWING_WIDTH_FULL+2, v_heights["Vo max"][1]), \
                (DRAWING_WIDTH_FULL+2, v_heights["Voh min"][0]), \
                (DRAWING_WIDTH_FULL/2+4, v_heights["Voh min"][0]), \
                fill="#92E483")

        #Output Voltage Range Logic 0
        if(v_heights["Vol max"][1] < v_heights["Vo min"][0]):
            drawing_canvas.create_polygon( \
                (DRAWING_WIDTH_FULL/2+4, v_heights["Vol max"][1]), \
                (DRAWING_WIDTH_FULL+2, v_heights["Vol max"][1]), \
                (DRAWING_WIDTH_FULL+2, v_heights["Vo min"][0]), \
                (DRAWING_WIDTH_FULL/2+4, v_heights["Vo min"][0]), \
                fill="#F95E5E")
    if(device_entry["io_mode"] == IO_OUTPUT_ONLY):
        #Output Voltage Range Logic 1
        if(v_heights["Vo max"][1] < v_heights["Voh min"][0]):
            drawing_canvas.create_polygon( \
                (6, v_heights["Vo max"][1]), \
                (DRAWING_WIDTH_FULL/2+4, v_heights["Vo max"][1]), \
                (DRAWING_WIDTH_FULL/2+4, v_heights["Voh min"][0]), \
                (6, v_heights["Voh min"][0]), \
                fill="#92E483")

        #Output Voltage Range Logic 0
        if(v_heights["Vol max"][1] < v_heights["Vo min"][0]):
            drawing_canvas.create_polygon( \
                (6, v_heights["Vol max"][1]), \
                (DRAWING_WIDTH_FULL/2+4, v_heights["Vol max"][1]), \
                (DRAWING_WIDTH_FULL/2+4, v_heights["Vo min"][0]), \
                (6, v_heights["Vo min"][0]), \
                fill="#F95E5E")
    # To see if we need to redraw other canvases
    return max_voltage