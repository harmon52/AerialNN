import numpy as np
import cv2

import matplotlib.pyplot as plt

import imgmask_utils as imutil


def regular_polygon(img, loc, radius, nedges, angle, color):
    obj = np.zeros_like(img, dtype=np.uint8)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)

    loc = np.array(loc)
    angle = angle*np.pi/180
    thetas = np.linspace(0, 2 * np.pi, nedges, endpoint=False) + angle

    pts = np.cos(thetas), np.sin(thetas)
    pts = (radius * np.array(pts).T + loc).astype(np.int32)

    cv2.fillPoly(mask, [pts], 1)
    mask = mask.astype(np.bool)
    obj[mask] = color
    return obj, mask.astype(np.bool)


def star(img, loc, radius, npoints, angle, color):
    obj = np.zeros_like(img, dtype=np.uint8)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)

    loc = np.array(loc)
    angle = angle*np.pi/180
    inner_thetas = np.linspace(0, 2*np.pi, npoints, endpoint=False) + angle
    thetas = inner_thetas - np.pi/npoints  # half phase shift

    # did some math
    inner_r = radius * np.cos(2*np.pi/npoints) / np.cos(np.pi/npoints)

    pts = np.cos(thetas), np.sin(thetas)
    pts = (radius * np.array(pts).T + loc)

    inner_pts = np.cos(inner_thetas), np.sin(inner_thetas)
    inner_pts = (inner_r * np.array(inner_pts).T + loc)

    # Fortran order interleaves the points.
    pts_tot = np.array([pts, inner_pts]).reshape(-1, 2, order='F').astype(np.int32)
    cv2.fillPoly(mask, [pts_tot], 1)
    mask = mask.astype(np.bool)
    obj[mask] = color
    return obj, mask.astype(np.bool)


def circle(img, loc, radius, angle, color):
    obj = np.zeros_like(img, dtype=np.uint8)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    cv2.circle(mask, loc, radius, 1, -1)
    mask = mask.astype(np.bool)
    obj[mask] = color
    return obj, mask.astype(np.bool)


def half_circle(img, loc, radius, angle, color):
    obj = np.zeros_like(img, dtype=np.uint8)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)

    shift = np.sin(angle*np.pi/180), np.cos(angle*np.pi/180)
    shift = 4*radius/(3*np.pi) * np.array(shift)
    loc = tuple(loc+shift.astype(np.int32))

    cv2.ellipse(mask, loc, (radius, radius), 180-angle, 0, 180, 1, -1)
    mask = mask.astype(np.bool)
    obj[mask] = color
    return obj, mask.astype(np.bool)


def quarter_circle(img, loc, radius, angle, color):
    obj = np.zeros_like(img, dtype=np.uint8)
    mask = np.zeros(img.shape[:2], dtype=np.uint8)

    shift = np.sin(angle*np.pi/180), np.cos(angle*np.pi/180)
    shift = np.sqrt(32) * radius / (3 * np.pi) * np.array(shift)
    loc = tuple(loc + shift.astype(np.int32))

    cv2.ellipse(mask, loc, (radius, radius), 180-angle, 45, 135, 1, -1)
    mask = mask.astype(np.bool)
    obj[mask] = color
    return obj, mask


def cross(img, loc, tot_w, arm_width, angle, color):
    obj = np.zeros_like(img, np.uint8)
    mask = np.zeros(img.shape[:2], np.uint8)

    rect1 = [[-tot_w / 2, -arm_width / 2],
             [-tot_w / 2, arm_width / 2],
             [tot_w / 2, arm_width / 2],
             [tot_w / 2, -arm_width / 2]]
    rect1 = np.array(rect1)

    angle = angle*np.pi/180
    rot = np.array([[np.cos(angle), -np.sin(angle)],
                    [np.sin(angle), np.cos(angle)]])

    r1 = (np.matmul(rect1, rot) + loc).astype(np.int32)
    r2 = (np.matmul(rect1[...,::-1], rot) + loc).astype(np.int32)

    cv2.fillPoly(obj, [r1], color)
    cv2.fillPoly(obj, [r2], color)
    cv2.fillPoly(mask, [r1], 1)
    cv2.fillPoly(mask, [r2], 1)

    return obj, mask.astype(np.bool)


