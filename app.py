import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

confirmation_count = 0

def reset_confirmation_count():
    global confirmation_count
    confirmation_count = 0

def create_exit_confirmation(app_window):
    global confirmation_count
    confirmation_count += 1

    confirm_window = tk.Toplevel(app_window)
    confirm_window.title("Exit Confirmation")
    confirm_window.geometry(f"{300 + confirmation_count * 10}x{150 + confirmation_count * 5}")
    confirm_window.grab_set()

    label = tk.Label(confirm_window, text="Are you sure you want to exit?", font=("Tahoma", 12))
    label.pack(pady=10)

    yes_button = tk.Button(confirm_window, text="Yes", width=max(10 - confirmation_count, 2), height=2,
                           command=lambda: handle_exit_confirmation(confirm_window, app_window))
    yes_button.pack(side='left', padx=20, pady=10)

    no_button = tk.Button(confirm_window, text="No", width=12, height=2,
                          command=lambda: cancel_exit(confirm_window, app_window))
    no_button.pack(side='right', padx=20, pady=10)

def handle_exit_confirmation(confirm_window, app_window):
    confirm_window.destroy()
    if confirmation_count < 7:
        create_exit_confirmation(app_window)
    else:
        app_window.destroy()

def cancel_exit(confirm_window, app_window):
    confirm_window.destroy()
    app_window.focus_set()

def create_main_window_exit_confirmation():
    confirm = messagebox.askyesno("Exit Confirmation", "Are you sure you want to exit?")
    if confirm:
        display_taskbar_message("To escape, take CONTROL of the situation")

def display_taskbar_message(text):
    taskbar_message.config(text=text, font=("Tahoma", 16, "bold"))
    taskbar_message.pack_configure(expand=True)

def exit_on_ctrl_press(event):
    root.quit()

def open_mind_reader():
    reset_confirmation_count()

    mind_reader_window = tk.Toplevel(root)
    mind_reader_window.title("Mind Reader")
    mind_reader_window.attributes('-fullscreen', True)
    mind_reader_window.grab_set()
    mind_reader_window.focus_set()

    genie_img = Image.open("akinator_genie.png").resize(
        (mind_reader_window.winfo_screenwidth(), mind_reader_window.winfo_screenheight()), Image.LANCZOS
    )
    genie_photo = ImageTk.PhotoImage(genie_img)

    bg_label = tk.Label(mind_reader_window, image=genie_photo)
    bg_label.image = genie_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    text_frame = tk.Frame(mind_reader_window, bg="white")
    text_frame.place(relx=1.0, rely=0.2, anchor='ne')

    messages = [
        "Think of a number between 1 and 3",
        "Scanning your thoughts...",
        "Dodging all negative thoughts...",
        "The number you thought of was 2!"
    ]
    delays = [0, 3000, 4000, 7000]

    for i in range(len(messages)):
        mind_reader_window.after(delays[i], lambda m=messages[i]: display_message(m, text_frame))

    mind_reader_window.bind("<Escape>", lambda event: create_exit_confirmation(mind_reader_window))
    mind_reader_window.protocol("WM_DELETE_WINDOW", lambda: create_exit_confirmation(mind_reader_window))

def display_message(msg, frame):
    label = tk.Label(frame, text=msg, font=("Consolas", 24), bg="white", anchor='e', justify='right')
    label.pack(anchor='e', pady=5, fill='x')

def open_calculator():
    reset_confirmation_count()

    calculator_window = tk.Toplevel(root)
    calculator_window.title("Calculator")
    calculator_window.attributes('-fullscreen', True)
    calculator_window.grab_set()
    calculator_window.focus_set()

    entry = tk.Entry(calculator_window, font=("Consolas", 24), width=15, justify='right')
    entry.grid(row=0, column=0, columnspan=4)

    def evaluate_expression():
        try:
            expression = entry.get()
            expression = expression.replace('*', 'TEMP_DIV').replace('/', 'TEMP_MUL')
            expression = expression.replace('+', 'TEMP_SUB').replace('-', 'TEMP_ADD', 1)
            expression = expression.replace('TEMP_DIV', '/').replace('TEMP_MUL', '*')
            expression = expression.replace('TEMP_SUB', '-').replace('TEMP_ADD', '+')

            result = eval(expression)
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(result))
        except Exception:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Error")

    buttons = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
        ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
    ]

    for (text, row, col) in buttons:
        btn = tk.Button(calculator_window, text=text, font=("Consolas", 18),
                        command=lambda t=text: entry.insert(tk.END, t) if t != '=' else evaluate_expression())
        btn.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)

    for i in range(5):
        calculator_window.grid_rowconfigure(i, weight=1)
        calculator_window.grid_columnconfigure(i, weight=1)

    calculator_window.bind("<Escape>", lambda event: create_exit_confirmation(calculator_window))
    calculator_window.protocol("WM_DELETE_WINDOW", lambda: create_exit_confirmation(calculator_window))

def create_taskbar():
    global taskbar_message
    taskbar = tk.Frame(root, bg='#004080', height=40)
    taskbar.pack(side='bottom', fill='x')

    # Load the start button icon
    start_icon = ImageTk.PhotoImage(Image.open("start_icon.png").resize((40, 40)))  # Change the file name and size as needed

    # Create a label with the start icon
    start_button = tk.Label(taskbar, image=start_icon, bg='#004080', relief='flat')
    start_button.image = start_icon  # Keep a reference to avoid garbage collection
    start_button.bind("<Button-1>", start_menu)  # Bind left mouse click to the start_menu function
    start_button.pack(side='left', padx=5, pady=5)

    taskbar_message = tk.Label(taskbar, text="", bg='#004080', fg='white')
    taskbar_message.pack(side='right', padx=10)
def start_menu(event=None):
    menu = tk.Menu(root, tearoff=0, bg='#c0c0c0', font=("Tahoma", 10))
    menu.add_command(label="Mind Reader", command=open_mind_reader)
    menu.add_command(label="Calculator", command=open_calculator)
    menu.add_separator()
    menu.add_command(label="Exit", command=create_main_window_exit_confirmation)
    menu.tk_popup(10, root.winfo_height() - 100)

def create_desktop_icons():
    mind_reader_icon = ImageTk.PhotoImage(Image.open("mind_reader_icon.png").resize((90, 90)))
    calculator_icon = ImageTk.PhotoImage(Image.open("calculator_icon.png").resize((90, 90)))

    icons = [
        ("Mind Reader", open_mind_reader, mind_reader_icon),
        ("Calculator", open_calculator, calculator_icon),
    ]

    for i, (name, command, icon) in enumerate(icons):
        icon_button = tk.Button(root, image=icon, command=command, relief='flat')
        icon_button.image = icon
        icon_button.place(x=90, y=90 + i * 120)

root = tk.Tk()
root.title("Windows XP Emulator")
root.geometry("800x600")
root.attributes('-fullscreen', True)

bg_image = Image.open("background.png")
bg_photo = ImageTk.PhotoImage(bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS))

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

create_taskbar()
create_desktop_icons()

root.bind("<Escape>", lambda event: create_main_window_exit_confirmation())
root.bind("<Control_L>", exit_on_ctrl_press)

root.mainloop()
