import numpy as np
import cv2
import matplotlib.pyplot as plt

def correlate(answers, bing):
    ret = []
    for ans in answers:
        ret.append( (ans, closest(bing, ans)) )
    return ret

def closest(possible, find):
    min = 9999999
    sel = None
    for i in possible:
        err = sum_square_diff(i, find)
        if err < min:
            min = err
            sel = i
    intersectArea = (min(sel[2],find[2])-max(sel[0],find[0]))*(min(sel[3],find[3])-max(sel[1],find[1]))
    selArea = (sel[2]-sel[0])*(sel[3]-sel[1])
    findArea = (find[2]-find[0])*(find[3]-find[1])
    if intersectArea < 0.60*selArea or intersectArea < 0.60*findArea:
        return None
    return sel

def sum_square_diff(x, y):
    sum = 0
    for i in xrange(len(x)):
        diff = y[i] - x[i]
        sum += diff*diff
    return sum

def display(correlations, img):
    fig, ax = plt.subplots(figsize=(12, 12))
    if img != None:
        img = img[:, :, (2, 1, 0)]
        ax.imshow(img, aspect='equal')
    for i in correlations:
        ax.add_patch(plt.Rectangle((i[0][0], i[0][1])
                                   , i[0][2] - i[0][0]
                                   , i[0][3] - i[0][1], fill=False
                                   , edgecolor='green', linewidth=3.5))
        ax.add_patch(plt.Rectangle((i[1][0], i[1][1])
                                   , i[1][2] - i[1][0]
                                   , i[1][3] - i[1][1], fill=False
                                   , edgecolor='red', linewidth=3.5))
        ax.add_patch(plt.Line2D((i[0][0], i[1][0]), (i[0][1], i[1][1])
                                , color='blue', linewidth=3.5))
    plt.axis('off')
    plt.tight_layout()
    plt.draw()
    plt.show()
