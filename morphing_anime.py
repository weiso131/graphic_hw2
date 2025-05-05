import time
import numpy as np
import math
import threading

import tkinter as tk

from morphing import morphing
from choice_img import set_img_label


alpha_delta = 0.1
anime_buf = []
buf_cnt = 0
ready_play = False

ready_play_lock = threading.Lock()

def get_morphing_anime(img1_array: np.ndarray, img2_array: np.ndarray, lp_array: list):    
    def least_than_two_img():
        print("meow")
    if (img1_array is None) or (img2_array is None):
        return least_than_two_img

    def morphing_calculate():
        global alpha_delta, anime_buf, buf_cnt, ready_play

        anime_buf = []
        buf_cnt = 0
        alpha = 0

        start = time.time()
        print("start morphing")
        while (1):
            _, _, result = morphing(lp_array, img1_array, img2_array, alpha)
            anime_buf.append(result)
            if math.isclose(alpha, 1.0):
                break
            alpha += alpha_delta
        print(f"end morphing, time: {time.time() - start}")
        with ready_play_lock:
            ready_play = True
            print(f"ready to play{ready_play}")

    def morphing_anime_func():
        threading.Thread(target=morphing_calculate).start()
    return morphing_anime_func

def play_anime(root, result_label: tk.Label):
    global ready_play, buf_cnt
    with ready_play_lock:
        if ready_play:
            print("play anime")
            set_img_label(result_label, anime_buf[buf_cnt])
            buf_cnt += 1
            if buf_cnt >= len(anime_buf):
                ready_play = False
    root.after(100, lambda: play_anime(root, result_label))
