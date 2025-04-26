import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
import threading
import time

from morphing import *

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

def get_morphing(root, img1_array: np.ndarray, img2_array: np.ndarray, result_buf: np.ndarray, buf_idx: int, \
                    result_label: np.ndarray, alpha: int):
    def least_than_two_img():
        print("meow")
    if (img1_array is None) or (img2_array is None):
        return least_than_two_img

    def morphing_calculate():
        lp_array = [LinePair(np.array([20, 10]), np.array([25, 80]), \
        np.array([45, 60]), np.array([45, 95])), 
        LinePair(np.array([25, 175]), np.array([20, 245]), \
        np.array([45, 140]), np.array([45, 170])), 
        LinePair(np.array([50, 127]), np.array([120, 127]), \
        np.array([50, 116]), np.array([110, 116])),
        LinePair(np.array([180, 100]), np.array([180, 160]), \
        np.array([130, 90]), np.array([130, 140])),]

        start = time.time()
        print("start morphing")
        _, _, result_buf[buf_idx] = morphing(lp_array, img1_array, img2_array, alpha)
        print(f"end morphing, time: {time.time() - start}")

        root.after(0, lambda: set_img_label(result_label, result_buf[buf_idx]))

    def morphing_func():
        threading.Thread(target=morphing_calculate).start()
    return morphing_func

root = tk.Tk()
root.title("多張圖片展示")
root.geometry("1920x1080")

empty_img_array = np.zeros((400, 400, 3), dtype=np.uint8)
empty_img_array[:, :] = [230, 230, 230]
pil_img = Image.fromarray(empty_img_array)
empty_img = ImageTk.PhotoImage(pil_img)


frame = tk.Frame(root)
frame.pack(pady=20)

img_buf = [None, None, None]

IMG1_BUF = 0
IMG2_BUF = 1
RESULT_BUF = 2

img1_label = tk.Label(frame, image=empty_img)
img2_label = tk.Label(frame, image=empty_img)
result_img_label = tk.Label(frame, image=empty_img)

img1_label.grid(row=0, column=0, padx=10)
img2_label.grid(row=0, column=1, padx=10)
result_img_label.grid(row=0, column=2, padx=10)


img1_btn = tk.Button(root, text="選擇檔案", command=btn_choice_img(img1_label, img_buf, IMG1_BUF))
img1_btn.pack(pady=20)

img2_btn = tk.Button(root, text="選擇檔案", command=btn_choice_img(img2_label, img_buf, IMG2_BUF))
img2_btn.pack(pady=20)

img2_btn = tk.Button(root, text="morphing", command=lambda: get_morphing(root, img_buf[IMG1_BUF], img_buf[IMG2_BUF], img_buf, RESULT_BUF, result_img_label, 0.5)())
img2_btn.pack(pady=20)

root.mainloop()

