import numpy
from typing import Tuple, Optional, List


class NTree:
    def __init__(self, bbox: Tuple[float, ...], capacity: int = 10, max_depth: int = 20):
        self._capacity = capacity
        self._max_depth = max_depth
        self.bbox = numpy.array(bbox)
        self.bbox = self.bbox.reshape(2, self.bbox.size // 2)
        self.center = self.bbox.sum(axis=0) / 2
        self.children: Optional[List["NTree"]] = None
        self.points = []
        self.depth = 0

    def insert(self, data, bbox):
        bbox = numpy.array(bbox).reshape(self.bbox.shape)
        if not self._rect_overlap(self.bbox, bbox):
            return False
        self._insert(data, bbox)

    def intersect(self, bbox: Tuple[float, ...]):
        bbox = numpy.array(bbox).reshape(self.bbox.shape)
        yield from self._query_rect(bbox, set())

    def __iter__(self):
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

    def _query_rect(self, bbox, uniq: set):
        # If the queried bounding box contains entire quad we can start iterating without any checks
        # all items should in this case match
        if self._rect_contains(bbox, self.bbox):
            yield from self._iter(uniq)
        else:
            if self.children:
                for child in self.children:
                    if child._rect_overlap(child.bbox, bbox):
                        yield from child._query_rect(bbox, uniq)
            for obj, obj_bbox in self.points:
                obj_id = id(obj)
                if obj_id not in uniq and self._rect_overlap(bbox, obj_bbox):
                    uniq.add(obj_id)
                    yield obj

    def _insert(self, data, bbox: Tuple[float, float, float, float]):
        if self.children:
            self._insert_to_children(data, bbox)
        else:
            if self.depth != self._max_depth and len(self.points) == self._capacity:
                self._create_children()
                points = self.points
                self.points = []
                for i, p in points:
                    self._insert_to_children(i, p)
                self._insert_to_children(data, bbox)
            else:
                self.points.append((data, bbox))

    def _insert_to_children(self, data, bbox):
        if all(bbox[0] <= self.center) and all(self.center <= bbox[1]):
            # Point overlap with all children
            self.points.append((data, bbox))
        else:
            for child in self.children:
                if child._rect_overlap(child.bbox, bbox):
                    child._insert(data, bbox)

    @staticmethod
    def _rect_overlap(bbox1, bbox2):
        return (
                all(bbox1[0] <= bbox2[1]) and
                all(bbox1[1] >= bbox2[0])
        )

    @staticmethod
    def _rect_contains(bbox1, bbox2):
        return (
                all(bbox1[0] <= bbox2[0]) and
                all(bbox1[1] >= bbox2[1])
        )

    def _create_children(self):
        size2 = self.bbox[1] - self.center
        polarity = 2 ** numpy.arange(self.bbox.shape[1])
        self.children = []
        for i in range(2 ** self.bbox.shape[1]):
            mult = (i // polarity % 2)
            top_left = self.bbox[0]+mult*size2
            bbox = numpy.array([top_left, top_left + size2])
            child = NTree(bbox, capacity=self._capacity, max_depth=self._max_depth)
            child.depth = self.depth + 1
            self.children.append(child)
