#!/usr/bin/env python3
import math

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
#            tree = quadtree.Tree(left=-256, right=256, \
#                                 top=256, bottom=256, \
#                                 [capacity=C], [branchingFactor=B] \
#                                )
#          capacity and branchingFactor are optional
#
#      2. Populate the tree with data points:
#            tree.insert((-50, -50, enemy))
#            tree.insert((-40, -50, enemyBase))
#            ...
#            tree.insert((100, 100, player))
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


class Tree:
    #######################################################
    # constructor:
    #    Creates a Tree object which can perform inserts and do
    #        queries of points inside the Tree.
    #
    #       Inputs:
    #         top:    top boundary of tree region
    #         right:  right boundary of tree region
    #         bottom: bottom boundary of tree region
    #         left:   left boundary of tree region
    #         capacity: capacity of each sub-tree (default: 10)
    #         branchingFactor: how many branches the tree divides
    #                            into, must be a power of two
    #
    #      Note: The values top-bottom and left-right
    #              must be whole powers of two, (this can be bypassed,
    #              though that can result in rounding error with the
    #              consequence of missing a child tree).
    #
    def __init__(self, top, right, bottom, left, capacity=10, branchingFactor=2, checkPower=True):
        self.children = []
        self.__capacity = capacity

        # See if the dimensions should check of being power of two.
        #   This is to make sure child regions have nice numbers
        if checkPower:
            lr = left-right
            tb = top-bottom
            if lr != __powerOfTwo(lr):
                raise Exception("x-dimension is not power of two", lr, "vs", __powerOfTwo(lr))
            if tb != __powerOfTwo(tb):
                raise Exception("y-dimension is not power of two", tb, "vs", __powerOfTwo(tb))

        self.rectangle = Tree.__Rectangle( \
                              left   = min(left,right), \
                              right  = max(left,right), \
                              bottom = min(bottom, top), \
                              top    = max(bottom, top))
        self.points = []
        self.totalPoints = 0
        # Set branching factor to 2 or higher
        self.__branchingFactor = max(2,int(branchingFactor))
        # Find nearest power of two of value
        self.__branchingFactor = 2**math.floor(math.log(self.__branchingFactor,2))

    #######################################################
    # insert:
    #    Insert a point into the quadtree.
    #       Inputs:
    #         point: Tuple with an x-position, y-position and custom
    #                  data.
    #                  example: insert((0.1, 0.5, myObject))
    #
    #       Returns:
    #         True if point was successfully inserted
    #         False otherwise
    def insert(self, point):
        # Check if point actually is in region
        if not self.rectangle.overlapPoint(point):
            return False

        # If it is in region it should fit in the root or one child
        self.totalPoints +=1
        curr = self
        while True:
            # Check if current region have space for new point
            if len(curr.points) < curr.__capacity:
                curr.points.append(point)
                return True
            # Otherwise get the child where point should fit in:
            curr = curr.__querychild(point)

    #######################################################
    # queryCircle:
    #    Creates a query of a circular region within the quadtree
    #       Inputs:
    #         x: center point in x-direction
    #         y: center point in y-direction
    #         r: radius of circle
    #
    #       Returns:
    #         Query object with the following function calls:
    #          next(): returns next object in query, None if no other
    #                    object exists
    #          all():  returns an array of all remaining objects which
    #                    matches the query
    def queryCircle(self, x, y, r):
        return Tree.__Query(self, Tree.__circleRule(x,y,r))

    #######################################################
    # queryRect:
    #    Create a query of a rectangular region within the quadtree
    #       Inputs:
    #         top:    top boundary of query region
    #         right:  right boundary of query region
    #         bottom: bottom boundary of query region
    #         left:   left boundary of query region
    #
    #       Returns:
    #         Query object with the following function calls:
    #          next(): returns next object in query, None if no other
    #                    object exists
    #          all():  returns an array of all remaining objects which
    #                    matches the query
    def queryRect(self, top, right, bottom, left):
        return Tree.__Query(self, \
                Tree.__rectRule( \
                    Tree.__Rectangle(left   = left, \
                                     right  = right, \
                                     top    = top, \
                                     bottom = bottom)))

    ######################################################
    # Print the tree -- Used for debugging
    #
    def print(self, depth=-1):
        self.__print(depth, 0)
    def __print(self, depth, indentation):
        print(" "*indentation + str(self.rectangle), "points:", len(self.points))
        depth -= 1
        if depth is not 0:
            self.children.sort()
            for child in self.children:
                child.__print(depth,indentation+2)

    def __eq__(self, other):
        return self.rectangle == other.rectangle

    def __lt__(self, other):
        return self.rectangle < other.rectangle

    #
    # End of debugging functions
    ######################################################




    ######################################################
    #
    # Internal classes and functions, not instantiated by the user
    #
    ######################################################
    # Internal function to query the matching child region
    # or to create a new child region if it does not exist
    def __querychild(self, point):

        # First see if any of the existing child is a match
        for child in self.children:
            if child.rectangle.overlapPoint(point):
                return child

        # If no match was found, create a new child object that match
        # the region.
        # Width and height is reduced by the branching factor
        w = (self.rectangle.right-self.rectangle.left)/self.__branchingFactor
        h = (self.rectangle.top-self.rectangle.bottom)/self.__branchingFactor
        # Find which region the point belong to
        xSteps = min(math.floor((point[0]-self.rectangle.left)/w), self.__branchingFactor-1)
        ySteps = min(math.floor((point[1]-self.rectangle.bottom)/h), self.__branchingFactor-1)

        # Create the new child node
        left   = self.rectangle.left + xSteps*w
        bottom = self.rectangle.bottom + ySteps*h

        # No need to check if child tree is a power of two. The root
        # tree itself should be a power of two
        child = Tree(left   = left,   right = left   + w, \
                     bottom = bottom, top   = bottom + h, \
                     capacity = self.__capacity, \
                     branchingFactor = self.__branchingFactor,\
                     checkPower = False)
        self.children.append(child)
        return child


    # Class to handle the rule of a circular query
    class __circleRule:
        def __init__(self, x, y, r):
            self.__x = float(x)
            self.__y = float(y)
            self.__r = float(r)

        def validPoint(self, point):
            dx = point[0] - self.__x
            dy = point[1] - self.__y
            return dx*dx+dy*dy <= self.__r*self.__r

        def validRegion(self, region):
            dX = min(0,self.__x - region.rectangle.left)   + max(0,self.__x - region.rectangle.right)
            dY = min(0,self.__y - region.rectangle.bottom) + max(0,self.__y - region.rectangle.top)
            return dX*dX + dY*dY < self.__r*self.__r

    # Class to handle the rule of a rectangular query
    class __rectRule:
        def __init__(self, rectangle):
            self.__rectangle = rectangle

        def validPoint(self, point):
            return self.__rectangle.overlapPoint(point)

        def validRegion(self, region):
            return self.__rectangle.overlapRectangle(region.rectangle)

    # Class of rectangle representation
    class __Rectangle:
        def __init__(self, top, right, bottom, left):
            self.top    = float(top)
            self.right  = float(right)
            self.bottom = float(bottom)
            self.left   = float(left)

        def __repr__(self):
            return self.__str__()
        def __str__(self):
            return "[l:" + str(self.left) + ", r:" + str(self.right) + ", t:" + str(self.top) + ", b:" + str(self.bottom) + "]"

        def overlapPoint(self, point):
            return point[0] >= self.left   and \
                   point[0] <= self.right  and \
                   point[1] >= self.bottom and \
                   point[1] <= self.top

        def overlapRectangle(self, rectangle):
            return rectangle.right  >= self.left   and \
                   rectangle.left   <= self.right  and \
                   rectangle.top    >= self.bottom and \
                   rectangle.bottom <= self.top

        def __eq__(self, other):
            return self.left == other.left and \
                   self.right == other.right and \
                   self.top == other.top and \
                   self.bottom == other.bottom

        def __lt__(self, other):
            return self.left < other.left or \
                ( self.left == other.left and \
                  self.bottom < other.bottom )

    # Class of a query object, returned when calling queryCircle or
    # queryRect
    class __Query:
        def __init__(self, region, rule):
            self.__regions = [region]
            self.__rule = rule
            self.__index = 0
            self.__regions_checked = 0
            self.__points_checked = 0
            self.__matching_points = 0
            self.__total_points = region.totalPoints;

        # Query next item from tree
        def next(self):
            while len(self.__regions) > 0:
                while self.__index < len(self.__regions[0].points):
                    # Get point in current region and move to next index
                    point = self.__regions[0].points[self.__index]
                    self.__index += 1
                    self.__points_checked += 1

                    # Check if point is valid and return if it is
                    if self.__rule.validPoint(point):
                        self.__matching_points += 1
                        return point
                # Check if region is subdivided and for each region check
                # if they should be added
                for region in self.__regions[0].children:
                    if self.__rule.validRegion(region):
                        self.__regions.append(region)
                self.__regions.pop(0)
                self.__regions_checked += 1
                self.__index = 0
            return None

        # Returns a list of all objects matching the given query. If
        # the objects are processed one at a time it is faster to run
        # next() instead of all()
        def all(self):
            result = []
            item = self.next()
            while (item is not None):
                result.append(item)
                item = self.next()
            return result

        # Lists some summary of the current query
        def summary(self):
            print("Regions checked:", self.__regions_checked)
            print("Points checked:", self.__points_checked)
            print("matching points:", self.__matching_points)
            print("Total points:", self.__total_points)
            print("Percentage checked: %.2f" % (float(self.__points_checked)/float(self.__total_points)))
            print("Percentage matching: %.2f" % (float(self.__matching_points)/float(self.__points_checked)))


# Helper function to get the nearest power of two (rounded down) from a given value
def __powerOfTwo(val):
    # check if zero
    if val == 0:
        return 0

    # Get sign of value
    sign = 1
    if val < 0:
        sign = -1
        val = -val

    # Find nearest power of 2
    val = 2**math.floor(math.log(val,2))
    return sign*val

