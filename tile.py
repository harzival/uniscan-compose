

class Tile:
    def __init__(self, box, pos):
        self.box = box
        self.geom_box = None
        self.pos = pos
        self.child_list = []
        self.lod_dir_name = None
        self.geom_error = None

    def __iter__(self):
        yield ("boundingVolume", dict(self.geom_box))
        yield ("geometricError", self.geom_error)
        yield ("content", {"uri": self.get_uri()})
        yield ("extras", {"name": self.get_name()})
        if len(self.child_list) > 0:
            yield ("children", [dict(tile) for tile in self.child_list])

    def dict(self):
        return dict(self)

    def get_name(self):
        return str(self.pos.x) + "_" + str(self.pos.y) + "_" + str(self.pos.z)

    def get_obj_name(self):
        return self.get_name() + ".obj"

    def get_glb_name(self):
        return self.get_name() + ".glb"

    def get_b3dm_name(self):
        return self.get_name() + ".b3dm"

    def get_albedo_map_name(self):
        return self.get_name() + "_albedo.jpg"

    def get_normal_map_name(self):
        return self.get_name() + "_normal.jpg"

    def get_uri(self):
        return (self.lod_dir_name + "/" + self.get_b3dm_name())


class RootTile (Tile):
    def __init__(self, box, child_list, geom_error, transform):
        super().__init__(box, None)
        self.child_list = child_list
        self.lod_dir_name = None
        self.geom_error = geom_error
        self.transform = transform

    def __iter__(self):
        yield ("transform", self.transform)
        yield ("boundingVolume", dict(self.box))
        yield ("refine", "REFINE")
        yield ("geometricError", self.geom_error)
        yield ("children", [dict(tile) for tile in self.child_list])

    def dict(self):
        return dict(self)


class Tileset:
    def __init__(self, version, error, root_tile):
        self.version = version
        self.error = error
        self.root_tile = root_tile

    def __iter__(self):
        yield ("asset", {"version": self.version})
        yield ("geometricError", self.error)
        yield ("root", dict(self.root_tile))

    def dict(self):
        return dict(self)
