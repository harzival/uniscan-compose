from pathlib import Path
from box import Box
from lod import Lod
from converter import Converter
import tempfile

obj_root_dir = Path(
    "C:/Users/harzival/Desktop/uniscan/datasets/testing/wall1/tiler-obj"
)

b3dm_root_path = Path(
    "C:/Users/harzival/Desktop/uniscan/datasets/testing/wall1/tileset"
)

lod_list = [Lod(dir) for dir in obj_root_dir.iterdir() if dir.is_dir()]

converter = Converter(
    _obj2gltf_js_path="C:/Users/harzival/Desktop/"
    "uniscanTo3DTiles/dependencies/obj2gltf/bin/obj2gltf.js",
    _3d_tiles_tools_js_path="C:/Users/harzival/Desktop/uniscanTo3DTiles"
    "/dependencies/3d-tiles-tools/tools/bin/3d-tiles-tools.js",
    _node_path="node",
)

for lod in lod_list:
    if (b3dm_root_path / lod.dir.name).exists() is False:
        (b3dm_root_path / lod.dir.name).mkdir()
    for tile in lod.tile_list:
        obj_path = lod.dir / tile.get_obj_name()
        albedo_path = lod.dir / tile.get_albedo_map_name()
        normal_path = lod.dir / tile.get_normal_map_name()
        b3dm_path = b3dm_root_path / lod.dir.name / tile.get_b3dm_name()
        converter.write_mtl_data(obj_path)
        with tempfile.TemporaryDirectory() as temp_dir:
            glb_path = Path(temp_dir) / tile.get_glb_name()
            converter.obj_to_glb(obj_path, glb_path, albedo_path, normal_path)
            converter.glb_to_b3dm(glb_path, b3dm_path)

world_box = Box.from_joining_box_list([lod.box for lod in lod_list])

tile_list = Lod.sort_lods_into_tile_tree(lod_list)

print("hi")