def put_text(obj, loc, font_scale, char, angle ,color):
    if char == '': return

    font = cv2.FONT_HERSHEY_SIMPLEX
    thick = int(font_scale*2)
    (w, h), bl = cv2.getTextSize(char, font, font_scale, thick)

    text = np.zeros(obj.shape[:2], dtype=np.uint8)

    txtloc = loc[0]-w//2, loc[1] + (h-bl)//2
    cv2.putText(text, char, txtloc, font, font_scale, 1, thick, cv2.LINE_AA)

    rot = cv2.getRotationMatrix2D(loc, angle, 1.0)

    text = cv2.warpAffine(text, rot, obj.shape[:2][::-1])

    obj[text.astype(np.bool)] = color

    # plt.imshow(text)
    # plt.show()

    # text = np.zeros((w, h, 3), dtype=np.uint8)
    # cv2.putText(text, char, (0, h-bl//2), font, font_scale, color, thick, cv2.LINE_AA)


def place_obj(img, loc, angle,
              obj_type, args, obj_color,
              char, text_size, text_color):
    """
    :param img:         Image to place onto
    :param loc:         Where to put it
    :param angle:       What orientation it's at
    :param obj_type:    function that generates an object
    :param args:        List of params that define the object.
    :param obj_color:   Object color
    :param char:        Text to put
    :param text_size:   Size of text
    :param text_color:  Color of text
    :return:
    """
    obj, mask = obj_type(img, loc, *args, angle, obj_color)
    put_text(obj, loc, text_size, char, angle, text_color)

    imutil.apply_blur_mask(img, obj, mask, ksize=4)
    imutil.apply_noise_mask(img, mask, sigma=12)

    return mask


if __name__ == '__main__':
    img = np.ones((400, 350, 3), dtype=np.uint8)

    place_obj(img, (255, 255), 155,
              regular_polygon, [30, 4], (255, 0, 0),
              'a', 1.2, (255, 255, 255))
    place_obj(img, (100, 200), 45,
              star, [45, 5], (0, 255, 0),
              't', 1.2, (255, 0, 255))
    place_obj(img, (50, 50), 210,
              half_circle, [30], (0, 0, 255),
              'd', 1.2, (255, 0, 255))
    place_obj(img, (50, 350), -30,
              quarter_circle, [50], (255, 0, 255),
              'L', 1.2, (255,255,255))
    place_obj(img, (200, 150), 75,
              cross, [50, 20], (0,255,255),
              'm', 1, (255,0,255))

    obj1, mask1 = regular_polygon(img, (255, 255), 30, 4, 155, (255, 0, 0))
    put_text(obj1, (255, 255), 1.2, 'a', 155, (255,255,255))
    obj2, mask2 = star(img, (100, 200), 45, 5, 45, (0,255,0))
    put_text(obj2, (100, 200), 1.2, 't', 45, (255,0,255))
    obj3, mask3 = half_circle(img, (50, 50), 30, 210, (0,0,255))
    obj4, mask4 = quarter_circle(img, (50, 350), 50, -30, (255,0,255))
    put_text(obj4, (50, 350), 1.2, 'L', -30, (255,255,255))
    obj5, mask5 = cross(img, (200, 150), 50, 20, 75, (0,255,255))

    plt.subplot(121)
    plt.title('Using raw functions')
    plt.imshow(obj1 + obj2 + obj3 + obj4 + obj5)
    # plt.imshow(mask1 | mask2 | mask3 | mask4 | mask5)

    plt.subplot(122)
    plt.title('Using place_obj function')
    plt.imshow(img)
    # plt.savefig('demo.png')
    plt.show()
