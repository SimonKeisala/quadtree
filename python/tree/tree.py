import numpy
from typing import Tuple

from tree.region import Region, shape_check


class Tree:
    """ Class for storing points in a region and for quick query of the points in the tree.

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
        self._size = abs(size)
        self._capacity = capacity
        self.region = Region(center, self._size)
        self.parent = None
        self.children = None
        self.points = []
        self.totalPoints = 0

    def insert(self, obj, point):
        """Insert a point into the quadtree.

        :param obj:    linked object to this point
        :param point:  Tuple with same dimension as the tree
        :return: True if point was successfully inserted. False otherwise

        example: insert((0.1, 0.5), myObject)
        """
        # Check if point actually is in region
        if not self.region.overlap_point(point):
            return False
        return self._insert(obj, point)

    def _insert(self, obj, point):
        # If it is in region it should fit in the root or one child
        self.totalPoints += 1

        # Check if current region have space for new point
        if len(self.points) < self._capacity:
            self.points.append((obj, numpy.atleast_1d(point)))
            return True

        # Otherwise get the child branch where point should fit in:
        child = self._get_child(point)
        return child._insert(obj, point)

    def query_circle(self, point, r):
        """Creates a generator query of a circular region within the quadtree.

        :param point: tuple of point in tree
        :param r:     radius of circle
        :return: Generator object corresponding to the query
        """
        r2 = r*r
        point = numpy.atleast_1d(point)
        if self.region.overlap_circle(point, r):
            for obj, pt in self.points:
                if numpy.sum((point-pt)**2) < r2:
                    yield obj, pt
            if self.children:
                for c in self.children:
                    yield from c.query_circle(point, r)

    def query_rect(self, point, rect):
        """Creates a generator query of a rectangular region within the quadtree.

        :param point: tuple of point in tree
        :param rect: rectangle to extract
        :return: generator object corresponding to the query
        """
        point = numpy.atleast_1d(point)
        rect = shape_check(rect, self.region.dimensions)
        if self.region.overlap_region(point, rect):
            for obj, pt in self.points:
                if numpy.max(numpy.abs(point-pt)-rect) < 0:
                    yield obj, pt
            for c in self.children:
                yield from c.query_rect(point, rect)

    def __iter__(self):
        """Iterates through all the objects in the quadtree."""
        for obj, pt in self.points:
            yield obj, pt
        for c in self.children:
            yield from c

    def _get_child(self, point) -> "Tree":
        """
        Internal function that queries the matching child region.
        If the child regions has not yet been created it firsts create all the child regions.
        """
        if not self.children:
            half_size = self.region.shape / 2
            polarity = 2**numpy.arange(self.region.dimensions)
            self.children = []
            for i in range(2 ** self.region.dimensions):
                mult = (i // polarity % 2) * 2 - 1
                center = self.region.center+half_size*mult
                child = Tree(center, half_size)
                child.parent = self
                self.children.append(child)
            self.range = 2**numpy.arange(2)

        index = 0
        for i in range(len(self.region.center)):
            if self.region.center[i] < point[i]:
                index += 2**i
        return self.children[index]
