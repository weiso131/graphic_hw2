import numpy as np

def perpendicular(vec: np.ndarray) -> np.ndarray:
    a = vec[0]
    b = vec[1]
    return np.array([b, -a])

def warping(dest_vec: np.ndarray, src_vec: np.ndarray, 
            dest_target_vec: np.ndarray, src_start: np.ndarray) -> np.ndarray:
    """
    Args:
        dest_vec(np.ndarray): Q - P
        src_vec(np.ndarray):  Q' - P'
        dest_target_vec(np.ndarray): X - P
        src_start(np.ndarray): P'
    Returns:
        np.ndarray: X'
    """
    u = np.dot(dest_target_vec, dest_vec) / \
                ((dest_vec ** 2).sum())
    v = np.dot(dest_target_vec, perpendicular(dest_vec)) / \
                np.linalg.norm(dest_vec)
    return src_start + \
        u * src_vec + v * perpendicular(src_vec) / \
            np.linalg.norm(src_vec)

def get_dist(P: np.ndarray, A: np.ndarray, B: np.ndarray) -> float:
    P = np.array(P)
    A = np.array(A)
    B = np.array(B)
    AB = B - A
    AP = P - A
    AB_len_squared = np.dot(AB, AB)

    if AB_len_squared == 0:
        return np.linalg.norm(AP) 

    t = np.dot(AP, AB) / AB_len_squared
    t = np.clip(t, 0, 1) 

    projection = A + t * AB
    return np.linalg.norm(P - projection)

def get_alpha(dest: np.ndarray, src: np.ndarray, alpha: float):
    return (dest - src) * alpha + src

class LinePair():
    def __init__(self, src_start: np.ndarray, src_end: np.ndarray, \
                 dest_start: np.ndarray, dest_end: np.ndarray):
        self.src_start = src_start
        self.src_end = src_end
        self.dest_start = dest_start
        self.dest_end = dest_end
    def warping(self, target_dest: np.ndarray, alpha=1.0) -> np.ndarray:
        dest_start_alpha = get_alpha(self.dest_start, self.src_start, alpha)
        dest_end_alpha = get_alpha(self.dest_end, self.src_end, alpha)

        dest_vec = dest_end_alpha - dest_start_alpha
        src_vec = self.src_end - self.src_start
        dest_target_vec = target_dest - dest_start_alpha
        return warping(dest_vec, src_vec, dest_target_vec, self.src_start)
    def weight(self, target_dest: np.ndarray, alpha=1.0, a=0.1, b=1, p=0.5) -> float:
        dest_start_alpha = get_alpha(self.dest_start, self.src_start, alpha)
        dest_end_alpha = get_alpha(self.dest_end, self.src_end, alpha)

        length = np.linalg.norm(dest_end_alpha - dest_start_alpha)
        dist = get_dist(target_dest, dest_start_alpha, dest_end_alpha)
        return ((length ** p) / (a + dist)) ** b
    def reverse(self):
        return LinePair(self.dest_start, self.dest_end, self.src_start, self.src_end)

def bounding(l: int, r: int, value: float):
    return min(r, max(l, int(value)))

def mul_line_warping(img_array: np.ndarray, lp_array: list[LinePair], alpha=1.0, a=0.1, b=1, p=0.5):
    n, m, _ = img_array.shape
    new_img_array = np.zeros_like(img_array)

    for i in range(n):
        for j in range(m):
            weight_sum = 0
            dsum = np.array([0.0, 0.0])
            target_dest = np.array([i, j])
            for lp in lp_array:
                weight = lp.weight(target_dest, alpha=alpha, a=a, b=b, p=p)
                dsum += weight * lp.warping(target_dest, alpha=alpha)
                weight_sum += weight
            
            pos = dsum / weight_sum
            new_img_array[i, j] = \
                    img_array[bounding(0, n - 1, pos[0]), 
                            bounding(0, m - 1, pos[1])]
    return new_img_array