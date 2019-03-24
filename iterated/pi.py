from collections import OrderedDict
from geographic.distance import midPoint2f, twoPoints2f, extendLineTo2f
from math import pow

def flattenPoint2f(point2f):
    return (point2f[0], point2f[1])

class SliceOfPi(object):
    def __init__(self, radius):
        self.radius = float(radius)
        self.origin = (0.0, 0.0)
        self.vertical = (0.0, self.radius)
        self.horizontal = (self.radius, 0.0)
        self.points = OrderedDict()
        self.lengths = OrderedDict()

    def applyIteration(self, iteration):
        if iteration == 0:
            ax, ay = flattenPoint2f(self.vertical)
            bx, by = flattenPoint2f(self.horizontal)

            self.points[0] = midPoint2f(ax, ay, bx, by)
            self.lengths[0] = twoPoints2f(ax, ay, bx, by)
        else:
            keyMidPoint = iteration << 1
            keyExtendLineTo = keyMidPoint - 1

            vx, vy = flattenPoint2f(self.vertical)

            if not keyExtendLineTo in self.points:
                ox, oy = flattenPoint2f(self.origin)
                px, py = flattenPoint2f(self.points[keyExtendLineTo - 1])
                self.points[keyExtendLineTo] = extendLineTo2f(ox, oy, px, py, self.radius)

            if not keyMidPoint in self.points:
                bx, by = flattenPoint2f(self.points[keyExtendLineTo])

                self.points[keyMidPoint] = midPoint2f(vx, vy, bx, by)

            ex, ey = flattenPoint2f(self.points[keyExtendLineTo])
            self.lengths[iteration] = twoPoints2f(vx, vy, ex, ey)

    def perform(self, iterations):
        if iterations < 0:
            raise ValueError("A zero or positive iterations count is required.")
        else:
            if not iterations in self.lengths:
                current = len(self.lengths)
                for iteration in range(iterations - current + 1):
                    self.applyIteration(current + iteration)

        return pow(2, iterations) * self.lengths[iterations]

    def recordToCsv(self):
        pass
