import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import threading
import time

from morphing import *
from choice_img import *
from morphing_anime import get_morphing_anime, play_anime

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

lp_array = []

alpha = 0.5
def get_morphing(root, img1_array: np.ndarray, img2_array: np.ndarray, result_buf: np.ndarray, buf_idx: int, \
                    result_label: tk.Label):    
    def least_than_two_img():
        print("meow")
    if (img1_array is None) or (img2_array is None):
        return least_than_two_img

    def morphing_calculate():
        global alpha
        try:
            value = float(alpha_entry.get())
            value = max(0.0, min(1.0, value))
            alpha = value
        except ValueError:
            alpha = 0.5
            print("請輸入合法數字")
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

morphing_btn = tk.Button(root, text="morphing", command=lambda: get_morphing(root, img_buf[IMG1_BUF], img_buf[IMG2_BUF], img_buf, RESULT_BUF, result_img_label)())
morphing_btn.pack(pady=20)

morphing_video_btn = tk.Button(root, text="morphing video", command=lambda: get_morphing_anime(img_buf[IMG1_BUF], 
                                                                                         img_buf[IMG2_BUF], 
                                                                                         lp_array)())
morphing_video_btn.pack(pady=20)

play_anime(root, result_img_label)

start_x = start_y = 0
current_line = None
canvas_id = 0    #user need to draw on img1 then img2
line_pair = []


def mouse_down_func(canvas, img_id):
    def on_mouse_down(event):
        global start_x, start_y, current_line, canvas_id, line_pair, lp_array
        
        if canvas_id == img_id and current_line == None:
            start_x, start_y = event.x, event.y
            current_line = canvas.create_line(start_x, start_y, start_x, start_y, fill="blue", width=2)
        elif canvas_id == img_id:
            canvas.coords(current_line, start_x, start_y, event.x, event.y)
            line_pair.append((current_line, np.array([start_y, start_x]), np.array([event.y, event.x])))
            current_line = None
            canvas_id = (canvas_id + 1) % 3
            if canvas_id == 0:
                lp_array.append(LinePair(line_pair[0][1], line_pair[0][2], 
                                         line_pair[1][1], line_pair[1][2], 
                                         line_pair[0][0], line_pair[1][0]))
                line_pair = []

    return on_mouse_down

def mouse_move_func(canvas, img_id):
    def on_mouse_move(event):
        global start_x, start_y, current_line
        if current_line is not None and canvas_id == img_id:
            canvas.coords(current_line, start_x, start_y, event.x, event.y)

    return on_mouse_move

img1_canvas.bind("<Button-1>", mouse_down_func(img1_canvas, 1))
img1_canvas.bind("<Motion>", mouse_move_func(img1_canvas, 1))
img2_canvas.bind("<Button-1>", mouse_down_func(img2_canvas, 2))
img2_canvas.bind("<Motion>", mouse_move_func(img2_canvas, 2))
def start_draw():
    global current_line, canvas_id, line_pair
    canvas_id = canvas_id == 0
    
    #if user click draw button before draw complete, then release uncomplete part
    if len(line_pair) != 0:       
        img1_canvas.delete(line_pair[0][0])
        if len(line_pair) == 2:
            img2_canvas.delete(line_pair[1][0])
        elif current_line != None:
            img2_canvas.delete(current_line)
    elif current_line != None:
        img1_canvas.delete(current_line)

    current_line = None
    line_pair = []

button = tk.Button(root, text="draw", command=start_draw)
button.pack(padx=20, pady=20)

alpha_container = tk.Frame(root)
alpha_label = tk.Label(alpha_container, text="alpha: ")
alpha_entry = tk.Entry(alpha_container, textvariable=tk.StringVar(value=alpha), width=6)

alpha_label.pack(side="left")
alpha_entry.pack(side="left")
alpha_container.pack(pady=5)

root.mainloop()
