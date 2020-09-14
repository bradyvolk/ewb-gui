import tkinter as tk
from tkinter import messagebox as tkMessageBox


top = tk.Tk()
top.title("My CS Glossary")
top.configure(background="black")
# Add Photo
my_photo = tk.PhotoImage(file="dog.png")
tk.Label(top, image=my_photo, bg="black").grid(row=0, column=0, sticky=tk.E)


top.mainloop()
