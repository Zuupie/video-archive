import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import os
import re

from file_manager import save_video_and_thumbnail
from database import insert_video


CATEGORIES = ["", "Privat", "Arbeit", "Projekt", "Tutorial", "Sonstiges"]
DATE_REGEX = r"^\d{4}-\d{2}-\d{2}$"


class VideoForm(tk.Frame):
    def __init__(self, master, switch_to_list):
        super().__init__(master)
        self.switch_to_list = switch_to_list
        self.today = datetime.today().strftime("%Y-%m-%d")
        self.date_placeholder = self.today

        # ---------- Titel (Pflicht) ----------
        tk.Label(self, text="Titel *").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(self, width=40)
        self.title_entry.grid(row=0, column=1)

        # ---------- Beschreibung ----------
        tk.Label(self, text="Beschreibung").grid(row=1, column=0, sticky="w")
        self.desc_entry = tk.Entry(self, width=40)
        self.desc_entry.grid(row=1, column=1)

        # ---------- Notiz ----------
        tk.Label(self, text="Notiz").grid(row=2, column=0, sticky="w")
        self.note_entry = tk.Entry(self, width=40)
        self.note_entry.grid(row=2, column=1)

        # ---------- Kategorie (Enum) ----------
        tk.Label(self, text="Kategorie").grid(row=3, column=0, sticky="w")
        self.category_var = tk.StringVar(value="")
        self.cat_menu = tk.OptionMenu(self, self.category_var, *CATEGORIES)
        self.cat_menu.grid(row=3, column=1, sticky="w")

        # ---------- Datum ----------
        tk.Label(self, text="Datum (YYYY-MM-DD)").grid(row=4, column=0, sticky="w")
        self.date_entry = tk.Entry(self, width=40, fg="grey")
        self.date_entry.insert(0, self.date_placeholder)
        self.date_entry.grid(row=4, column=1)
        self.date_entry.bind("<FocusIn>", self._clear_date_placeholder)
        self.date_entry.bind("<FocusOut>", self._restore_date_placeholder)

        # ---------- Video-Pfad (Pflicht) ----------
        tk.Button(self, text="Video auswählen *", command=self.pick_video).grid(row=5, column=0)
        self.video_path = tk.Label(self, text="", fg="grey", wraplength=300, anchor="w", justify="left")
        self.video_path.grid(row=5, column=1, sticky="w")

        # ---------- Thumbnail ----------
        tk.Button(self, text="Thumbnail auswählen", command=self.pick_thumbnail).grid(row=6, column=0)
        self.thumb_path = tk.Label(self, text="", fg="grey", wraplength=300, anchor="w", justify="left")
        self.thumb_path.grid(row=6, column=1, sticky="w")

        # ---------- Buttons ----------
        tk.Button(self, text="Speichern", command=self.save).grid(row=7, column=0, pady=10)
        tk.Button(self, text="Zur Liste", command=switch_to_list).grid(row=7, column=1, pady=10)

    # ---------------- Actions ----------------

    def pick_video(self):
        file = filedialog.askopenfilename(title="Video auswählen")
        if file:
            self.video_path.config(text=file)

    def pick_thumbnail(self):
        file = filedialog.askopenfilename(title="Thumbnail auswählen")
        if file:
            self.thumb_path.config(text=file)

    def _clear_date_placeholder(self, event):
        if self.date_entry.get() == self.date_placeholder:
            self.date_entry.delete(0, tk.END)
            self.date_entry.config(fg="black")

    def _restore_date_placeholder(self, event):
        if not self.date_entry.get():
            self.date_entry.insert(0, self.date_placeholder)
            self.date_entry.config(fg="grey")

    # ---------------- Validation ----------------

    def validate(self):
        errors = []
        data = {}

        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        note = self.note_entry.get().strip()
        category = self.category_var.get()
        date = self.date_entry.get().strip()
        video = self.video_path.cget("text").strip()
        thumbnail = self.thumb_path.cget("text").strip()
        

        # Pflicht: Titel
        if not title:
            errors.append("Titel ist ein Pflichtfeld.")

        if not description:
            description = ""

        if not note:
            note = ""

        if not category:
            category = ""

        # Pflicht: Video-Pfad
        if not video:
            errors.append("Video-Datei muss ausgewählt werden.")

        if not thumbnail:
            thumbnail = ""

        # Datum prüfen
        if date:
            if not re.match(DATE_REGEX, date):
                errors.append("Datum muss im Format YYYY-MM-DD sein.")
        else:
            date = datetime.today().strftime("%Y-%m-%d")
        
        if not errors:
            data = {
                "title": title,
                "description": description,
                "note": note,
                "category": category,
                "date": date,
            }

        return errors, data

    # ---------------- Save ----------------

    def save(self):
        errors, data = self.validate()

        if errors:
            messagebox.showerror(
                "Ungültige Eingabe",
                "\n".join(errors)
            )
            return

        video = self.video_path.cget("text").strip()
        thumb = self.thumb_path.cget("text").strip()

        try:
            new_video, new_thumb = save_video_and_thumbnail(video, thumb, data)

            data["video_path"] = new_video
            data["thumbnail_path"] = new_thumb

            insert_video(data)

            messagebox.showinfo("Erfolg", "Video wurde erfolgreich archiviert ✅")
            self.switch_to_list()

        except Exception as e:
            messagebox.showerror("Fehler", f"Speichern fehlgeschlagen:\n{e}")



