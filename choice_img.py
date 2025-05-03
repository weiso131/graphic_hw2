import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np

def set_img_label(img_label: tk.Label, img_array: np.ndarray):
    img_array = np.clip(img_array, 0, 255).astype(np.uint8)
    pil_img = Image.fromarray(img_array)
    tk_img = ImageTk.PhotoImage(pil_img)

    img_label.config(image=tk_img)
    img_label.image = tk_img

def read_img(img_path: str) -> np.ndarray:
    img =  Image.open(img_path).resize((400, 400))
    return np.array(img)

def choose_file():
    filepath = filedialog.askopenfilename(
        title="選擇一個檔案",
        filetypes=[("圖片檔案", "*.png *.jpg *.jpeg *.bmp"), ("所有檔案", "*.*")]
    )
    return str(filepath)

def btn_choice_img(img_label: tk.Label, img_array_buf: np.ndarray, buf_idx: int):
    def btn_func():
        filepath = choose_file()
        img_array_buf[buf_idx] = read_img(filepath)
        set_img_label(img_label, img_array_buf[buf_idx])
    return btn_func