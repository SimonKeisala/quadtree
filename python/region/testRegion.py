#!/usr/bin/env python3
import unittest
import numpy

from . import region

class TestRegionCreation(unittest.TestCase):
    def setUp(self):
        pass

    def test_all_invalid(self):
        self.assertRaises(Exception, region.Region, (), None)

    def test_no_center(self):
        self.assertRaises(region.CenterPointInvalidType, region.Region, (), 5)

    def test_no_shape(self):
        self.assertRaises(region.RegionSizeInvalid, region.Region, (5), None)

    def test_shape_negative(self):
        self.assertRaises(region.RegionSizeInvalid, region.Region, (5), -5)
        self.assertRaises(region.RegionSizeInvalid, region.Region, (5), -0.01)

    def test_shape_zero(self):
        region.Region( (5), 0)

    def test_region_invalid_type(self):
        self.assertRaises(region.CenterPointInvalidType, region.Region, "hej", 4)

    def test_region_partial_invalid_type(self):
        self.assertRaises(region.CenterPointInvalidType, region.Region, (1,"hej"), 4)

    def test_shape_invalid_type(self):
        self.assertRaises(region.RegionSizeInvalid, region.Region, (5), "hej")

    def test_shape_single_dimension_valid_values(self):
        a = region.Region((3), 5)
        self.assertEqual(a.dimensions, 1)
        #self.assertEqual(a.shape, 5)
        self.assertTrue(numpy.allclose(a.shape, 5))
        self.assertEqual(a.center, 3)


    def test_shape_two_dimension_valid_values(self):
        a = region.Region((3,9), 5)
        self.assertEqual(a.dimensions, 2)
        self.assertTrue(numpy.allclose(a.shape, 5))
        #self.assertEqual(a.shape, 5)
        self.assertTrue(numpy.allclose(a.center, (3,9)))


    def test_shape_three_dimension_valid_values(self):
        a = region.Region((3,9,6), 5)
        self.assertEqual(a.dimensions, 3)
        self.assertTrue(numpy.allclose(a.shape, 5))
        #self.assertEqual(a.shape, 5)
        self.assertTrue(numpy.allclose(a.center, (3,9,6)))


