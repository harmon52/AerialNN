import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image
import shutil # for deleting files
import os  # for making directories

import genPolygon as gp

    
TRAINING_IMGS = 24 # number of training images to generate
VALIDATION_IMGS = 16 # number of validation images to generate
NUM_SHAPE_TYPES = 2 # number of possible shapes to try
IMG_SIZE = 252 # height and width of image

def getShape(choice): # modify this as you see fit
    if shapeChoice == 0: # SQUARE
        shape = gp.regular_polygon
        args = [int(IMG_SIZE/2), 4]
        label = "square"
    elif shapeChoice == 1: # CIRCLE
        shape = gp.circle
        args = [int(IMG_SIZE*3/8)]
        label = "circle"
    elif shapeChoice == 2: # STAR
        shape = gp.star
        args = [int(IMG_SIZE/2), 5]
        label = "star"

    else:
        print('NO VALID SHAPE CHOSEN')
    return shape, args, label

if __name__ == '__main__':
    
    shutil.rmtree('trainingShapes', ignore_errors=True)
    shutil.rmtree('validationShapes', ignore_errors=True)
    
    shapenames = 'square', 'circle','star'
    f = open('labels.txt', 'w')
    
    for x in range(NUM_SHAPE_TYPES):
        if not os.path.exists('trainingShapes/'+shapenames[x]+'/'):
            os.makedirs('trainingShapes/'+shapenames[x]+'/')
        if not os.path.exists('validationShapes/'+shapenames[x]+'/'):
            os.makedirs('validationShapes/'+shapenames[x]+'/')
        f.write(shapenames[x]+"\n")
        
    f.close()
    
    for x in range(TRAINING_IMGS):
        data = np.zeros((IMG_SIZE, IMG_SIZE, 3), dtype=np.uint8)

        angle = random.randint(0, 360)
        shapeChoice = random.randint(0, NUM_SHAPE_TYPES-1)
        shape, args, label = getShape(shapeChoice)       
        
        gp.place_obj(data, (int(IMG_SIZE/2), int(IMG_SIZE/2)), angle,
          shape, args, (255, 255, 255),
          '', 0, 0)
        
        img = Image.fromarray(data, 'RGB')
        img.save('trainingShapes/'+ label +'/image' + str(x) + '.jpg')
        #img.show()
    for x in range(VALIDATION_IMGS):
        data = np.zeros((IMG_SIZE, IMG_SIZE, 3), dtype=np.uint8)

        angle = random.randint(0, 360)
        shapeChoice = random.randint(0, NUM_SHAPE_TYPES-1)
        shape, args, label = getShape(shapeChoice)       
        
        gp.place_obj(data, (int(IMG_SIZE/2), int(IMG_SIZE/2)), angle,
          shape, args, (255, 255, 255),
          '', 0, 0)
        
        img = Image.fromarray(data, 'RGB')
        img.save('validationShapes/'+ label +'/image' + str(x) + '.jpg')
    
