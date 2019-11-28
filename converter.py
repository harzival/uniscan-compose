from subprocess import call
from pathlib import Path


class Converter:
    def __init__(self, _obj2gltf_js_path, _3d_tiles_tools_js_path, _node_path):
        self._obj2gltf_js_path = str(_obj2gltf_js_path)
        self._3d_tiles_tools_js_path = str(_3d_tiles_tools_js_path)
        self._node_path = str(_node_path)

    @staticmethod
    def get_mtl_data(obj_path):
        opened_obj_file = obj_path.open('r')
        # Get the line in the mesh's file which starts with "usemtl ".
        # Return a string containing the line without the "usemtl " prefix.
        for i, line in enumerate(opened_obj_file):
            if line.startswith("usemtl"):
                mtl_data = "newmtl {0}\n{1}\n{2}\n{3}\n{4}\n{5}".format(
                    line.replace("usemtl ", "").rstrip("\n"),
                    "Ka 1 1 1",
                    "Kd 1 1 1",
                    "d 1",
                    "Ns 0",
                    "illum 1",
                )
                opened_obj_file.close()
                return mtl_data

    @classmethod
    def write_mtl_data(cls, obj_path):
        mtl_path = Path(str(obj_path).replace(".obj", ".mtl"))
        if mtl_path.exists():
            print(
                "UNISCAN: MTL file for OBJ already exists,"
                " will now delete and recreate it."
            )
            mtl_path.unlink()
        else:
            print(
                "UNISCAN: MTL file for OBJ does not exist,"
                " will now create it."
            )
        try:
            mtl_file = open(mtl_path, "x")
            mtl_file.write(cls.get_mtl_data(obj_path))
            mtl_file.close()
        except IOError as error:
            print(error)
        except Exception:
            print("UNISCAN: Unknown error creating MTL")

    def obj_to_glb(self, obj_path, glb_path, albedo_map_path, normal_map_path):
        call(
            [
                self._node_path,
                self._obj2gltf_js_path,
                "--binary",
                "--unlit",
                "-i",
                str(obj_path),
                "--baseColorTexture",
                str(albedo_map_path),
                "--normalTexture",
                str(normal_map_path),
                "-o",
                str(glb_path),
            ]
        )

    def glb_to_b3dm(self, glb_path, b3dm_path):
        call(
            [
                self._node_path,
                self._3d_tiles_tools_js_path,
                "glbToB3dm",
                "--force",
                "-i",
                str(glb_path),
                "-o",
                str(b3dm_path),
            ]
        )
