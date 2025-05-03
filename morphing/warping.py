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

    u = u.reshape(-1, 1)
    v = v.reshape(-1, 1)

    return src_start + \
        u @ src_vec.reshape(1, -1) + v @ perpendicular(src_vec).reshape(1, -1) / \
            np.linalg.norm(src_vec)

def get_dist(P: np.ndarray, A: np.ndarray, B: np.ndarray) -> np.ndarray:
    AB = B - A 
    AP = P - A 
    AB_len_squared = np.dot(AB, AB)

    if AB_len_squared == 0:
        return np.linalg.norm(AP, axis=1)

    t = np.einsum('ij,j->i', AP, AB) / AB_len_squared  # (n,)
    t = np.clip(t, 0, 1)  # (n,)

    projection = A + t[:, np.newaxis] * AB  # (n,2)
    return np.linalg.norm(P - projection, axis=1)  # (n,)

def get_alpha(dest: np.ndarray, src: np.ndarray, alpha: float):
    return (dest - src) * alpha + src

class LinePair():
    def __init__(self, src_start: np.ndarray, src_end: np.ndarray, \
                 dest_start: np.ndarray, dest_end: np.ndarray, line1_id=None, line2_id=None):
        self.src_start = src_start
        self.src_end = src_end
        self.dest_start = dest_start
        self.dest_end = dest_end
        self.line1_id = line1_id
        self.line2_id = line2_id
    def warping(self, target_dest: np.ndarray, alpha=1.0) -> np.ndarray:
        dest_start_alpha = get_alpha(self.dest_start, self.src_start, alpha)
        dest_end_alpha = get_alpha(self.dest_end, self.src_end, alpha)

        dest_vec = dest_end_alpha - dest_start_alpha
        src_vec = self.src_end - self.src_start
        dest_target_vec = target_dest - dest_start_alpha

        src_start = np.ones_like(target_dest) * self.src_start

        return warping(dest_vec, src_vec, dest_target_vec, src_start)
    def weight(self, target_dest: np.ndarray, alpha=1.0, a=0.1, b=1, p=0.5) -> float:
        dest_start_alpha = get_alpha(self.dest_start, self.src_start, alpha)
        dest_end_alpha = get_alpha(self.dest_end, self.src_end, alpha)

        length = np.linalg.norm(dest_end_alpha - dest_start_alpha)
        dist = get_dist(target_dest, dest_start_alpha, dest_end_alpha)
        return (((length ** p) / (a + dist)) ** b)
    def reverse(self):
        return LinePair(self.dest_start, self.dest_end, self.src_start, self.src_end)
    def __str__(self):
        return (f"src_start: {self.src_start}, src_end: {self.src_end}, dest_start: {self.dest_start}, dest_end: {self.dest_end}\n")

def bounding(l: int, r: int, value: float):
    return min(r, max(l, int(value)))

def mul_line_warping(img_array: np.ndarray, lp_array: list[LinePair], alpha=1.0, a=0.1, b=1, p=0.5):
    n, m, _ = img_array.shape
    target = []
    for i in range(n):
        for j in range(m):
            target.append([i, j])
    target_dest = np.array(target)

    new_img_array = np.zeros_like(img_array)
    
    weight_sum = np.zeros((n * m, 1))
    dsum = np.zeros((n * m, 2))
    for lp in lp_array:
        weight = lp.weight(target_dest, alpha, a, b, p).reshape(-1, 1)
        weight_warping = weight * lp.warping(target_dest, alpha)

        dsum += weight_warping
        weight_sum += weight

    pos = dsum / weight_sum.reshape(-1, 1)

    pos = pos.astype(np.int32).reshape(n, m, 2)


    for i in range(n):
        for j in range(m):
            new_img_array[i, j] = img_array[bounding(0, n - 1, pos[i, j, 0]), 
                                bounding(0, m - 1, pos[i, j, 1])]
    return new_img_array