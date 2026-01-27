from tkinter import *
from tkinter.ttk import *


def fah_to_cel():
    """Convert Fahrenheit to Celsius"""
    fah_value = fah_temp.get().strip()
    try:
        if fah_value:
            celsius = (5 / 9) * (float(fah_value) - 32)
            cel_temp.delete(0, END)
            cel_temp.insert(0, str(round(celsius, 2)))
    except ValueError:
        cel_temp.delete(0, END)
        cel_temp.insert(0, "Error")


def cel_to_fah():
    """Convert Celsius to Fahrenheit"""
    cel_value = cel_temp.get().strip()
    try:
        if cel_value:
            fahrenheit = (float(cel_value) * 9/5) + 32
            fah_temp.delete(0, END)
            fah_temp.insert(0, str(round(fahrenheit, 2)))
    except ValueError:
        fah_temp.delete(0, END)
        fah_temp.insert(0, "Error")


def create_temp_entry(parent, label_text, column):
    """Create a temp entry frame with label"""
    frame = Frame(master=parent)
    entry = Entry(master=frame, width=10)
    label = Label(master=frame, text=label_text)

    entry.grid(row=0, column=0, sticky="e")
    label.grid(row=0, column=1, sticky="w")
    frame.grid(row=0, column=column, padx=10)

    return entry



window = Tk()
window.title("Temperature Converter")
window.resizable(width=False, height=False)

# Create temp entries
fah_temp = create_temp_entry(window, "\N{DEGREE FAHRENHEIT}", 0)
cel_temp = create_temp_entry(window, "\N{DEGREE CELSIUS}", 2)

# Create button frame for arrows
btn_frame = Frame(master=window)
btn_frame.grid(row=0, column=1, pady=10)

# Right arrow: F > C
btn_right = Button(
    master=btn_frame,
    text="→",
    command=fah_to_cel,
    width=3
)
btn_right.grid(row=0, column=0, padx=2)

# Left arrow: C > F
btn_left = Button(
    master=btn_frame,
    text="←",
    command=cel_to_fah,
    width=3
)
btn_left.grid(row=0, column=1, padx=2)


window.mainloop()
