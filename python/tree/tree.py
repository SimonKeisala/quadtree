import numpy
from typing import Tuple

from tree.region import Region


def shape(size, dimensions):
    size = numpy.atleast_1d(size)
    if len(size) == 1:
        return numpy.repeat(size, dimensions)
    return size


class Tree:
    """ Class for storing points in a region and for quick querying of the points in the tree.

        What's included:
          * A general class able to store points with corresponding data
          * Simple querying of regions within the object.
             Region types:
               - Circular regions
               - Rectangular regions

        How to use:
          1. Start by creating a Tree object:
                tree = quadtree.Tree(center=(0,0), size=256, \
                                     [capacity=10])
               (NOTE: capacity is optional)

          2. Populate the tree with data points:
                tree.insert(enemy, (-50, -50))
                tree.insert(enemyBase, (-40, -50))
                ...
                tree.insert(player, (100, 100))

          3. Query data points from the tree:
              # Query all objects within 100 units in a circle around the
              # player
              query = tree.query_circle(player.x, player.y, 100)
              for obj, point in query:
                  <do things>

        Note that the tree have to be recreated each time an object move.
        To speed up the queries, separate static objects and dynamic
        objects into two trees and perform a query on both trees.
    """

    def __init__(self, center: Tuple[float, ...] = (0, 0), size: float = 256, capacity: int = 10):
        """Creates a Tree object which can perform inserts and perform query for points inside the Tree.

          :param center: Center point of the qtree area
          :param size: Size of area (distance in each direction both
                       positive and negative)
          :param capacity: Capacity of each sub-tree (default: 10)
        """
        self._size = size
        self._capacity = capacity
        self._dimensions = len(center)
        self.region = Region(center, shape(self._size, self._dimensions))
        self.parent = None
        self.children = None
        self.points = []

    def insert(self, obj, point):
        """Insert a point into the quadtree.

        :param obj:    linked object to this point
        :param point:  Tuple with same dimension as the tree
        :return: True if point was successfully inserted. False otherwise

        example: insert((0.1, 0.5), myObject)
        """
        # Check if point actually is in region
        if not self.region.point_inside(point):
            return False
        self._insert(obj, point)
        return True

    def _insert(self, obj, point):
        # Check if current region have space for new point
        if self.children:
            self._get_child(point)._insert(obj, point)
        else:
            if len(self.points) == self._capacity:
                self._create_children()
                for i, p in self.points:
                    self._get_child(p)._insert(i, p)
                self.points = []
                self._get_child(point)._insert(obj, point)
            else:
                self.points.append((obj, numpy.atleast_1d(point)))

    def intersect(self, center, rect):
        """Creates a generator query of a rectangular region within the quadtree.

        :param center: tuple of center point in tree
        :param rect: rectangle to extract
        :return: generator object corresponding to the query
        """
        center = numpy.atleast_1d(center)
        rect = shape(rect, self._dimensions)
        yield from self._query_rect(center, rect)

    def _query_rect(self, center, rect):
        if self.region.intersects(center, rect):
            if self.region.contains(center, rect):
                yield from self
            else:
                if self.children:
                    for c in self.children:
                        yield from c._query_rect(center, rect)
                else:
                    for obj, pt in self.points:
                        if not any(numpy.abs(center-pt)-rect > 0):
                            yield obj

    def __iter__(self):
        """Iterates through all the objects in the quadtree."""
        if self.children:
            for c in self.children:
                yield from c
        else:
            for obj, _ in self.points:
                yield obj

    def _get_child(self, point) -> "Tree":
        index = 0
        for i in range(len(self.region.center)):
            if self.region.center[i] < point[i]:
                index += 2**i
        return self.children[index]

    def _create_children(self):
        size2 = self._size / 2
        size4 = self.region.shape / 4
        polarity = 2 ** numpy.arange(self._dimensions)
        self.children = []
        for i in range(2 ** self._dimensions):
            mult = (i // polarity % 2) * 2 - 1
            center = self.region.center + size4 * mult
            child = Tree(center, size2)
            child.parent = self
            self.children.append(child)
