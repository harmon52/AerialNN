import random
picture_width = 3840
picture_height = 2160


def coordinate_generator(width, height): 

	x1 = random.randint(1, picture_width)
	y1 = random.randint(1, picture_height)
	
	x2 = random.randint(1, picture_width)
	while x2 < x1-width and x1+width < x2:
		x2 = random.randint(1, picture_width)
	
	x3 = random.randint(1, picture_width)
	while x3 < x1-width and x1+width < x3:
		x3 = random.randint(1, picture_width)
	
	y2 = random.randint(1, picture_height)
	while y2 < y1-height and y1+height < y:
		x2 = random.randint(1, picture_height)
	
	y3 = random.randint(1, picture_height)
	while y3 < y1-height and y1+height <y3:
		y3 = random.randint(1, picture_height)

	return (x1,y1,x2,y2,x3,y3)

def main():
	
	(x1,y1,x2,y2,x3,y3) = coordinate_generator(200, 300)
	
