import tempfile
import json
from pathlib import Path
from box import Box
from lod import Lod
from tile import RootTile, Tileset
from converter import Converter
from arg_parser import get_parser

def main(args=None):

    parser = get_parser()
    args = parser.parse_args(args)
    obj_root_dir = Path(args.input)
    b3dm_root_path = Path(args.output)
    converter = Converter(
        _obj2gltf_js_path=args._obj2gltf_js_path,
        _3d_tiles_tools_js_path=args._3d_tiles_tools_js_path,
        _node_path=args._node_path)
    geom_error_list = [args.max_geom_error]
    geom_error_division_factor = args.geom_error_division_factor
    geom_error_list.append(geom_error_list[0] / geom_error_division_factor)
    root_transform = args.root_transform
    tileset_version = args.tileset_version

    if b3dm_root_path.exists() is False:
        b3dm_root_path.mkdir()

    lod_list = [Lod(dir) for dir in obj_root_dir.iterdir() if dir.is_dir()]
    lod_list.sort(key=lambda l: l.total_slices())

    for lod in lod_list:
        geom_error_list.append(geom_error_list[-1] / geom_error_division_factor)
        if (b3dm_root_path / lod.dir.name).exists() is False:
            (b3dm_root_path / lod.dir.name).mkdir()
        for tile in lod.tile_list:
            b3dm_path = b3dm_root_path / lod.dir.name / tile.get_b3dm_name()
            tile.geom_error = geom_error_list[-1]
            obj_path = lod.dir / tile.get_obj_name()
            tile.geom_box = Box.from_obj_geometry(str(obj_path))
            if b3dm_path.exists():
                print(
                    "UNISCAN: The '.b3dm' of "+lod.dir.name+"/"+tile.get_name() +
                    " already exists in export location ("+str(b3dm_root_path)+")")
            else:
                amap_path = lod.dir / tile.get_albedo_map_name()
                nmap_path = lod.dir / tile.get_normal_map_name()
                converter.write_mtl_data(obj_path)
                with tempfile.TemporaryDirectory() as temp_dir:
                    glb_path = Path(temp_dir) / tile.get_glb_name()
                    converter.obj_to_glb(obj_path, glb_path, amap_path, nmap_path)
                    converter.glb_to_b3dm(glb_path, b3dm_path)

    tile_list = Lod.sort_lods_into_tile_tree(lod_list)
    world_box = Box.from_joining_box_list([tile.geom_box for tile in tile_list])
    root_tile = RootTile(world_box, tile_list, 10000, root_transform)
    tileset = Tileset("1.0", 100000, root_tile)
    with (b3dm_root_path / "tileset.json").open('w') as file:
        json.dump(dict(tileset), file, indent=4)

if __name__ == "__main__":
    main()
