import tkinter as tk
from tkinter import messagebox


def user_confirm(prompt):
    root = tk.Tk()
    root.withdraw()

    response = messagebox.askyesno("Confirmation", prompt)

    root.destroy()

    return response
