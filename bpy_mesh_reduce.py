import bpy
import tempfile
import subprocess
from pathlib import Path

input_dir = Path(
    "C:/Users/harzival/Desktop/uniscan/datasets/testing/wall1/tiler-obj"
)
output_dir = Path(
    "C:/Users/harzival/Desktop/uniscan/datasets/testing/wall1/optimiser-obj"
)
hausdorff_script = Path("B:/Uniscan/BakeMyScan/scripting/geomerror.mlx")
reduction_factor = 0.05
max_error = 0.0015


def import_obj(obj_path):
    object_list = [o for o in bpy.data.objects]
    bpy.ops.import_scene.obj(filepath=str(obj_path), axis_up="Z")
    object_list = [o for o in bpy.data.objects if o not in object_list]
    mesh = [o for o in object_list if o.type == "MESH"][0]
    return mesh


def import_texture(texture_path):
    bpy.ops.bakemyscan.create_empty_material()
    bpy.ops.bakemyscan.assign_texture(filepath=str(texture_path))


def set_active_object(object):
    bpy.context.scene.objects.active = object


def deselect_all():
    bpy.ops.object.select_all(action="DESELECT")


def get_boundary_face_count(mesh):
    deselect_all()
    set_active_object(mesh)
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="DESELECT")
    bpy.ops.mesh.select_non_manifold()
    bpy.context.active_object.update_from_editmode()
    bpy.ops.object.mode_set(mode="OBJECT")
    return len(
        [f for f in bpy.context.active_object.data.polygons if f.select]
    )


def reduce_mesh(mesh, face_count):
    deselect_all()
    mesh.select = True
    set_active_object(mesh)
    bpy.ops.bakemyscan.remesh_meshlab(
        facescount=face_count,  # Target faces in output mesh.
        quality=0.37,  # Quality threshold.
        boundaries=True,  # Preserve the mesh's 'boundary'.
        weight=0.1,  # Boundary preservation extent.
        normals=False,  # Preserve existing normal maps.
        topology=False,  # Preserve existing topology.
        existing=False,  # 'Use' existing verticies.
        planar=False,  # Apply planar simplification.
        post=True,  # Check for isolated/duplicated verticies.
    )
    return bpy.context.active_object


def get_total_face_count(mesh):
    return len(mesh.data.polygons)


def get_hausdorff_error(original_mesh, reduced_mesh):
    temp_dir = tempfile.TemporaryDirectory()
    original_mesh_path = Path(temp_dir.name) / "original.obj"
    reduced_mesh_path = Path(temp_dir.name) / "reduced.obj"
    deselect_all()
    set_active_object(original_mesh)
    original_mesh.select = True
    bpy.ops.export_scene.obj(
        filepath=str(original_mesh_path), use_selection=True
    )
    deselect_all()
    set_active_object(reduced_mesh)
    reduced_mesh.select = True
    bpy.ops.export_scene.obj(
        filepath=str(reduced_mesh_path), use_selection=True
    )
    command = [
        bpy.types.Scene.executables["meshlabserver"],
        "-i",
        str(original_mesh_path),
        "-i",
        str(reduced_mesh_path),
        "-s",
        str(hausdorff_script),
    ]
    str_cmd = ""
    for part in command:
        str_cmd += str(part) + " "
    print(str_cmd)
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
    )
    stdout, _ = proc.communicate()
    for line in stdout.splitlines():
        if "RMS : " in line:
            return float(line.split("RMS : ")[1])
            # Stops unwanted lines containing "RMS : " being captured
            break


def bake_between_meshes(mesh, reduced_mesh):
    deselect_all()
    set_active_object(reduced_mesh)
    reduced_mesh.select = True
    bpy.ops.bakemyscan.unwrap()
    mesh.select = True
    bpy.ops.bakemyscan.bake_textures(
        resolution=1024,  # Texture resolution
        cageRatio=0.02,  # Baking cage size as a ratio
        bake_albedo=True,  # Bake albedo map
        bake_geometry=True,  # Bake geometric normals into normal map
        bake_surface=True,  # Bake shading-surface normals into the same map.
    )


def export_obj(mesh, output_path):
    if output_path.parent.parent.exists() is not True:
        output_path.parent.parent.mkdir()
    if output_path.parent.exists() is not True:
        output_path.parent.mkdir()
    set_active_object(mesh)
    # Tell BakeMyScan to export the reduced mesh as an OBJ, with its albedo and
    # normal maps (jpg) in the same place, named by taking the ".obj" off the
    # export path and adding "_albedo.jpg" and "_normal.jpg" respectively.
    bpy.ops.bakemyscan.export(filepath=str(output_path))


def main():
    class Mesh:
        def __init__(self, obj_path, texture_path):
            self.obj_path = obj_path
            self.texture_path = texture_path

    input_mesh_list = []
    for lod_dir in [d for d in input_dir.iterdir() if d.is_dir()]:
        for obj_path in [
            p for p in lod_dir.iterdir() if p.name.endswith(".obj")
        ]:
            for line in obj_path.open("r"):
                if line.startswith("mtllib "):
                    texture_path = lod_dir / Path(
                        line.replace("mtllib ", "")
                        .replace(".mtl", ".jpg")
                        .rstrip("\n")
                    )
                    input_mesh_list.append(Mesh(obj_path, texture_path))
                    break
    for input_mesh in input_mesh_list:
        mesh = import_obj(input_mesh.obj_path)
        set_active_object(mesh)
        import_texture(input_mesh.texture_path)
        boundary_face_count = get_boundary_face_count(mesh)
        target_face_count = (
            round(get_total_face_count(mesh) * reduction_factor)
            + boundary_face_count
        )
        reduction_incomplete = True
        reduced_mesh = None
        while reduction_incomplete:
            reduced_mesh = reduce_mesh(mesh, target_face_count)
            hausdorff_error = get_hausdorff_error(mesh, reduced_mesh)
            if hausdorff_error < max_error:
                reduction_incomplete = False
            else:
                print(
                    "DEFORM-TEST: Hausdorff Error exceeds threshold! "
                    + str(hausdorff_error)
                    + " > "
                    + str(max_error)
                )
                print(
                    "DEFORM-TEST: Master mesh faces: "
                    + str(len(mesh.data.polygons))
                )
                print(
                    "DEFORM-TEST: Rejected mesh faces: "
                    + str(target_face_count)
                )
                target_face_count += round(target_face_count * 0.03)
                print(
                    "DEFORM-TEST: Faces to reduce with: "
                    + str(target_face_count)
                )
        bake_between_meshes(mesh, reduced_mesh)
        export_path = (
            output_dir
            / input_mesh.obj_path.parent.name
            / input_mesh.obj_path.name
        )
        export_obj(reduced_mesh, export_path)

        print("UNISCAN: Mesh reduction complete!")
        print("UNISCAN: Mesh name: " + input_mesh.obj_path.name)
        print("UNISCAN: Original mesh faces: " + str(len(mesh.data.polygons)))
        print(
            "UNISCAN: Reduced mesh faces: "
            + str(len(reduced_mesh.data.polygons))
        )

        set_active_object(mesh)
        mesh.select = True
        deselect_all()
        bpy.ops.object.delete()
        set_active_object(reduced_mesh)
        reduced_mesh.select = True
        bpy.ops.object.delete()


main()
