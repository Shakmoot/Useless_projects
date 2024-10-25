import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk

def exit_fullscreen(event=None):
    root.destroy()

def start_menu(event=None):
    menu = tk.Menu(root, tearoff=0, bg='#c0c0c0', font=("Tahoma", 10))
    menu.add_command(label="Mind reader", command=open_notepad)
    menu.add_command(label="Calculator", command=open_calculator)
    menu.add_separator()
    menu.add_command(label="Exit", command=root.quit)
    menu.tk_popup(10, root.winfo_height() - 100)

def open_notepad():
    notepad = tk.Toplevel(root)
    notepad.title("Mindreader")
    notepad.geometry("400x300")

    text_area = scrolledtext.ScrolledText(notepad, wrap='word', font=("Consolas", 10))
    text_area.pack(expand=True, fill='both')

def open_calculator():
    calculator = tk.Toplevel(root)
    calculator.title("Calculator - Windows XP")
    calculator.geometry("250x300")

    expression = tk.StringVar()
    entry = tk.Entry(calculator, textvariable=expression, font=("Consolas", 15), justify='right')
    entry.grid(row=0, column=0, columnspan=4, sticky='nsew')

    buttons = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
        ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
    ]

    for (text, row, col) in buttons:
        btn = tk.Button(calculator, text=text, font=("Consolas", 12), 
                        width=5, height=2,  # Change button size here
                        command=lambda t=text: on_calc_button_click(t, expression))
        btn.grid(row=row, column=col, sticky='nsew')

    for i in range(5):
        calculator.grid_rowconfigure(i, weight=1)
        calculator.grid_columnconfigure(i % 4, weight=1)

def on_calc_button_click(char, expression):
    if char == '=':
        try:
            expression.set(str(eval(expression.get())))
        except Exception:
            expression.set("Error")
    else:
        expression.set(expression.get() + char)

def create_taskbar():
    taskbar = tk.Frame(root, bg='#004080', height=40)
    taskbar.pack(side='bottom', fill='x')

    start_button = tk.Button(taskbar, text="Start", font=("Tahoma", 10),
                             bg='#c0c0c0', relief='raised',
                             width=8, height=2,  # Adjust the size here
                             command=start_menu)
    start_button.pack(side='left', padx=5, pady=5)

def create_desktop_icons():
    apps = [("Mind reader", open_notepad), ("Calculator", open_calculator)]

    for i, (name, command) in enumerate(apps):
        icon_button = tk.Button(root, text=name, font=("Tahoma", 10),
                                bg='#e0e0e0', relief='flat',
                                width=10, height=3,  # Adjust icon button size here
                                command=command)
        icon_button.place(x=50, y=50 + i * 100)

def set_background_image():
    bg_image = Image.open("background.png")
    bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

root = tk.Tk()
root.title("Windows XP Emulator")

root.attributes('-fullscreen', True)
root.bind("<Escape>", exit_fullscreen)

set_background_image()
create_taskbar()
create_desktop_icons()

root.mainloop()
#srhjrtjdrjr
