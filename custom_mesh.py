"""PyBlitz Daily Tutorial - ADD-ON: custom mesh from raw geometry data.
ORIGINAL example (not copied from any reference article): a small pyramid
built from our own vertex/face lists, using the lower-level data-block API:
  bpy.data.meshes.new + from_pydata + update,
  bpy.data.objects.new, and a new collection linked into the scene.
Run headless: blender -b -P custom_mesh.py
Verifies: mesh has 5 vertices / 5 faces, object is in the new collection,
and the scene renders.
"""
import bpy, os

OUT = os.path.expanduser("~/workspace/blender-daily-tutorial-build/renders")
os.makedirs(OUT, exist_ok=True)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.collections):
    for x in list(coll):
        if x.name not in ("Camera",):
            try:
                coll.remove(x)
            except Exception:
                pass

scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.display.shading.type = 'SOLID'
scene.display.shading.color_type = 'MATERIAL'
scene.world.color = (0.04, 0.04, 0.07)

# Camera rig (same look as the main tutorial: 3/4 view, tracked target)
bpy.ops.object.empty_add(location=(0, 0, 1))
target = bpy.context.active_object
target.name = "CamTarget"
bpy.ops.object.camera_add(location=(7, -8, 5))
cam = bpy.context.active_object
scene.camera = cam
con = cam.constraints.new(type='TRACK_TO')
con.target = target
con.track_axis = 'TRACK_NEGATIVE_Z'
con.up_axis = 'UP_Y'

# --- Step 1: our OWN geometry data: a pyramid ---
# Base square (z=0) + apex (z=2). 5 vertices, 5 faces, no edges needed:
# from_pydata derives edges from faces when the edge list is empty.
verts = [
    (-1.0, -1.0, 0.0),  # 0 base corner
    (1.0, -1.0, 0.0),   # 1 base corner
    (1.0, 1.0, 0.0),    # 2 base corner
    (-1.0, 1.0, 0.0),   # 3 base corner
    (0.0, 0.0, 2.0),    # 4 apex
]
edges = []
faces = [
    (0, 1, 2, 3),  # base
    (0, 1, 4),     # side
    (1, 2, 4),     # side
    (2, 3, 4),     # side
    (3, 0, 4),     # side
]

# --- Step 2: mesh data-block from the raw lists ---
pyramid_mesh = bpy.data.meshes.new("PyramidMesh")
pyramid_mesh.from_pydata(verts, edges, faces)
pyramid_mesh.update()
assert len(pyramid_mesh.vertices) == 5, len(pyramid_mesh.vertices)
assert len(pyramid_mesh.polygons) == 5, len(pyramid_mesh.polygons)

# --- Step 3: wrap the mesh in an object ---
pyramid_obj = bpy.data.objects.new("CustomPyramid", pyramid_mesh)

# --- Step 4: own collection, linked into the scene ---
custom_coll = bpy.data.collections.new("CustomMeshes")
scene.collection.children.link(custom_coll)
custom_coll.objects.link(pyramid_obj)
assert pyramid_obj.name in custom_coll.objects

# Material so the pyramid reads on camera (same neon palette as the tutorial)
mat = bpy.data.materials.new("Pyramid_Purple")
mat.use_nodes = True
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs["Base Color"].default_value = (0.66, 0.33, 0.97, 1.0)
bsdf.inputs["Metallic"].default_value = 0.7
bsdf.inputs["Roughness"].default_value = 0.25
mat.diffuse_color = (0.66, 0.33, 0.97, 1.0)  # Workbench renders use diffuse_color
pyramid_obj.data.materials.append(mat)

# Lighting (same studio setup family as the main tutorial)
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
bpy.context.active_object.data.energy = 3.0

scene.render.filepath = os.path.join(OUT, "custom_pyramid.png")
bpy.ops.render.render(write_still=True)

# Second angle: top-down-ish hero for the section end card
cam.location = (5, -9, 7)
scene.render.filepath = os.path.join(OUT, "custom_pyramid_hero.png")
bpy.ops.render.render(write_still=True)

bpy.ops.wm.save_as_mainfile(filepath=os.path.expanduser(
    "~/workspace/blender-daily-tutorial-build/custom_mesh.blend"))
print("CUSTOM MESH VERIFIED: verts=5 faces=5 object=CustomPyramid "
      "collection=CustomMeshes renders=custom_pyramid.png, custom_pyramid_hero.png")
