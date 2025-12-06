import tkinter as tk
from database import init_db
from ui_form import VideoForm
from ui_list import VideoList

def main():
    init_db()

    root = tk.Tk()
    root.title("Video Archiv App")

    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    def show_form():
        clear()
        form = VideoForm(container, show_list)
        form.pack(fill="both", expand=True)

    def show_list():
        clear()
        listing = VideoList(container, show_form)
        listing.pack(fill="both", expand=True)

    def clear():
        for widget in container.winfo_children():
            widget.destroy()

    show_list()

    root.mainloop()

if __name__ == "__main__":
    main()
