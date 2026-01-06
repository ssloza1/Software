import tkinter as tk
from tkinter import messagebox, ttk
from crud_musics import *

def clear_fields():
    entry_music.delete(0, tk.END)
    entry_artist.delete(0, tk.END)
   

def create():
    try:
        create_music(
            entry_music.get(),
            entry_artist.get(),
            float(entry_balance.get())
        )
        messagebox.showinfo("Success", "Music created successfully")
        load_musics()
        clear_fields()
    except:
        messagebox.showerror("Error", "Invalid data")

frame_form = tk.Frame(root)
frame_form.pack(pady=10)

tk.Label(frame_form, text="Your favorite music").grid(row=0, column=0)
entry_music = tk.Entry(frame_form)
entry_music.grid(row=0, column=1)

tk.Label(frame_form, text="What is the artist").grid(row=1, column=0)
entry_artist = tk.Entry(frame_form)
entry_artist.grid(row=1, column=1)


load_musics()
root.mainloop()