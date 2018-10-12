import numpy as np
import matplotlib.pyplot as plt
import random

import genPolygon as gp

img = np.zeros((64, 64, 3), dtype=np.uint8)

angle = random.randint(0, 360)
#shape = random.choice(gp.regular_polygon) doesn't seem to work
shapeChoice = random.randint(0, 2)
if shapeChoice == 0: # SQUARE
    shape = gp.regular_polygon
    args = [32, 4]
elif shapeChoice == 1: # STAR
    shape = gp.star
    args = [32, 5]
elif shapeChoice == 2: # CIRCLE
    shape = gp.circle
    args = [24]

gp.place_obj(img, (32, 32), angle,
          shape, args, (255, 255, 255),
          '', 0, 0)


plt.subplot(122)
plt.title('Using place_obj function')
plt.imshow(img)
# plt.savefig('demo.png')
plt.show()
