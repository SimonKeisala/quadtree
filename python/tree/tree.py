import abc
from typing import Tuple
from .quadtree import Quadtree
from .octree import Octree
from .ntree import NTree


class Tree(abc.ABC):
    """
    Class for storing points in a region and for quick querying of the points in the tree.

    What's included:
      * A general class able to store points with corresponding data
      * Simple querying of a rectangular region

    How to use:
      1. Start by creating a Tree object:
            tree = tree.Tree((0, 0, 512, 512))

      2. Populate the tree with data points:
            tree.insert(enemy, (-50, -50, -40, -40))
            tree.insert(enemyBase, (-40, -50, -10, -20))
            ...
            tree.insert(player, (90, 90, 110, 110))

      3. Query data points from the tree:
          # Query all objects within 100 units in a circle around the
          # player
          query = tree.intersect((player.x-100, player.y-100, player.x+100, player.y+100))
          for obj, point in query:
              <do things>

    Note:
    There is currently no way to remove items from the tree,
    so it has to be recreated each time an object moves or is deleted.

    Hint:
    To speed up the queries, separate static objects and dynamic
    objects into two trees and perform a query on both trees.
    """

    def __new__(cls, bbox: Tuple[float, ...], capacity: int = 10, max_depth: int = 20):
        """
        Creates a Tree object which can perform inserts and perform query for points inside the Tree.

            Note:
                Quadtree (2D) and Octree (3D) trees have sped up specialized implementations.
                Use any of them if possible.

        Args:
            bbox: Tree bounding box.
                  Must be a multiple of two, can be any N dimensions otherwise
            capacity: Capacity of each branch (default: 10)
            max_depth: Maximum depth until tree stops splitting into new regions
        """
        assert len(bbox) % 2 == 0
        # Special sped-up implementations for Quadtree (2D) and Octree (3D) trees.
        if len(bbox) == 4:
            return Quadtree(bbox, capacity, max_depth)
        if len(bbox) == 6:
            return Octree(bbox, capacity, max_depth)
        return NTree(bbox, capacity, max_depth)

    @abc.abstractmethod
    def insert(self, data, bbox):
        """
        Insert a point into the quadtree.

        Args:
            data:  Data to connect to this bounding box
            bbox:  Tuple with same dimension as the tree
        Returns:
            True if bounding box is inside the quadtree region, False otherwise

        example: insert(myObject, (0.1, 0.5, 0.1, 0.5))
        """

    @abc.abstractmethod
    def intersect(self, bbox: Tuple[float, ...]):
        """
        Creates a generator query of a rectangular region within the quadtree.

        Args:
            bbox: tuple of intersection bounding box

        Returns:
            A generator object corresponding to the query
        """