class TestRegionComparisons(unittest.TestCase):
    def setUp(self):
        self.d1a = region.Region((1),4)
        self.d1b = region.Region((1),4)
        self.d1c = region.Region((2),4)
        self.d1d = region.Region((2),3)

        self.d2a = region.Region((1,1),4)
        self.d2b = region.Region((1,1),4)
        self.d2c = region.Region((1,2),4)
        self.d2d = region.Region((2,1),4)
        self.d2e = region.Region((2,2),4)

        self.d3a = region.Region((0,0,0),4)
        pass


    def test_one_dimension(self):
        self.assertTrue(self.d1a != self.d1c)
        self.assertTrue(self.d1b != self.d1c)

        self.assertTrue(self.d1a < self.d1c)
        self.assertTrue(self.d1a <= self.d1c)

        self.assertTrue(self.d1c > self.d1a)
        self.assertTrue(self.d1c >= self.d1a)

        self.assertTrue(self.d1a == self.d1b)
        self.assertTrue(self.d1a <= self.d1b)
        self.assertTrue(self.d1a >= self.d1b)

        self.assertTrue(self.d1c != self.d1d)
        self.assertTrue(self.d1c <= self.d1d)
        self.assertTrue(self.d1c >= self.d1d)


        self.assertFalse(self.d1a > self.d1c)
        self.assertFalse(self.d1a >= self.d1c)

        self.assertFalse(self.d1c < self.d1a)
        self.assertFalse(self.d1c <= self.d1a)

        self.assertFalse(self.d1a != self.d1b)
        self.assertFalse(self.d1a < self.d1b)
        self.assertFalse(self.d1a > self.d1b)

        self.assertFalse(self.d1c == self.d1d)
        self.assertFalse(self.d1c < self.d1d)
        self.assertFalse(self.d1c > self.d1d)



    def test_two_dimensions(self):
        self.assertTrue(self.d2a == self.d2b)
        self.assertTrue(self.d2a != self.d2c)
        self.assertTrue(self.d2a != self.d2d)
        self.assertTrue(self.d2a != self.d2e)
        self.assertTrue(self.d2c != self.d2d)
        self.assertTrue(self.d2c != self.d2e)
        self.assertTrue(self.d2d != self.d2e)

        self.assertFalse(self.d2a != self.d2b)
        self.assertFalse(self.d2a == self.d2c)
        self.assertFalse(self.d2a == self.d2d)
        self.assertFalse(self.d2a == self.d2e)
        self.assertFalse(self.d2c == self.d2d)
        self.assertFalse(self.d2c == self.d2e)
        self.assertFalse(self.d2d == self.d2e)

        self.assertTrue(self.d2a <= self.d2b)
        self.assertTrue(self.d2a >= self.d2b)
        self.assertTrue(self.d2a < self.d2c)
        self.assertTrue(self.d2a <= self.d2c)
        self.assertTrue(self.d2a < self.d2d)
        self.assertTrue(self.d2a <= self.d2d)
        self.assertTrue(self.d2a < self.d2e)
        self.assertTrue(self.d2a <= self.d2e)

        self.assertFalse(self.d2a < self.d2b)
        self.assertFalse(self.d2a > self.d2b)
        self.assertFalse(self.d2a > self.d2c)
        self.assertFalse(self.d2a >= self.d2c)
        self.assertFalse(self.d2a > self.d2d)
        self.assertFalse(self.d2a >= self.d2d)
        self.assertFalse(self.d2a > self.d2e)
        self.assertFalse(self.d2a >= self.d2e)

        self.assertTrue(self.d2c > self.d2b)
        self.assertTrue(self.d2c >= self.d2b)
        self.assertTrue(self.d2c < self.d2d)
        self.assertTrue(self.d2c <= self.d2d)
        self.assertTrue(self.d2c < self.d2e)
        self.assertTrue(self.d2c <= self.d2e)

        self.assertFalse(self.d2c < self.d2b)
        self.assertFalse(self.d2c <= self.d2b)
        self.assertFalse(self.d2c > self.d2d)
        self.assertFalse(self.d2c >= self.d2d)
        self.assertFalse(self.d2c > self.d2e)
        self.assertFalse(self.d2c >= self.d2e)

        self.assertTrue(self.d2d > self.d2b)
        self.assertTrue(self.d2d >= self.d2b)
        self.assertTrue(self.d2d > self.d2c)
        self.assertTrue(self.d2d >= self.d2c)
        self.assertTrue(self.d2d < self.d2e)
        self.assertTrue(self.d2d <= self.d2e)

        self.assertFalse(self.d2d < self.d2b)
        self.assertFalse(self.d2d <= self.d2b)
        self.assertFalse(self.d2d < self.d2c)
        self.assertFalse(self.d2d <= self.d2c)
        self.assertFalse(self.d2d > self.d2e)
        self.assertFalse(self.d2d >= self.d2e)

        self.assertTrue(self.d2e > self.d2b)
        self.assertTrue(self.d2e >= self.d2b)
        self.assertTrue(self.d2e > self.d2c)
        self.assertTrue(self.d2e >= self.d2c)
        self.assertTrue(self.d2e > self.d2d)
        self.assertTrue(self.d2e >= self.d2d)

        self.assertFalse(self.d2e < self.d2b)
        self.assertFalse(self.d2e <= self.d2b)
        self.assertFalse(self.d2e < self.d2c)
        self.assertFalse(self.d2e <= self.d2c)
        self.assertFalse(self.d2e < self.d2d)
        self.assertFalse(self.d2e <= self.d2d)

    def test_cross_dimensions(self):
        self.assertTrue(self.d1a != self.d2a)
        self.assertTrue(self.d1a != self.d3a)
        self.assertTrue(self.d2a != self.d3a)

        self.assertFalse(self.d1a == self.d2a)
        self.assertFalse(self.d1a == self.d3a)
        self.assertFalse(self.d2a == self.d3a)


        self.assertTrue(self.d1a < self.d2a)
        self.assertTrue(self.d1a <= self.d2a)
        self.assertTrue(self.d1c < self.d2a)
        self.assertTrue(self.d1c <= self.d2a)
        self.assertTrue(self.d1c < self.d3a)
        self.assertTrue(self.d1c <= self.d3a)
        self.assertTrue(self.d2e < self.d3a)
        self.assertTrue(self.d2e <= self.d3a)

        self.assertTrue(self.d2a > self.d1a)
        self.assertTrue(self.d2a >= self.d1a)
        self.assertTrue(self.d2a > self.d1c)
        self.assertTrue(self.d2a >= self.d1c)
        self.assertTrue(self.d3a > self.d1c)
        self.assertTrue(self.d3a >= self.d1c)
        self.assertTrue(self.d3a > self.d2e)
        self.assertTrue(self.d3a >= self.d2e)


        self.assertFalse(self.d1a > self.d2a)
        self.assertFalse(self.d1a >= self.d2a)
        self.assertFalse(self.d1c > self.d2a)
        self.assertFalse(self.d1c >= self.d2a)
        self.assertFalse(self.d1c > self.d3a)
        self.assertFalse(self.d1c >= self.d3a)
        self.assertFalse(self.d2e > self.d3a)
        self.assertFalse(self.d2e >= self.d3a)

        self.assertFalse(self.d2a < self.d1a)
        self.assertFalse(self.d2a <= self.d1a)
        self.assertFalse(self.d2a < self.d1c)
        self.assertFalse(self.d2a <= self.d1c)
        self.assertFalse(self.d3a < self.d1c)
        self.assertFalse(self.d3a <= self.d1c)
        self.assertFalse(self.d3a < self.d2e)
        self.assertFalse(self.d3a <= self.d2e)

