import numpy as np
import pylab as plt


class Shapes(object):
    def __init__(self, gridsize):
        self.gridsize = gridsize
        self.grid = np.zeros((gridsize, gridsize))

    def connect(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        r = self.gridsize / 2
        xs = np.round(np.arange(x1, x2, float(x2 - x1) / r)).astype(int) if x2 != x1 else np.array([x2] * int(r))
        ys = np.round(np.arange(y1, y2, float(y2 - y1) / r)).astype(int) if y2 != y1 else np.array([y2] * int(r))
        for x, y in zip(xs.tolist(), ys.tolist()):
            self.grid[x, y] = 1

    def reg_polygon(self, sides):
        theta = np.arange(0, 2 * np.pi, 2 * np.pi / sides)
        r = self.gridsize / 2
        for r0 in np.arange(r-1, r, 1).tolist():
            xs = np.round(r0 * np.cos(theta) + r).astype(int) - 1
            ys = np.round(r0 * np.sin(theta) + r).astype(int) - 1
            xy = list(zip(xs.tolist(), ys.tolist()))
            for i in range(len(xy)):
                p1 = xy[i - 1]
                p2 = xy[i]
                self.grid[p2[0], p2[1]] = 1
                self.connect(p1, p2)
        return self.grid

    def star(self):
        theta = np.arange(0, (18 / 5) * np.pi, 4 * np.pi / 5)
        r = self.gridsize / 2
        for r0 in np.arange(r - int(r / 10), r, 1).tolist():
            xs = np.round(r0 * np.cos(theta) + r).astype(int) - 1
            ys = np.round(r0 * np.sin(theta) + r).astype(int) - 1
            xy = list(zip(xs.tolist(), ys.tolist()))
            for i in range(len(xy)):
                p1 = xy[i - 1]
                p2 = xy[i]
                self.grid[p2[0], p2[1]] = 1
                self.connect(p1, p2)
        return self.grid


if __name__ == '__main__':
    hexagon = Shapes(200).reg_polygon(7)
    plt.imshow(hexagon, cmap='Greys')
    plt.show()
