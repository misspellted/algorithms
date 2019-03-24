from geographic.distance import *
from iterated.pi import *
from math import sqrt
import unittest

class TestGeographicDistance(unittest.TestCase):
    def testTwoPoints2f(self):
        self.assertEqual(sqrt(2), twoPoints2f(0.0, 1.0, 1.0, 0.0))

    def testMidPoint2f(self):
        ex, ey = midPoint2f(0.0, 1.0, 1.0, 0.0)
        self.assertEqual(0.5, ex)
        self.assertEqual(0.5, ey)

    def testExtendLineTo2f(self):
        ex, ey = extendLineTo2f(0.0, 0.0, 1.0, 0.0, 2)
        self.assertEqual(float(2), ex)
        self.assertEqual(float(0), ey)

class TestSliceOfPi(unittest.TestCase):
    def testRadius(self):
        self.assertEqual(float(1), SliceOfPi(1).radius)

    def testPerform_negativeIterations(self):
        tested = SliceOfPi(1)

        with self.assertRaises(ValueError):
            tested.perform(-1)

    def testPerform_zeroIterations(self):
        tested = SliceOfPi(1)

        self.assertEqual(sqrt(2), tested.perform(0))

    def testPerform_positiveIterations(self):
        tested = SliceOfPi(1)

        self.assertNotEqual(sqrt(2), tested.perform(1))

class TestPiCalculation(unittest.TestCase):
    def testCalculatingPi(self):
        tested = SliceOfPi(1)

        iterations = 17

        halfPi = tested.perform(iterations)

        print(f"\nIterations: %d" % iterations)
        print(f"\nCalculated Value of Pi (SigFig=10): %.11f" % (halfPi * 2))

if __name__ == "__main__":
    unittest.main()
