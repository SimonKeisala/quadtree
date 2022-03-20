from typing import Tuple, Optional, List


class Octree:
    def __init__(self,
                 bbox: Tuple[float, float, float, float, float, float],
                 capacity: int = 10, max_depth=20):
        self._capacity = capacity
        self.bbox = bbox
        self.center = ((bbox[3] - bbox[0]) / 2 + bbox[0],
                       (bbox[4] - bbox[1]) / 2 + bbox[1],
                       (bbox[5] - bbox[2]) / 2 + bbox[2])
        self.parent = None
        self.children: Optional[List["Octree"]] = None
        self.points = []
        self.depth = 0
        self._max_depth = max_depth

    def insert(self, item, bbox: Tuple[float, float, float, float, float, float]):
        if not self._rect_overlap(self.bbox, bbox):
            return False
        self._insert(item, bbox)

    def intersect(self, bbox):
        """Creates a generator query of a rectangular region within the quadtree.

        :param bbox: Intersection bounding box
        :return: generator object corresponding to the query
        """
        if self._rect_overlap(self.bbox, bbox):
            yield from self._query_rect(bbox, set())

    def __iter__(self):
        """Iterator to return all objects in this Quadtree node or all children."""
        self._iter(set())

    def _iter(self, uniq: set):
        if self.children:
            for c in self.children:
                yield from c._iter(uniq)
            for obj, _ in self.points:
                obj_id = id(obj)
                if obj_id not in uniq:
                    uniq.add(obj_id)
                    yield obj
        else:
            for obj, _ in self.points:
                obj_id = id(obj)
                if obj_id not in uniq:
                    uniq.add(obj_id)
                    yield obj

    def _query_rect(self, bbox, uniq: set):
        # If the queried bounding box contains entire quad we can start iterating without any checks
        # all items should in this case match
        if self._rect_contains(bbox, self.bbox):
            yield from self._iter(uniq)
        else:
            if self.children:
                if bbox[0] <= self.center[0]:
                    if bbox[1] <= self.center[1]:
                        if bbox[2] <= self.center[2]:
                            yield from self.children[0]._query_rect(bbox, uniq)
                        if bbox[5] >= self.center[2]:
                            yield from self.children[1]._query_rect(bbox, uniq)
                    if bbox[4] >= self.center[1]:
                        if bbox[2] <= self.center[2]:
                            yield from self.children[2]._query_rect(bbox, uniq)
                        if bbox[5] >= self.center[2]:
                            yield from self.children[3]._query_rect(bbox, uniq)
                if bbox[3] >= self.center[0]:
                    if bbox[1] <= self.center[1]:
                        if bbox[2] <= self.center[2]:
                            yield from self.children[4]._query_rect(bbox, uniq)
                        if bbox[5] >= self.center[2]:
                            yield from self.children[5]._query_rect(bbox, uniq)
                    if bbox[4] >= self.center[1]:
                        if bbox[2] <= self.center[2]:
                            yield from self.children[6]._query_rect(bbox, uniq)
                        if bbox[5] >= self.center[2]:
                            yield from self.children[7]._query_rect(bbox, uniq)
            for obj, pt in self.points:
                obj_id = id(obj)
                if obj_id not in uniq and self._rect_overlap(bbox, pt):
                    uniq.add(obj_id)
                    yield obj

    def _insert(self, item, bbox: Tuple[float, float, float, float]):
        if self.children:
            self._insert_to_children(item, bbox)
        else:
            if self.depth != self._max_depth and len(self.points) == self._capacity:
                self._create_children()
                points = self.points
                self.points = []
                for i, p in points:
                    self._insert_to_children(i, p)
                self._insert_to_children(item, bbox)
            else:
                self.points.append((item,bbox))

    def _insert_to_children(self, item, rect: Tuple[float, float, float, float]):
        if (
                rect[0] <= self.center[0] <= rect[3] and
                rect[1] <= self.center[1] <= rect[4] and
                rect[2] <= self.center[2] <= rect[5]
        ):
            self.points.append((item, rect))
        else:
            if rect[0] <= self.center[0]:
                if rect[1] <= self.center[1]:
                    if rect[2] <= self.center[2]:
                        self.children[0]._insert(item, rect)
                    if rect[5] >= self.center[2]:
                        self.children[1]._insert(item, rect)
                if rect[4] >= self.center[1]:
                    if rect[2] <= self.center[2]:
                        self.children[2]._insert(item, rect)
                    if rect[5] >= self.center[2]:
                        self.children[3]._insert(item, rect)
            if rect[3] >= self.center[0]:
                if rect[1] <= self.center[1]:
                    if rect[2] <= self.center[2]:
                        self.children[4]._insert(item, rect)
                    if rect[5] >= self.center[2]:
                        self.children[5]._insert(item, rect)
                if rect[4] >= self.center[1]:
                    if rect[2] <= self.center[2]:
                        self.children[6]._insert(item, rect)
                    if rect[5] >= self.center[2]:
                        self.children[7]._insert(item, rect)

    def _create_children(self):
        self.children = [
            Octree((self.bbox[0],   self.bbox[1],   self.bbox[2],
                    self.center[0], self.center[1], self.center[2]), self._capacity, self._max_depth),
            Octree((self.bbox[0],   self.bbox[1],   self.center[2],
                    self.center[0], self.center[1], self.bbox[5]), self._capacity, self._max_depth),
            Octree((self.bbox[0],   self.center[1], self.bbox[2],
                    self.center[0], self.bbox[4],   self.center[2]), self._capacity, self._max_depth),
            Octree((self.bbox[0],   self.center[1], self.center[2],
                    self.center[0], self.bbox[4],   self.bbox[5]), self._capacity, self._max_depth),
            Octree((self.center[0], self.bbox[1],   self.bbox[2],
                    self.bbox[3],   self.center[1], self.center[2]), self._capacity, self._max_depth),
            Octree((self.center[0], self.bbox[1],   self.center[2],
                    self.bbox[3],   self.center[1], self.bbox[5]), self._capacity, self._max_depth),
            Octree((self.center[0], self.center[1], self.bbox[2],
                    self.bbox[3],   self.bbox[4],   self.center[2]), self._capacity, self._max_depth),
            Octree((self.center[0], self.center[1], self.center[2],
                    self.bbox[3],   self.bbox[4],   self.bbox[5]), self._capacity, self._max_depth),
        ]
        for child in self.children:
            child.depth = self.depth + 1
            child.parent = self

    @staticmethod
    def _is_point_inside(bbox, point):
        return (bbox[0] <= point[0] <= bbox[3] and
                bbox[1] <= point[1] <= bbox[4] and
                bbox[2] <= point[2] <= bbox[5])

    @staticmethod
    def _rect_overlap(bbox1, bbox2):
        return (bbox1[0] <= bbox2[3] and
                bbox1[1] <= bbox2[4] and
                bbox1[2] <= bbox2[5] and
                bbox1[3] >= bbox2[0] and
                bbox1[4] >= bbox2[1] and
                bbox1[5] >= bbox2[2])

    @staticmethod
    def _rect_contains(bbox1, bbox2):
        return (bbox1[0] <= bbox2[0] and
                bbox1[1] <= bbox2[1] and
                bbox1[2] <= bbox2[2] and
                bbox1[3] >= bbox2[3] and
                bbox1[4] >= bbox2[4] and
                bbox1[5] >= bbox2[5])