class TestRegionFunctions(unittest.TestCase):
    def setUp(self):
        self.region = region.Region(4, 5)
        self.region2 = region.Region((4,7), 4)
        pass

    def test_repr(self):
        repr(self.region)
        pass

    def test_string(self):
        str(self.region)
        pass

    def test_overlap_point_invalid(self):
        self.assertFalse(self.region.overlapPoint(()))
        self.assertFalse(self.region.overlapPoint((2,2)))
        self.assertFalse(self.region.overlapPoint((None)))
        pass
    def test_overlap_point_valid(self):
        self.assertTrue(self.region.overlapPoint((0)))
        self.assertFalse(self.region.overlapPoint((10)))
        self.assertFalse(self.region.overlapPoint((-10)))
        pass

    def test_overlap_region_invalid(self):
        self.assertFalse(self.region.overlapRegion((), []))
        self.assertFalse(self.region.overlapRegion((2,2), ()))
        self.assertFalse(self.region.overlapRegion((None), ()))
        self.assertFalse(self.region2.overlapRegion((), []))
        self.assertFalse(self.region2.overlapRegion((2,2), ()))
        self.assertFalse(self.region2.overlapRegion((None), ()))
        pass

    def test_overlap_region_valid(self):
        self.assertTrue(self.region.overlapRegion((0), 1))
        self.assertFalse(self.region.overlapRegion((11), 1))
        self.assertFalse(self.region.overlapRegion((-11), 1))
        self.assertTrue(self.region2.overlapRegion((0, 8), 1))
        self.assertTrue(self.region2.overlapRegion((7, 0), (1,3)))
        self.assertFalse(self.region2.overlapRegion((11, 5), 1))
        self.assertFalse(self.region2.overlapRegion((-11, 5), 1))
        pass

