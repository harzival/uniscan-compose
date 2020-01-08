import argparse

def get_parser():
    parser = argparse.ArgumentParser(
        'uniscan-compose',
        epilog="Creates a 3D Tile's Tileset, that complies with"
        "3D Tiles' standard, from a collection of OBJ meshes.",
        fromfile_prefix_chars="@"
    )
    parser.add_argument(
        "input",
        type=str,
        help="Path to root of directory containing list of OBJ mesh files",
    )
    parser.add_argument(
        "output",
        type=str,
        help="Path to directory where the output tilese"
        "t.json and .b3dm mesh files should placed",
    )
    parser.add_argument(
        "-d",
        "--debug",
        help="Set logging show debug messages.",
        action="store_true",
    )
    parser.add_argument(
        "-rt",
        "--root-transform",
        dest="root_transform"
        type=float,
        nargs=16,
        metavar=0,
        default=[
            96.86356343768793,
            24.848542777253734, 0, 
            0, -15.986465724980844,
            62.317780594908875,
            76.5566922962899,
            0, 19.02322243409411,
            -74.15554020821229,
            64.3356267137516, 0,
            1215107.7612304366,
            -4736682.902037748,
            4081926.095098698, 1]
        help="A transform on earth's surface specified with 16 f"
        "loats as per the 3D Tiles' standard's Transform",
        required=False,
    )
    parser.add_argument(
        "-o2gjs",
        "--obj2gltfjs",
        dest="obj2gltf_js_path"
        type=str,
        help="Path to the entrypoint js file in the obj2gltf"
        "NodeJS library",
        required=True,
    )
    parser.add_argument(
        "-3ttjs",
        "--3d-tiles-toolsjs",
        dest="3d_tiles_tools_js_path"
        type=str,
        help="Path to the entrypoint js file in the 3d-tiles-tools"
        "NodeJS library",
        required=True,
    )
    parser.add_argument(
        "-njs",
        "--nodejs-path",
        dest="node_path"
        type=str,
        help="Path to the NodeJS runtime command. e.g. just 'node' on most systems.",
        required=False,
        default="node"
    )
    parser.add_argument(
        "-mge",
        "--max-geom-error",
        dest="max_geom_error"
        type=float,
        help="The geometric error for the unrendered tileset, which"
        " is divided by the geometric error division factor for each"
        " level detail. e.g. '--max-geom-error 100000"
        " --geom-error-division-factor 10' causes Tileset: 100000,"
        " Root: 10000, Level-1: 1000, Level-2: 100, Level-3: 10 (highest detail)",
        required=False,
        default=100000
    )
    parser.add_argument(
        "-gedf",
        "--geom-error-division-factor",
        dest="geom_error_division_factor"
        type=float,
        help="The geometric error division factor for each"
        " level detail. e.g. '--max-geom-error 100000"
        " --geom-error-division-factor 10' causes Tileset: 100000,"
        " Root: 10000, Level-1: 1000, Level-2: 100, Level-3: 10 (highest detail)",
        required=False,
        default=10
    )
    parser.add_argument(
        "-tv",
        "--tileset-version",
        dest="tileset_version"
        type=str,
        help="The tileset 'asset' version to use in the resulting tileset.json",
        required=False,
        default="1.0"
    )
    return parser