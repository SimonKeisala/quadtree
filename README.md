# N-Tree implementation in python (N-dimensional quadtree)

The implementation allows bounding-box N-tree indexing with fast
queries for objects in the tree.

The Tree class contains two functions, "insert" and "intersect" (querying).
The implementation is inspired by pyqtree, with slight improvement in performance for large region queries, with minimum performance loss for small sized queries.

The following shows benchmarking results between this implementation and other existing python libraries. The obvious steps in the insertion is due to python garbage collector and being unable to de-allocate data manually:

![Insertion speed. Description: The new implementation either match or surpasses any alternative](/python/images/insertion_benchmarking.png)

And Intersection speed:

![Intersection speed. Description: The new implementation is close to on par with pyqtree for small region queries, but surpasses the pyqtree library when regions get larger](/python/images/intersect_benchmarking_full.png)

![Intersection speed. Description: The new implementation is close to on par with pyqtree for small region queries, but surpasses the pyqtree library when regions get larger](/python/images/intersect_benchmarking_zoom.png)
