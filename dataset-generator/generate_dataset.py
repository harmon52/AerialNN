import numpy as np
import cv2 as cv2
import sys as sys
import math as math
import os as os
import os.path
import random as random
import string as string

import generate_coordinates as generate_coordinates
import imgmask_utils as imgmask_utils
import genPolygon as genPolygon


desiredOutputs = 1500
numShapes = 3


colors = [ ("red", (255, 0, 0)), ("green", (0, 255, 0)), ("blue", (0, 0, 255)) ]
chars = list(string.ascii_uppercase + string.digits)
minRadius = 35
maxRadius = 40
def randradius():
    return random.randint(minRadius, maxRadius)
    
shapes = []
maxSidedPolygon = 7
for sides in range(3, maxSidedPolygon+1):
    shapes.append(lambda img, coord, angle, color: genPolygon.regular_polygon(img, coord, randradius(), sides, angle, color))
minStarPoints = 5
maxStarPoints = 5
shapes.append(lambda img, coord, angle, color: genPolygon.star(img, coord, randradius(), random.randint(minStarPoints, maxStarPoints), angle, color))
shapes.append(lambda img, coord, angle, color: genPolygon.circle(img, coord, randradius(), angle, color))
shapes.append(lambda img, coord, angle, color: genPolygon.half_circle(img, coord, randradius(), angle, color))
shapes.append(lambda img, coord, angle, color: genPolygon.quarter_circle(img, coord, randradius(), angle, color))
minCrossArmWidthRadiusPortion = 0.48
maxCrossArmWidthRadiusPortion = 0.52
shapes.append(lambda img, coord, angle, color: (lambda radius: genPolygon.cross(img, coord, 2*radius, random.randint(int(radius*minCrossArmWidthRadiusPortion), int(radius*maxCrossArmWidthRadiusPortion)), angle, color))(randradius()))

def overlay_img(img, numShapes, dbg):
    h, w = img.shape[:2]
    x1,y1,x2,y2,x3,y3 = generate_coordinates.coordinate_generator(w, h)
    coords = [(x1, y2), (x2, y2), (x3, y3)]
    for coord in coords:
        angle = random.randint(0, 359)
        shape_color = random.choice(colors)[1]
        obj, mask = random.choice(shapes)(img, coord, angle, shape_color)
        text_color = random.choice(colors)[1]
        while text_color == shape_color:
            text_color = random.choice(colors)[1]
        # text_size = math.ceil(0.3*minRadius)
        text_size = 1
        genPolygon.put_text(obj, coord, text_size, random.choice(chars), angle, text_color)
        imgmask_utils.apply_blur_mask(img, obj, mask, ksize=4)
#        imgmask_utils.apply_noise_mask(img, mask, sigma=12)


def left_pad(s, n, prefix):
    while len(s) < n:
        s = prefix+s
    return s

def read_img(file):
    return cv2.imread(file)

def write_img(file, img):
    cv2.imwrite(file, img)

def process_dir(input_dir, output_dir, desiredOutputs, numShapes):
    files = None
    try:
        files = os.listdir(input_dir)
    except RuntimeError:
        raise RuntimeError("cannot get listing for dir "+dir+" is this path even valid?")
    if not os.path.exists(output_dir):
        try:
            os.mkdir(output_dir)
        except RuntimeError:
            raise RuntimeError("output dir doesn't exist, and was not able to be created (do its parents exist?)")
    if not os.path.isdir(output_dir):
        raise RuntimeError("output dir is not a directory")
    if len(os.listdir(output_dir)) != 0:
        raise RuntimeError("output dir is not empty, will not proceed")
    numFailed = 0
    numSucceeded = 0
    outputNum = 0
    variationsPerImage = int(math.ceil(desiredOutputs/len(files)))
    for file in files:
        try:
            img = read_img(file)
            write_img("/var/www/html/output/field0.jpg", img)
            for i in range(variationsPerImage):
                img_copy = np.copy(img)
                overlay_img(img_copy, numShapes, outputNum)
                write_img(os.path.join(output_dir,left_pad(str(outputNum), 8, "0")+".jpg"), img_copy)
                outputNum += 1
            numSucceeded += 1
        except RuntimeError:
            numFailed += 1
            print("failed to process "+file)
    return (numSucceeded, numFailed)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python3 generate_dataset.py input_dir/ output_dir/')
        sys.exit(-1)
    input_dir = os.path.abspath(sys.argv[1])
    output_dir = os.path.abspath(sys.argv[2])
    succ, fail = process_dir(input_dir, output_dir, desiredOutputs, numShapes)
    print("Successfully processed "+str(succ)+"/"+str(succ+failed)+" images")
