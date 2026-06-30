# 🖼️ Background Remover Utility

A simple and elegant GUI application built with Python to remove backgrounds from images effortlessly. This project uses `customtkinter` for a modern dark/light mode interface and the `rembg` library for high-quality background removal.

![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg?logo=python&logoColor=white) ![Platform Windows](https://img.shields.io/badge/Platform-Windows-blue.svg?logo=windows&logoColor=white) ![License GPL--3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/netanelelhadad)

## 🌟 Features
- **Modern UI**: Clean and user-friendly interface using `customtkinter`.
- **Easy to Use**: Select an image, remove the background with one click, and save the result as a PNG.
- **Asynchronous Processing**: The UI remains responsive while the background is being processed.
- **Standalone Executable Support**: Designed to work smoothly even when compiled into a standalone `.exe` using PyInstaller.

## 🛠️ Prerequisites
Make sure you have Python installed. Then, install the required libraries:

```bash
pip install customtkinter Pillow rembg
```

## 🚀 How to Run
1. Clone this repository or download the source code.
2. Open your terminal or command prompt in the project directory.
3. Run the script:
   ```bash
   python bg_remover_app.py
   ```
4. Click **Select Picture** to choose an image (JPG, PNG, WEBP).
5. Click **Remove Background and Save** to process the image and choose where to save the transparent PNG.

## ⚖️ License
This project is licensed under the **GPL-3.0 License**.

## 👨‍💻 Credits
Created by **Netanel Elhadad**.
