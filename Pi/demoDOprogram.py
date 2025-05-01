import serial 
import tkinter as tk

from gpiozero import LED
from time import sleep

led = LED(17)

# main = tk.Tk()
# main.config(bg="#E4E2E2")
# main.title("Main Window")
# main.geometry("301x132")

# label = tk.Label(master=main, text="Saturation Target")
# label.config(bg="#E4E2E2", fg="#000")
# label.grid(row=0, column=0)

# scale_var = tk.DoubleVar(value=0)
# scale = tk.Scale(master=main, variable=scale_var)
# scale.config(bg="#fff", fg="#000", from_=0, to=100, resolution=1)
# scale.grid(row=1, column=0)

# label1 = tk.Label(master=main, text="Tolerance %")
# label1.config(bg="#E4E2E2", fg="#000")
# label1.grid(row=0, column=1)

# entry = tk.Entry(master=main, text="placeholder text")
# entry.config(bg="#fff", fg="#000")
# entry.grid(row=1, column=1)

if __name__ == '__main__':
    # Arduino device 1
    dev0 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    dev0.reset_input_buffer()

    # Arduino device 2
    dev1 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    dev1.reset_input_buffer()

    # Arduino device 3
    dev2 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    dev2.reset_input_buffer()

    # Arduino device 4
    dev3 = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    dev3.reset_input_buffer()

    # main.mainloop()

    # Dummy send vars
    dev0Motor1Enabled = False
    dev0Motor1Enabled = False

    dev0Motor1Enabled = False
    dev0Motor1Enabled = False
    target = 55
    tol = 5
    line = "0.0"

    while True:
        if (dev0.in_waiting > 0):
            line = dev0.readline().decode('utf-8').rstrip()
            print(line)

        val = float(line)

        # if (val < (scale_var.get() - float(entry.get()))):
        if (val < (target - tol)):
            led.on()
        # elif (val > (scale_var.get() + float(entry.get()))):
        elif (val > (target + tol)):
            led.blink()
        else:
            led.off()
        