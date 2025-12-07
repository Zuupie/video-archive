# 🎞️ Video Archive App

A lightweight desktop application to locally archive and organize your own (Youtube) video files with thumbnails, categories, and notes.

Developed as a final submission for the MiniHackathon 3.0

---

## ✨ Features

- 📁 Local video archive based on SQLite
- 🖼️ Thumbnail preview for each video
- 🏷️ Custom categories (can be added via UI)
- 📝 Descriptions and notes per video
- 💾 All data stored locally (no cloud, no tracking)

---

## 🖥️ Supported Platforms

- ✅ macOS
- ✅ Linux
- Windows (EXE) //you have to build it first with pyinstaller

---

## ⬇️ Download & Run (Recommended)

👉 **For end users:**

1. Go to **GitHub → Releases**
2. Download the file from the **.zip Folder** section  
3. Open the dist Folder and double-click on `VideoArchive`

### macOS
  - ⚠️ Allow in **Privacy & Security** if prompted


📌 On first start, the application creates a local `data/` folder next to the app to store:
- the SQLite database
- archived video files
- archived thumbnail files

---

## 🛠️ Development Setup (Tech Stack)

- Python 3.11+
- Tkinter (GUI)
- SQLite (local database)
- Pillow (image handling)
- PyInstaller (build & release) Only needed if you want to run or modify the source code.


