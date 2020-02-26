import numpy
from numbers import Number
# Exception types
class CenterPointInvalidType(Exception):
    def __init__(self):
        super().__init__( "Center point contains one or more invalid values")

class RegionSizeInvalid(Exception):
    def __init__(self):
        super().__init__("Region shape must be larger than zero")


def shapeCheck(data, size):
    data = numpy.atleast_1d(data).flatten()
    if not all(isinstance(x, Number) for x in data):
        raise RegionSizeInvalid()
    if any(x < 0 for x in data):
        raise RegionSizeInvalid()
    elif len(data) == 1:
        return numpy.array([data]*size)
    elif len(data) == size:
        return data
    else:
        raise RegionSizeInvalid()

# Class of Region representation
class Region:
    def __init__(self, center, shape):

        # Center check
        self.center = numpy.atleast_1d(center)
        for a in self.center:
            if not isinstance(a, Number):
                raise CenterPointInvalidType()

        # Dimension check
        self.dimensions = len(self.center)
        if self.dimensions == 0:
            raise CenterPointInvalidType()

        self.shape = shapeCheck(shape, self.dimensions)


    def __repr__(self):
        return self.__str__()
    def __str__(self):
        return "center:" + str(self.center) +\
               ", shape:" + str(self.shape) + \
               ", dimensions:" + str(self.dimensions)

    def overlapPoint(self, point):
        try:
            return len(numpy.atleast_1d(point)) == self.dimensions and \
                   numpy.max(
                           numpy.subtract( \
                               numpy.abs( \
                                   numpy.subtract(numpy.atleast_1d(point),self.center)), \
                               self.shape) \
                       ) <= 0
        except:
            return False

    def overlapRegion(self, center, shape):
        try:
            shape = shapeCheck(shape, self.dimensions)
            return len(numpy.atleast_1d(center)) == self.dimensions and \
                   len(numpy.atleast_1d(shape)) == self.dimensions and \
                   numpy.max(
                       numpy.subtract( \
                           numpy.subtract( \
                               numpy.abs(
                                   numpy.subtract(center,self.center) \
                                   ), self.shape), \
                           shape) \
                      ) <= 0
        except:
            return False

    # Comparisons of different types

    # Equals
    def __eq__(self, other):
        return self.dimensions == other.dimensions and \
               numpy.allclose(self.center, other.center) and \
               numpy.allclose(self.shape, other.shape)

    # Not equlas
    def __ne__(self, other):
        return not self.__eq__(other)

    # less than
    def __lt__(self, other):
        # Lower dimensions is smaller
        if (self.dimensions != other.dimensions):
            return self.dimensions < other.dimensions
        if self.dimensions == 1:
            return self.center < other.center
        for i in range(self.dimensions):
            if self.center[i] != other.center[i]:
                return self.center[i] < other.center[i]
        return False;

    # greater than
    def __gt__(self, other):
        return other.__lt__(self)

    # less than or equal
    def __le__(self, other):
        return not other.__lt__(self)

    # greater than or equal
    def __ge__(self, other):
        return not self.__lt__(other)


