import numpy as np
import math
from .warping import LinePair, mul_line_warping

def morphing(lp_array: list[LinePair], img_array1: np.ndarray, img_array2: np.ndarray, alpha=1.0, a=0.1, b=1, p=0.5):
    reverse_lp_array = []

    for lp in lp_array:
        reverse_lp_array.append(lp.reverse())
    
    if math.isclose(alpha, 0.0):
        new_img_array1 = img_array1
    else:
        new_img_array1 = mul_line_warping(img_array1, lp_array, alpha=alpha, a=a, b=b, p=p)

    if math.isclose(alpha, 1.0):
        new_img_array2 = img_array2
    else:
        new_img_array2 = mul_line_warping(img_array2, reverse_lp_array, alpha=1 - alpha, a=a, b=b, p=p)

    return new_img_array1, new_img_array2, new_img_array1 * (1 - alpha) + new_img_array2 * alpha