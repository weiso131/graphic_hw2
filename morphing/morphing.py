import numpy as np

from .warping import LinePair, mul_line_warping

def morphing(lp_array: list[LinePair], img_array1: np.ndarray, img_array2: np.ndarray, alpha=1, a=0.1, b=1, p=0.5):
    reverse_lp_array = []

    for lp in lp_array:
        reverse_lp_array.append(lp.reverse())
        
    new_img_array1 = mul_line_warping(img_array1, reverse_lp_array, alpha=alpha, a=a, b=b, p=p)
    new_img_array2 = mul_line_warping(img_array2, lp_array, alpha=1 - alpha, a=a, b=b, p=p)

    return new_img_array1, new_img_array2, new_img_array1 * (1 - alpha) + new_img_array2 * alpha