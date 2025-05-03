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

img1_canvas = tk.Canvas(frame, width=400, height=400)
img2_canvas = tk.Canvas(frame, width=400, height=400)
img1_id = img1_canvas.create_image(0, 0, anchor='nw', image=empty_img)
img2_id = img2_canvas.create_image(0, 0, anchor='nw', image=empty_img)

result_img_label = tk.Label(frame, image=empty_img)

img1_canvas.grid(row=0, column=0, padx=10)
img2_canvas.grid(row=0, column=1, padx=10)
result_img_label.grid(row=0, column=2, padx=10)


img1_btn = tk.Button(root, text="選擇檔案", command=btn_choice_img(img1_canvas, img_buf, IMG1_BUF, img1_id))
img1_btn.pack(pady=20)

img2_btn = tk.Button(root, text="選擇檔案", command=btn_choice_img(img2_canvas, img_buf, IMG2_BUF, img2_id))
img2_btn.pack(pady=20)

img2_btn = tk.Button(root, text="morphing", command=lambda: get_morphing(root, img_buf[IMG1_BUF], img_buf[IMG2_BUF], img_buf, RESULT_BUF, result_img_label, 0.5)())
img2_btn.pack(pady=20)

def check_inside(img: tuple, x: int, y: int) -> bool:
    rootx, rooty, endx, endy = img
    return x > rootx and x < endx and y > rooty and y < endy

def on_click_func(img1: tk.Label, img2: tk.Label):
    img_list = [(img1.winfo_rootx(), img1.winfo_rooty(), 
                 img1.winfo_rootx() + img1.winfo_width(), 
                 img1.winfo_rooty() + img1.winfo_height()),
                (img2.winfo_rootx(), img2.winfo_rooty(), 
                 img2.winfo_rootx() + img2.winfo_width(), 
                 img2.winfo_rooty() + img2.winfo_height())]

    def on_click(_):
        global access_mouse
        if access_mouse:
            x = root.winfo_pointerx()
            y = root.winfo_pointery()

            for i in range(len(img_list)):
                if check_inside(img_list[i], x, y):
                    print(f"inside img{i + 1}")
                    break

    return on_click

def show_mouse_position():
    global access_mouse
    access_mouse ^= True

button = tk.Button(root, text="Get Mouse Position", command=show_mouse_position)
button.pack(padx=20, pady=20)


root.bind("<Button-1>", func=lambda event: on_click_func(img1_canvas, img2_canvas)(event))

root.mainloop()

