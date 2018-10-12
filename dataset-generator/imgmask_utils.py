import numpy as np
import cv2

import matplotlib.pyplot as plt


def gen_circle(img, pos, color, r):
    obj = np.zeros_like(img, dtype=np.uint8)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.circle(obj, pos, r, color, -1)
    cv2.circle(mask, pos, r, 1, -1)
    return obj, mask.astype(np.bool)


def apply_blur_mask(img, obj, mask, ksize=5):
    """
    Takes in a crisp mask, blurs its edges, and applys it to img.
    :param img: Image in
    :param obj: Object to apply
    :return:
    """
    img[mask] = obj[mask]

    kernel = np.ones((ksize, ksize))
    exp = cv2.morphologyEx(mask.astype(np.uint8), cv2.MORPH_DILATE, kernel).astype(np.bool)
    # edge = cv2.morphologyEx(msk.astype(np.uint8), cv2.MORPH_GRADIENT, kernel).astype(np.bool)

    blur = cv2.blur(img, (ksize, ksize))

    img[exp] = blur[exp]


def apply_noise_mask(img, mask, sigma=12):
    noisy = np.random.normal(0, sigma, img.shape) + img
    noisy[noisy<0] = 0
    noisy[noisy>255] = 255

    img[mask] = noisy[mask].astype(np.uint8)


def apply_rotate(obj, center, angle):
    h, w = obj.shape[:2]
    rot = cv2.getRotationMatrix2D(center, angle, 1.0)

    cos, sin = np.abs(rot[0, :2])

    nW, nH = int(h*sin + w*cos), int(h*cos + w*sin)
    rot[:, 2] += np.array([nW, nH])/2 - center
    new_img = cv2.warpAffine(obj, rot, (nW, nH))
    return new_img


if __name__ == '__main__':
    img = cv2.imread('field0.png')[..., ::-1]

    # img = np.zeros((100, 100, 3), dtype=np.uint8)
    circ, mask = gen_circle(img, (2000, 650), (255, 0, 0), 30)

    # img[mask] = circ[mask]
    apply_blur_mask(img, circ, mask, ksize=20)
    apply_noise_mask(img, mask)

    plt.imshow(img)

    plt.show()
