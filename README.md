# Blender Daily Tutorial — PyBlitz

Build 3D elements, a custom mesh, and a low-poly humanoid character in
Blender using pure Python (`bpy`). Companion code for the PyBlitz daily
tutorial video (split-screen: code left, viewport right).

## What it builds
- Primitive shapes (cube, sphere, cylinder) at exact x, y, z coordinates
- A **custom pyramid mesh from raw geometry data**: vertex/face lists,
  `bpy.data.meshes.new` + `from_pydata` + `update()`,
  `bpy.data.objects.new`, and a new `CustomMeshes` collection linked
  into the scene (`custom_mesh.py`)
- A stylised low-poly humanoid from primitives (legs, torso, arms, head, eyes)
- Materials (dark body, cyan eyes/chest core) and studio lighting
  (sun + blue/purple area lights)

## Run (Blender 4.5.15 LTS)
```bash
blender -b -P daily_tutorial.py   # renders stage stills + 24-frame orbit, saves daily_tutorial.blend
blender -b -P custom_mesh.py     # verifies the custom mesh (5 verts, 5 faces) + renders the pyramid
```
Renders are Workbench viewport renders at 1920x1080 and land in `renders/`.
The humanoid is a stylised figure built from primitives — not a sculpted
realistic human.

## Channel
PyBlitz — https://youtube.com/@pyblitz
Playlist: Blender Python Course — Python Se Blender Expert Bano
