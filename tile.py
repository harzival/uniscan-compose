

class Tile:
    def __init__(self, box, pos):
        self.box = box
        self.pos = pos
        self.child_list = []
        self.geom_error = None

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

# class RootTile (Tile):
#    def __init__(self, box, pos, child_list, )
