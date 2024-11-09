from tkinter import filedialog
from constants import *
import app_common
import csv

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
    savename = filedialog.askopenfilename(initialfile = "devices.csv")
    with open(savename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        print(reader)
        for row in reader:
            print(row)
            device_entry = {}
            device_entry["io_mode"] = int(row[1])
            device_entry["values"] = {}
            device_entry["values"]["Vcc"] = float(row[2]) #todo safeguard this
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

            app_common.device_entries[row[0]] = device_entry

    print(app_common.device_entries, savename)