from collections import namedtuple
from vec3 import Vec3
from tile import Tile


class Box:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def is_inside(self, other):
        if self.min >= other.min and self.max <= other.max:
            return True
        else:
            return False

    def slice_into_tiles(self, slices):
        def slice_1d(min, max, slices):
            slice_len = (max - min) / slices
            return [
                [min + (slice * slice_len), min + (slice + 1) * slice_len]
                for slice in range(slices)
            ]
        return [
            Tile(
                Box(Vec3(x[0], y[0], z[0]), Vec3(x[1], y[1], z[1])),
                Vec3(ix, iy, iz),
            )
            for ix, x in enumerate(slice_1d(self.min.x, self.max.x, slices.x))
            for iy, y in enumerate(slice_1d(self.min.y, self.max.y, slices.y))
            for iz, z in enumerate(slice_1d(self.min.z, self.max.z, slices.z))
        ]

    @classmethod
    def from_joining_box_list(cls, box_list):
        min = Vec3(0, 0, 0)
        max = Vec3(0, 0, 0)
        for i, box in enumerate(box_list):
            if i == 0:
                min = box.min
                max = box.max
            else:
                if box.max.x > max.x:
                    max.x = box.max.x
                if box.max.y > max.y:
                    max.y = box.max.y
                if box.max.z > max.z:
                    max.z = box.max.z
                if box.min.x < min.x:
                    min.x = box.min.x
                if box.min.y < min.y:
                    min.y = box.min.y
                if box.min.z < min.z:
                    min.z = box.min.z
        return cls(min, max)

    @classmethod
    def from_obj_geometry(cls, obj_path):
        Point = namedtuple("Point", ["x", "y", "z"])
        min = Vec3(0, 0, 0)
        max = Vec3(0, 0, 0)
        vertex_count = 0
        for line in open(obj_path, "r"):
            if line[:2] == "v ":
                vertex_values = line[2:].rstrip("\n").split(" ")
                vertex = Point(
                    float(vertex_values[0]),
                    float(vertex_values[1]),
                    float(vertex_values[2]),
                )
                vertex_count += 1
                if vertex_count == 1:
                    min = Vec3(vertex.x, vertex.y, vertex.z)
                    max = Vec3(vertex.x, vertex.y, vertex.z)
                else:
                    if vertex.x > max.x:
                        max.x = vertex.x
                    if vertex.y > max.y:
                        max.y = vertex.y
                    if vertex.z > max.z:
                        max.z = vertex.z
                    if vertex.x < min.x:
                        min.x = vertex.x
                    if vertex.y < min.y:
                        min.y = vertex.y
                    if vertex.z < min.z:
                        min.z = vertex.z
        return cls(min, max)
