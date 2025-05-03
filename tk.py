import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import threading
import time

from morphing import *
from choice_img import *

root = tk.Tk()
root.title("morphing")
root.geometry("1920x1080")

empty_img_array = np.zeros((400, 400, 3), dtype=np.uint8)
empty_img_array[:, :] = [230, 230, 230]
pil_img = Image.fromarray(empty_img_array)
empty_img = ImageTk.PhotoImage(pil_img)

IMG1_BUF = 0
IMG2_BUF = 1
RESULT_BUF = 2

img_buf = [None, None, None] #save the img np array

access_mouse = False #if True, on_click will get the mouse position

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

frame = tk.Frame(root)
frame.pack(pady=20)

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

