from tkinter import *
from app_common import *
 
DRAWING_WIDTH=200
DRAWING_HEIGHT=401


canvas_test = Canvas(app, width=DRAWING_WIDTH, height=DRAWING_HEIGHT)

canvas_test.place(x=10,y=10)
sttingy = input()
scale = (DRAWING_HEIGHT-1) / max(device_entries[0]["Vcc"], device_entries[0]["Vi max"])
canvas_test.create_polygon((DRAWING_WIDTH/2, 2), (DRAWING_WIDTH/2+4, 2), (DRAWING_WIDTH/2+4, DRAWING_HEIGHT+2), (DRAWING_WIDTH/2, DRAWING_HEIGHT+2))
v_heights={}
for voltage_level in device_entries[0]:
    if voltage_level == "Name":
        continue
    else:
        
        pixel_height = int(scale * device_entries[0][voltage_level])
        branch_top = DRAWING_HEIGHT-min(pixel_height+1, (DRAWING_HEIGHT-1))+1
        branch_bottom = DRAWING_HEIGHT-max(pixel_height-1, 0)+2
        v_heights[voltage_level] = (branch_top, branch_bottom)
        print(voltage_level, ": ", pixel_height, "\t", branch_top, "\t", branch_bottom)
        if((voltage_level == "Vcc") or voltage_level[0:2]=="Vo"):
            canvas_test.create_polygon((DRAWING_WIDTH/2+4, branch_top), (DRAWING_WIDTH+2, branch_top), (DRAWING_WIDTH+2, branch_bottom), (DRAWING_WIDTH/2+4, branch_bottom))
        else: #Vi side
            canvas_test.create_polygon((2, branch_top), (DRAWING_WIDTH/2, branch_top), (DRAWING_WIDTH/2, branch_bottom), (2, branch_bottom))


# Acceptable Voltage In Logic 1
if(v_heights["Vi max"][1] < v_heights["Vih min"][0]-1):
    canvas_test.create_polygon( \
        (2, v_heights["Vi max"][1]), \
        (DRAWING_WIDTH/2, v_heights["Vi max"][1]), \
        (DRAWING_WIDTH/2, v_heights["Vih min"][0]), \
        (2, v_heights["Vih min"][0]), \
        fill="#78B65E")

#Acceptable Voltage In Logic 0
if(v_heights["Vil max"][1] < v_heights["Vi min"][0]-1):
    canvas_test.create_polygon( \
        (2, v_heights["Vil max"][1]), \
        (DRAWING_WIDTH/2, v_heights["Vil max"][1]), \
        (DRAWING_WIDTH/2, v_heights["Vi min"][0]), \
        (2, v_heights["Vi min"][0]), \
        fill="#965E5E")

#Output Voltage Range Logic 1
if(v_heights["Vo max"][1] < v_heights["Voh min"][0]-1):
    canvas_test.create_polygon( \
        (DRAWING_WIDTH/2+4, v_heights["Vo max"][1]), \
        (DRAWING_WIDTH+2, v_heights["Vo max"][1]), \
        (DRAWING_WIDTH+2, v_heights["Voh min"][0]), \
        (DRAWING_WIDTH/2+4, v_heights["Voh min"][0]), \
        fill="#92E483")

#Output Voltage Range Logic 0
if(v_heights["Vol max"][1] < v_heights["Vo min"][0]-1):
    canvas_test.create_polygon( \
        (DRAWING_WIDTH/2+4, v_heights["Vol max"][1]), \
        (DRAWING_WIDTH+2, v_heights["Vol max"][1]), \
        (DRAWING_WIDTH+2, v_heights["Vo min"][0]), \
        (DRAWING_WIDTH/2+4, v_heights["Vo min"][0]), \
        fill="#F95E5E")