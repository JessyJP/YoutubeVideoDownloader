import tkinter as tk
from tkinter import ttk


def apply_dark_theme(root, theme):
    root.configure(bg=theme['bg'])

    ttk.Style().configure("TButton", background=theme['button_bg'], foreground=theme['button_fg'], relief="flat")
    ttk.Style().map("TButton", background=[("active", theme['button_active_bg'])])

    ttk.Style().configure("TLabel", bg=theme['bg'], foreground=theme['label_fg'])
    ttk.Style().configure("TEntry", fieldbackground=theme['entry_bg'], foreground=theme['entry_fg'], bg=theme['bg'])

    for child in root.winfo_children():
        widget_type = child.winfo_class()
        if widget_type in ('Label', 'Button', 'Entry'):
            child.configure(bg=theme['bg'], fg=theme['fg'])
        elif widget_type in ('TLabel', 'TButton', 'TEntry'):
            pass
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

    create_widgets(root)

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

    apply_dark_theme(root, dark_theme)

    root.mainloop()


if __name__ == "__main__":
    main()
