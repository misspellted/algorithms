import math

def twoPoints2f(ax, ay, bx, by):
    return math.sqrt(math.pow(math.fabs(bx - ax), 2) + math.pow(math.fabs(by - ay), 2))

def midPoint2f(ax, ay, bx, by):
    return ((float(ax) + float(bx)) / float(2), (float(ay) + float(by)) / float(2))

def extendLineTo2f(ax, ay, bx, by, length):
    ratio = float(length) / twoPoints2f(ax, ay, bx, by)
    ex = ax + math.fabs(bx - ax) * ratio
    ey = ay + math.fabs(by - ay) * ratio
    return (ex, ey)

