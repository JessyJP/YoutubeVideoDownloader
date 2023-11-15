import tkinter as tk
from tkinter import ttk

def apply_dark_theme(root, theme):
    style = ttk.Style()
    style.configure("TFrame", background=theme['bg'])
    style.configure("TButton", background=theme['button_bg'], foreground=theme['button_fg'], relief="flat")
    style.map("TButton", background=[("active", theme['button_active_bg'])])
    style.configure("TLabel", background=theme['bg'], foreground=theme['label_fg'])
    style.configure("TEntry", fieldbackground=theme['entry_bg'], foreground=theme['entry_fg'])

    for child in root.winfo_children():
        widget_type = child.winfo_class()
        if widget_type in ('TLabel', 'TButton', 'TEntry'):
            pass  # ttk widgets, already styled
        elif widget_type in ('Label', 'Button', 'Entry'):
            child.configure(bg=theme['bg'], fg=theme['fg'])
        apply_dark_theme(child, theme)

def create_widgets(root):
    label = ttk.Label(root, text="Label")
    label.grid(row=0, column=0, padx=5, pady=5)

    button = ttk.Button(root, text="Button")
    button.grid(row=1, column=0, padx=5, pady=5)

    entry = ttk.Entry(root)
    entry.grid(row=2, column=0, padx=5, pady=5)

def main():
    root = tk.Tk()
    root.title("Dark Theme Test")

    # Create a main frame with the desired background color
    main_frame = ttk.Frame(root, style="TFrame")
    main_frame.pack(fill=tk.BOTH, expand=True)

    create_widgets(main_frame)  # Pass the main frame instead of root

    dark_theme = {
        "bg": "#222831",
        "fg": "#eeeeee",
        "button_bg": "#393e46",
        "button_fg": "#eeeeee",
        "button_active_bg": "#30ADA5",
        "label_fg": "#eeeeee",
        "entry_bg": "#393e46",
        "entry_fg": "#eeeeee"
    }

    apply_dark_theme(main_frame, dark_theme)  # Apply theme to main frame

    root.mainloop()

if __name__ == "__main__":
    main()
