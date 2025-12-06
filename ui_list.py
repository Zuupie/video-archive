import tkinter as tk
from database import get_all_videos

class VideoList(tk.Frame):
    def __init__(self, master, switch_to_form):
        super().__init__(master)

        tk.Button(self, text="Neues Video", command=switch_to_form).pack()

        self.listbox = tk.Listbox(self, width=60, height=20)
        self.listbox.pack()

        self.refresh()

    def refresh(self):
        self.listbox.delete(0, tk.END)
        rows = get_all_videos()

        for row in rows:
            vid = f"{row[1]}  |  {row[3]}  |  {row[4]}"
            self.listbox.insert(tk.END, vid)
