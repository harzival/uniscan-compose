import json
from vec3 import Vec3
from box import Box


class Lod:
    def __init__(self, dir):
        self.dir = dir
        self.box = None
        self.slices = None
        self.tile_list = []
        self.parse_metadata(self.dir / "metadata.json")

    def total_slices(self):
        return (self.slices.x * self.slices.y * self.slices.z)

    def parse_metadata(self, metadata_path):
        if metadata_path.exists():
            with open(metadata_path, "r") as file:
                json_dict = json.load(file)
                min = json_dict["WorldBounds"]["MinCorner"]
                max = json_dict["WorldBounds"]["MaxCorner"]
                self.box = Box(
                    Vec3(min["Y"], -min["X"], min["Z"]),
                    Vec3(max["Y"], -max["X"], max["Z"]), #fuuuuuuuuuuuuuuuuuuuuuuuuu
                )
                setsize = json_dict["SetSize"]
                self.slices = Vec3(setsize["X"], setsize["Y"], setsize["Z"])
                tile_exists_list = json_dict["CubeExists"]
                for tile in self.box.slice_into_tiles(self.slices):
                    if tile_exists_list[tile.pos.x][tile.pos.y][tile.pos.z]:
                        tile.lod_dir_name = self.dir.name
                        self.tile_list.append(tile)

    @staticmethod
    def sort_lods_into_tile_tree(lod_list):
        child_tile_list = []
        for i, lod in reversed(list(enumerate(lod_list))):
            if (i == len(lod_list) - 1):
                child_tile_list = lod.tile_list
            else:
                tile_list = []
                for tile in lod.tile_list:
                    for child_tile in child_tile_list:
                        if child_tile.box.is_inside(tile.box):
                            tile.child_list.append(child_tile)
                    tile_list.append(tile)
                if (i == 0):
                    return tile_list
                else:
                    child_tile_list = tile_list
