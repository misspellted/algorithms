import math
from collections import OrderedDict

from mpmath import *

def distanceBetweenPoints(pointA, pointB):
    ax, ay = pointA
    bx, by = pointB
    xDelta = fabs(mpf(ax) - mpf(bx))
    yDelta = fabs(mpf(ay) - mpf(by))
    return sqrt(power(xDelta, 2) + power(yDelta, 2))

def testDBP():
    pointA = (0, 1)
    pointB = (1, 0)
    d = distanceBetweenPoints(pointA, pointB)
    print str.format("dBP() quick test passed? {0}", d == sqrt(2))

def extendLineLengthBy(pointA, pointB, desired):
    current = distanceBetweenPoints(pointA, pointB)
    ax, ay = pointA
    bx, by = pointB
    xDelta = fabs(mpf(ax) - mpf(bx))
    yDelta = fabs(mpf(ay) - mpf(by))
    ratio = mpf(desired) / current
    xExt = bx + mpf(xDelta) * ratio
    yExt = by + mpf(yDelta) * ratio
    return (xExt, yExt)

def testELLB():
    pointA = (0, 0)
    pointB = (1, 0)
    cx, cy = extendLineLengthBy(pointA, pointB, 2)
    print str.format("eLLB() quick test passed? {0}", cx == mpf(3))

def extendLineLengthTo(pointA, pointB, desired):
    current = distanceBetweenPoints(pointA, pointB)
    ax, ay = pointA
    bx, by = pointB
    xDelta = fabs(mpf(ax) - mpf(bx))
    yDelta = fabs(mpf(ay) - mpf(by))
    ratio = mpf(desired) / current
    xExt = ax + mpf(xDelta) * ratio
    yExt = ay + mpf(yDelta) * ratio
    return (xExt, yExt)

def testELLT():
    pointA = (0, 0)
    pointB = (1, 0)
    cx, cy = extendLineLengthTo(pointA, pointB, 2)
    print str.format("eLLT() quick test passed? {0}", cx == mpf(2))

def midpoint(pointA, pointB):
    ax, ay = pointA
    bx, by = pointB
    xDelta = mpf(ax) + mpf(bx)
    yDelta = mpf(ay) + mpf(by)
    xMid = xDelta / 2
    yMid = yDelta / 2
    return (xMid, yMid)

def testMidpoint():
    pointA = (0, 1)
    pointB = (1, 0)
    cx, cy = midpoint(pointA, pointB)
    print str.format("midpoint() quick test passed? {0}", cx == mpf(0.5))
    print str.format("midpoint() quick test passed? {0}", cy == mpf(0.5))

class Pie:
    def __init__(this, radius):
        this._rds = radius
        this._orig = (0, 0)
        this._vert = (0, radius)
        this._horz = (radius, 0)
        this._pts = OrderedDict()
        this._lngths = OrderedDict()

    def getRadius(this):
        return this._rds

    def __buildIteration(this, iteration):
        if iteration == 0:
            this._pts[0] = midpoint(this._vert, this._horz)
            this._lngths[0] = distanceBetweenPoints(this._vert, this._horz)
        else:
            mpKey = iteration << 1
            elltKey = mpKey - 1
            if not elltKey in this._pts:
##                print str.format("Adding extension point for iteration {0}", iteration)
                this._pts[elltKey] = extendLineLengthTo(this._orig, this._pts[elltKey - 1], this._rds)
            if not mpKey in this._pts:
##                print str.format("Adding midpoint for iteration {0}", iteration)
                this._pts[mpKey] = midpoint(this._vert, this._pts[elltKey])
            this._lngths[iteration] = distanceBetweenPoints(this._vert, this._pts[elltKey])

    def checkDataPoints(this, iteration):
        if iteration < 0:
            raise ValueError("Cannot perform negative iterations!")
        else:
            if not iteration in this._lngths:
                current = len(this._lngths)
                missing = iteration - current + 1
                for itrtn in range(missing):
                    this.__buildIteration(current + itrtn)

    def approxQuarterCircumference(this, iteration):
        this.checkDataPoints(iteration)
##        print str.format("b-iteration length: {0}", this._lngths[iteration])
        return power(2, iteration) * this._lngths[iteration]

    def savePointsToCSV(this, path):
        if 0 < len(this._pts):
            with open(path, "w") as csv:
                x, y = this._orig
                csv.write(str.format("{0},{1}\n", x, y))
                x, y = this._vert
                csv.write(str.format("{0},{1}\n", x, y))
                x, y = this._horz
                csv.write(str.format("{0},{1}\n", x, y))
                for pt in this._pts.values():
                    x, y = pt
                    csv.write(str.format("{0},{1}\n", x, y))

def testPie(precision):
    mp.dps = precision + 1
    pi = Pie(1)
    aqc = pi.approxQuarterCircumference(10000)
    print str.format("C/4 ~ {0}", aqc)
    print str.format("C ~ {0}", aqc * 4)
    print str.format("C/2 ~ {0}", aqc * 2)
    print str.format("C/2*radius ~ {0}", aqc * 2 / pi.getRadius())
    
    #pi.savePointsToCSV("blah.csv")

def testAll(precision):
    testDBP()
    testELLB()
    testELLT()
    testMidpoint()
    testPie(precision)
