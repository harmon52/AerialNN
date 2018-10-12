import numpy as np
import matplotlib.pyplot as plt
import random
from PIL import Image
import shutil # for deleting files
import os  # for making directories

import genPolygon as gp

def getShape(choice):
    if shapeChoice == 0: # SQUARE
        shape = gp.regular_polygon
        args = [32, 4]
        label = "square"
    elif shapeChoice == 1: # STAR
        shape = gp.star
        args = [32, 5]
        label = "star"
    elif shapeChoice == 2: # CIRCLE
        shape = gp.circle
        args = [24]
        label = "circle"
    else:
        print('NO VALID SHAPE CHOSEN')
    return shape, args, label




if __name__ == '__main__':
    
    shutil.rmtree('trainingShapes', ignore_errors=True)
    shutil.rmtree('validationShapes', ignore_errors=True)
    
    shapenames = 'square', 'circle','star'
    f = open('labels.txt', 'w')
    
    for x in shapenames:
        if not os.path.exists('trainingShapes/'+x+'/'):
            os.makedirs('trainingShapes/'+x+'/')
        if not os.path.exists('validationShapes/'+x+'/'):
            os.makedirs('validationShapes/'+x+'/')
        f.write(x+"\n")
        
    f.close()
    
    TRAINING_IMGS = 10 # number of training images to generate
    VALIDATION_IMGS = 2 # number of validation images to generate
    
    for x in range(TRAINING_IMGS):
        data = np.zeros((64, 64, 3), dtype=np.uint8)

        angle = random.randint(0, 360)
        shapeChoice = random.randint(0, 2)
        shape, args, label = getShape(shapeChoice)       
        
        gp.place_obj(data, (32, 32), angle,
          shape, args, (255, 255, 255),
          '', 0, 0)
        
        img = Image.fromarray(data, 'RGB')
        img.save('trainingShapes/'+ label +'/image' + str(x) + '.jpg')
        #img.show()
    for x in range(VALIDATION_IMGS):
        data = np.zeros((64, 64, 3), dtype=np.uint8)

        angle = random.randint(0, 360)
        shapeChoice = random.randint(0, 2)
        shape, args, label = getShape(shapeChoice)       
        
        gp.place_obj(data, (32, 32), angle,
          shape, args, (255, 255, 255),
          '', 0, 0)
        
        img = Image.fromarray(data, 'RGB')
        img.save('validationShapes/'+ label +'/image' + str(x) + '.jpg')
    