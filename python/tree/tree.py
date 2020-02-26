#######################################################
#
#   Class for storing points in a region and for quick query of the
#   points in the tree.
#
#    What's included:
#      * A general class able to store points with corresponding data
#      * Simple querying of regions within the object.
#         Region types:
#           - Circular regions
#           - Rectangular regions
#
#    How to use:
#      1. Start by creating a Tree object:
#            tree = quadtree.Tree(center=(0,0), size=256, \
#                                 [capacity=10])
#           (NOTE: capacity is optional)
#
#      2. Populate the tree with data points:
#            tree.insert(enemy, (-50, -50))
#            tree.insert(enemyBase, (-40, -50))
#            ...
#            tree.insert(player, (100, 100))
#
#      3. Query data points from the tree:
#          # Query all objects within 100 units in a circle around the
#          # player
#          query = tree.queryCircle(player.x, player.y, 100)
#          next = query.next()
#          while next != None:
#              obj = next[2]
#              <do things>
#              next = query.next()
#
#      alternative method of querying objects:
#          # Query all objects within 100 units in a circle around the
#          # player
#          query = tree.queryCircle(player.x, player.y, 100)
#          for (x, y, obj) in query.all():
#              <do things>
#
#     Note that the tree have to be recreated each time an object
#     move.
#     To speed up the queries, separate static objects and dynamic
#     objects into two trees and perform a query on both trees.

from region.region import Region, shapeCheck
import numpy

class Tree:
    #######################################################
    # constructor:
    #    Creates a Tree object which can perform inserts and do
    #        queries of points inside the Tree.
    #
    #       Inputs:
    #         center: center point of the qtree area
    #         size: size of area (distance in each direction both
    #         positive and negative)
    #         capacity: capacity of each sub-tree (default: 10)
    def __init__(self, center = (0,0), size=256, capacity=10):
        self.parent = None
        self.children = []
        self.__size = abs(size)
        self.region = Region(center, self.__size)
        self.__capacity = capacity


        self.points = []
        self.totalPoints = 0

    #######################################################
    # insert:
    #    Insert a point into the quadtree.
    #       Inputs:
    #         obj:   linked object to this point
    #         point: Tuple with same dimension as the tree
    #       example: insert((0.1, 0.5), myObject)
    #
    #       Returns:
    #         True if point was successfully inserted
    #         False otherwise
    def insert(self, obj, point):
        # Check if point actually is in region
        if not self.region.overlapPoint(point):
            return False

        # If it is in region it should fit in the root or one child
        self.totalPoints +=1

        # Check if current region have space for new point
        if len(self.points) < self.__capacity:
            self.points.append((numpy.atleast_1d(point), obj))
            return True

        # Otherwise get the child branch where point should fit in:
        child = self.__getchild(point)
        child.parent = self
        return child.insert(obj,point)


    #######################################################
    # queryCircle:
    #    Creates a generator query of a circular region within the quadtree
    #       Inputs:
    #         point: tuple of point in tree
    #         r: radius of circle
    #
    #       Returns:
    #         generator object corresponding to the query
    def queryCircle(self, point, r):
        point = numpy.atleast_1d(point)
        if self.region.overlapPoint(point):
            for (p, o) in self.points:
                if numpy.sqrt(numpy.sum((point-p)**2)) < r:
                #if numpy.max(numpy.abs(point-p)) < r:
                    yield (p,o)
            for c in self.children:
                yield from c.queryCircle(point,r)


    #######################################################
    # queryRect:
    #    Creates a generator query of a circular region within the quadtree
    #       Inputs:
    #         point: tuple of point in tree
    #         r: radius of circle
    #
    #       Returns:
    #         generator object corresponding to the query
    def queryRect(self, point, rect):
        point = numpy.atleast_1d(point)
        rect = shapeCheck(rect, self.region.dimensions)
        if self.region.overlapPoint(point):
            for (p, o) in self.points:
                if numpy.max(numpy.abs(point-p)-rect) < 0:
                    yield (p,o)
            for c in self.children:
                yield from c.queryRect(point,rect)

    ######################################################
    #
    # Internal classes and functions, not instantiated by the user
    #
    ######################################################
    # Internal function to query the matching child region
    # or to create a new child region if it does not exist
    def __getchild(self, point):

        # First see if any of the existing child is a match
        for child in self.children:
            if child.region.overlapPoint(point):
                return child

        signs = numpy.sign(point-self.region.center)
        signs[signs == 0] = 1
        childCenter = self.region.center+(signs*self.__size/2)

        child = Tree(childCenter, self.__size/2)
        self.children.append(child)
        return child
