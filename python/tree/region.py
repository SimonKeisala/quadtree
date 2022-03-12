import numpy
from numbers import Number


class CenterPointInvalidType(Exception):
    def __init__(self):
        super().__init__("Center point contains one or more invalid values")


class RegionInvalid(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def shape_check(size, dimensions):
    size = numpy.atleast_1d(size).flatten()
    if not all(isinstance(x, Number) for x in size):
        raise RegionInvalid("Not all elements in shape is a number")
    if any(x <= 0 for x in size):
        raise RegionInvalid("Shape dimension size must be non-zero")
    elif len(size) == 1:
        return numpy.repeat(size,dimensions)
    elif len(size) == dimensions:
        return size
    else:
        raise RegionInvalid("Missmatching size and dimensions. Size must be either 1 or dimensions")


class Region:
    """Region definition of """
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

        self.shape = shape_check(shape, self.dimensions)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (
                "center:" + str(self.center) +
                ", shape:" + str(self.shape) +
                ", dimensions:" + str(self.dimensions)
        )

    def overlap_point(self, point):
        try:
            return (
                    len(numpy.atleast_1d(point)) == self.dimensions and
                    numpy.max(
                        numpy.subtract(
                            numpy.abs(
                                numpy.subtract(numpy.atleast_1d(point), self.center)),
                            self.shape)
                    ) <= 0
            )
        except:  # noqa: Ignore any exception
            return False

    def overlap_circle(self, point, r):
        try:
            return (
                    len(numpy.atleast_1d(point)) == self.dimensions and
                    numpy.max(
                        numpy.subtract(
                            numpy.abs(
                                numpy.subtract(numpy.atleast_1d(point), self.center)),
                            self.shape)
                    ) <= r
            )
        except:  # noqa: Ignore any exception
            return False

    def overlap_region(self, center, shape):
        try:
            shape = shape_check(shape, self.dimensions)
            return (
                    len(numpy.atleast_1d(center)) == self.dimensions and
                    len(numpy.atleast_1d(shape)) == self.dimensions and
                    numpy.max(
                        numpy.subtract(
                            numpy.subtract(
                                numpy.abs(
                                    numpy.subtract(center, self.center)
                                ), self.shape),
                            shape)
                    ) <= 0)
        except:  # noqa: Ignore any exception
            return False

    def __eq__(self, other):
        return self.dimensions == other.dimensions and \
               numpy.allclose(self.center, other.center) and \
               numpy.allclose(self.shape, other.shape)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        # Lower dimensions is smaller
        if self.dimensions != other.dimensions:
            return self.dimensions < other.dimensions
        if self.dimensions == 1:
            return self.center < other.center
        for i in range(self.dimensions):
            if self.center[i] != other.center[i]:
                return self.center[i] < other.center[i]
        return False

    def __gt__(self, other):
        return other.__lt__(self)

    def __le__(self, other):
        return not other.__lt__(self)

    def __ge__(self, other):
        return not self.__lt__(other)
