import tkinter as tk
from tkinter import ttk
from database import get_all_videos, add_category
from PIL import Image, ImageTk
from pathlib import Path


THUMBNAIL_SIZE = (120, 80)


class VideoList(tk.Frame):
    def __init__(self, master, switch_to_form):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.bind("<Configure>", self.on_resize)
        self.images = []  # wichtig: Referenzen für Thumbnails halten

        # Top-Bar
        top = tk.Frame(self)
        top.pack(fill="x", pady=5)

        tk.Button(top, text="➕ Neues Video", command=switch_to_form).pack(side="left", padx=10)
        tk.Button(top, text="📁 Kategorien", command=self.open_category_dialog).pack(side="left")

        # Scrollbereich
        self.canvas = tk.Canvas(self, borderwidth=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self._scroll_buffer = 0.0
        self.canvas.bind("<Enter>", self._bind_mousewheel)
        self.canvas.bind("<Leave>", self._unbind_mousewheel)


        self.scrollbar.pack(side="right", fill="y")


        self.refresh()

    def refresh(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        rows = get_all_videos()

        for row in rows:
            self.create_video_item(self.scroll_frame, row)

    def create_video_item(self, parent, row):
        (
            _id,
            title,
            description,
            note,
            category,
            date,
            video_path,
            thumbnail_path
        ) = row

        item = tk.Frame(parent, relief="groove", borderwidth=1, padx=10, pady=10)
        item.pack(fill="x", padx=10, pady=6)

        item.grid_columnconfigure(1, weight=1)
        item.grid_columnconfigure(2, weight=0)

        # --- Thumbnail ---
        thumb_label = tk.Label(item)
        thumb_label.grid(row=0, column=0, rowspan=2, sticky="nw", padx=(0, 12))

        img = self.load_thumbnail(thumbnail_path)
        if img:
            thumb_label.config(image=img)
            self.images.append(img)
        else:
            thumb_label.config(text="No\nImage", width=12, height=5)

        # --- Mitte ---
        mid = tk.Frame(item)
        mid.grid(row=0, column=1, sticky="nsew")

        title_lbl = tk.Label(mid, text=title, font=("Helvetica", 13, "bold"), anchor="w")
        title_lbl.pack(anchor="w")

        meta_lbl = tk.Label(mid, text=f"{category} | {date}", fg="gray")
        meta_lbl.pack(anchor="w", pady=(0, 4))

        desc_lbl = tk.Label(
            mid,
            text=description,
            justify="left",
            anchor="w"
        )
        desc_lbl.pack(fill="x")

        # --- Notiz ---
        note_lbl = tk.Label(
            item,
            text=note,
            justify="left",
            anchor="nw",
            fg="#444"
        )
        note_lbl.grid(row=0, column=2, rowspan=2, sticky="n", padx=(12, 0))

        # Referenzen für Resize
        item.desc_lbl = desc_lbl
        item.note_lbl = note_lbl

    def on_resize(self, event=None):
        width = self.winfo_width()

        # dynamische Textbreiten
        desc_width = max(300, width - 500)
        note_width = max(180, width // 4)

        for item in self.scroll_frame.winfo_children():
            if hasattr(item, "desc_lbl"):
                item.desc_lbl.config(wraplength=desc_width)
            if hasattr(item, "note_lbl"):
                item.note_lbl.config(wraplength=note_width)



    def load_thumbnail(self, path):
        if not path:
            return None

        p = Path(path)
        if not p.exists():
            return None

        try:
            img = Image.open(p)
            img.thumbnail(THUMBNAIL_SIZE)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None

    def _bind_mousewheel(self, event=None):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)     # Windows / macOS
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)       # Linux scroll up
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)       # Linux scroll down


    def _unbind_mousewheel(self, event=None):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        # Bestimme delta plattformunabhängig
        if hasattr(event, "delta") and event.delta:
            # Windows / macOS: event.delta (macOS meist feiner)
            delta = event.delta
        elif event.num == 4:
            delta = 120    # scroll up mouse wheel on many X11 setups
        elif event.num == 5:
            delta = -120   # scroll down
        else:
            return

        # Sammle deltas im Puffer und dämpfe sie (Faktor anpassen)
        self._scroll_buffer += -delta * 1.75  # 0.25 = Dämpfungs-/Sensitivitätsfaktor

        # Wenn genug Pixel im Puffer sind, führe Scroll aus
        scroll_pixels = int(self._scroll_buffer)
        if scroll_pixels == 0:
            return

        # Hole Gesamt-Höhe des Inhalts
        bbox = self.canvas.bbox("all")
        if not bbox:
            return
        total_height = max(1, bbox[3] - bbox[1])  # Absicherung gegen 0

        # Aktuelle Scroll-Position als Fraction (0.0 - 1.0)
        cur_frac = self.canvas.yview()[0]

        # Fractionale Verschiebung basierend auf Pixelbewegung
        frac_delta = scroll_pixels / total_height
        new_frac = cur_frac + frac_delta

        # Clamp zwischen 0 und 1
        if new_frac < 0:
            new_frac = 0.0
        elif new_frac > 1:
            new_frac = 1.0

        # Anwenden
        self.canvas.yview_moveto(new_frac)

        # Verbrauchte Pixel aus Puffer entfernen
        self._scroll_buffer -= scroll_pixels

    def open_category_dialog(self):
        win = tk.Toplevel(self)
        win.title("Kategorie hinzufügen")
        win.geometry("300x120")
        win.transient(self)
        win.grab_set()

        tk.Label(win, text="Neue Kategorie").pack(pady=5)
        entry = tk.Entry(win, width=30)
        entry.pack()

        def save_cat():
            name = entry.get().strip()
            if name:
                add_category(name)
                win.destroy()

        tk.Button(win, text="Speichern", command=save_cat).pack(pady=10)

