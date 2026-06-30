"""
Background Remover Utility
Copyright (C) 2024 Netanel Elhadad

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Author: Netanel Elhadad
"""

# --- תיקון לשגיאת קונסול ב-EXE - חייב להיות בראש הקובץ ---
import sys
import os

# אם התוכנה רצה כקובץ EXE (Frozen)
if getattr(sys, 'frozen', False):
    # הפניית פלט סטנדרטי (stdout, stderr) ל'שום מקום' כדי למנוע קריסה
    # ב-customtkinter כשאין קונסול פתוח.
    f = open(os.devnull, 'w')
    sys.stdout = f
    sys.stderr = f
else:
    # פילטר שמנקה הדפסות אזהרה ישירות ל-stderr מצד customtkinter
    class CTkStderrFilter:
        def __init__(self, stream):
            self.stream = stream
        def write(self, data):
            if "customtkinter.windows.widgets.font warning" in data or "font_shapes" in data or "circle_shapes" in data:
                return
            self.stream.write(data)
        def flush(self):
            self.stream.flush()
    sys.stderr = CTkStderrFilter(sys.stderr)
# -----------------------------------------------------------

import customtkinter as ctk

# הגדרה רשמית לשיטת ציור חלופית (ליתר ביטחון)
ctk.DrawEngine.preferred_drawing_method = "polygon_shapes"

from tkinter import filedialog, messagebox
from PIL import Image
from rembg import remove
import threading

# הגדרת עיצוב כללי לממשק
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class BackgroundRemoverApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Background Remover Utility")
        self.geometry("350x250")  # הגדלתי מעט את הגובה כדי שיהיה מקום לקרדיט
        self.resizable(False, False)

        self.input_path = None

        # --- יצירת רכיבי הממשק ---

        # כותרת
        self.title_label = ctk.CTkLabel(self, text="Remove Background", font=ctk.CTkFont(size=20, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        # כפתור בחירת תמונה
        self.select_btn = ctk.CTkButton(self, text="Select Picture", command=self.select_image)
        self.select_btn.pack(pady=10)

        # תצוגת נתיב הקובץ שנבחר
        self.path_label = ctk.CTkLabel(self, text="You dont select a picture", text_color="gray")
        self.path_label.pack(pady=5)

        # כפתור הסרת רקע
        self.process_btn = ctk.CTkButton(self, text="Remove Background and Save", command=self.start_processing,
                                         state="disabled")
        self.process_btn.pack(pady=10)

        # מד התקדמות (מוסתר כברירת מחדל)
        self.progress_bar = ctk.CTkProgressBar(self, mode="indeterminate")

        # --- הוספת שורת קרדיט למטה ---
        self.credit_label = ctk.CTkLabel(self, text="Created by Netanel Elhadad", font=ctk.CTkFont(size=11),
                                         text_color="gray")
        # מיקום בתחתית החלון עם מרווח קטן
        self.credit_label.pack(side="bottom", pady=10)

    def select_image(self):
        # פתיחת חלון לבחירת קובץ
        file_path = filedialog.askopenfilename(
            title="Select Picture",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.webp")]
        )
        if file_path:
            self.input_path = file_path
            # הצגת שם הקובץ הנבחר (רק השם, ללא כל הנתיב הארוך)
            filename = os.path.basename(file_path)
            self.path_label.configure(text=filename, text_color=("black", "white"))
            self.process_btn.configure(state="normal")

    def start_processing(self):
        # בחירת נתיב לשמירת הקובץ החדש
        output_path = filedialog.asksaveasfilename(
            title="Save Picture as..",
            defaultextension=".png",
            filetypes=[("PNG file", "*.png")]
        )

        if output_path:
            # עדכון הממשק להתחלת עבודה
            self.process_btn.configure(state="disabled")
            self.select_btn.configure(state="disabled")

            # הסרת הקרדיט זמנית כדי לפנות מקום למד ההתקדמות (אופציונלי)
            # self.credit_label.pack_forget()

            self.progress_bar.pack(pady=10)
            self.progress_bar.start()

            # הפעלת תהליך הסרת הרקע בתהליכון נפרד כדי לא לתקוע את הממשק
            threading.Thread(target=self.remove_background_task, args=(self.input_path, output_path),
                             daemon=True).start()

    def remove_background_task(self, input_path, output_path):
        try:
            # פתיחת התמונה, הסרת הרקע ושמירה
            input_image = Image.open(input_path)
            output_image = remove(input_image)
            output_image.save(output_path)

            # הצגת הודעת הצלחה (קריאה חזרה ל-Thread של הממשק)
            self.after(0, self.show_success, output_path)

        except Exception as e:
            self.after(0, self.show_error, str(e))

    def show_success(self, output_path):
        self.reset_ui()
        messagebox.showinfo("Success!", f"The background was removed successfully.\nSaved to:\n{output_path}")

    def show_error(self, error_message):
        self.reset_ui()
        messagebox.showerror("Error", f"An error occurred during processing:\n{error_message}")

    def reset_ui(self):
        # עצירת מד ההתקדמות והחזרת הכפתורים למצב פעיל
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

        # החזרת הקרדיט למטה
        # self.credit_label.pack(side="bottom", pady=10)

        self.select_btn.configure(state="normal")
        self.process_btn.configure(state="normal")


if __name__ == "__main__":
    app = BackgroundRemoverApp()
    app.mainloop()