import numpy


class Region:
    """Region definition of """
    def __init__(self, center, shape):
        self.center = numpy.atleast_1d(center)
        self.shape = shape
        self._half_shape = shape/2

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return (
                "center:" + str(self.center) +
                ", shape:" + str(self.shape)
        )

    def intersects(self, center, half_shape):
        return not any(numpy.abs(center - self.center) - self._half_shape > half_shape)

    def contains(self, center, half_shape):
        return not any(numpy.abs(center - self.center) + self._half_shape > half_shape)

    def point_inside(self, point):
        return not any(numpy.abs(point - self.center) - self._half_shape > 0)
