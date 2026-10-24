"""PyBlitz Daily Tutorial — SYNC VERSION formation animation (Blender 4.5.15 LTS).

ONE scene, ONE keyframed timeline. Every object appears / moves / recolours
only inside its own formation frame range, so the rendered frames can be
cut to the exact second its code line finishes typing in the video.

Frame plan (24 fps, Workbench unless noted):
  0          empty scene (after clean)
  10-57      cube scales 0 -> 1
  70-117     sphere scales 0 -> 1
  130-177    cylinder scales 0 -> 1
  190-249    pyramid vertex markers: 5 small spheres, 12 frames each
  262-309    pyramid mesh scales 0 -> 1 (faces fill as it grows)
  320        vertex markers hide (mesh solidifies into its object)
  332-367    demo shapes move aside (location keyframes)
  380-415    leg L scales in
  420-455    leg R scales in
  468-503    torso scales in
  516-551    arm L scales in
  556-591    arm R scales in
  604-639    head scales in
  652-675    eye L scales in
  680-703    eye R scales in
  716-739    chest core scales in
  752-775    body materials grey -> dark (diffuse + Principled keyframes)
  800-823    eye/core materials grey -> cyan
  840-887    EEVEE: sun + area light energies 0 -> full (lights ramp up)
  orbit      24 Workbench frames, camera 360 deg around final scene

Run headless: ~/workspace/blender/blender -b -P formation.py
Renders land in blender_frames/ next to this script.
"""
import bpy, math, os

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "blender_frames")
os.makedirs(OUT, exist_ok=True)

# --- clean scene ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras):
    for x in list(coll):
        coll.remove(x)

scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
scene.render.resolution_x = 1152
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.display.shading.type = 'SOLID'
scene.display.shading.color_type = 'MATERIAL'
scene.world.color = (0.04, 0.04, 0.07)

def mat(name, rgb, metallic=0.7, roughness=0.25):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    m.diffuse_color = (*rgb, 1.0)
    return m

BLUE   = mat("Neon_Blue",   (0.0, 0.83, 1.0))
PURPLE = mat("Neon_Purple", (0.66, 0.33, 0.97))
CYAN   = mat("Neon_Cyan",   (0.0, 1.0, 0.85))
DARK   = (0.05, 0.05, 0.12)
EYEC   = (0.0, 1.0, 1.0)
GREY   = (0.5, 0.5, 0.5)

def body_mat(name):
    """Own material per humanoid part, starting grey (Workbench + EEVEE safe)."""
    return mat(name, GREY, 0.0, 0.6)

def key_scale(obj, start, end, final_scale):
    obj.scale = (0.0, 0.0, 0.0)
    obj.keyframe_insert(data_path="scale", frame=start - 1)
    obj.scale = final_scale
    obj.keyframe_insert(data_path="scale", frame=end)
    # hold the final scale after formation
    obj.keyframe_insert(data_path="scale", frame=end + 1)

def key_loc(obj, start, end, new_loc):
    old = tuple(obj.location)
    obj.keyframe_insert(data_path="location", frame=start - 1)
    obj.location = new_loc
    obj.keyframe_insert(data_path="location", frame=end)

def key_colour(m, start, end, target):
    for f, col in ((start - 1, GREY), (end, target)):
        m.diffuse_color = (*col, 1.0)
        m.keyframe_insert(data_path="diffuse_color", frame=f)
        bsdf = m.node_tree.nodes["Principled BSDF"]
        bsdf.inputs["Base Color"].default_value = (*col, 1.0)
        bsdf.inputs["Base Color"].keyframe_insert(data_path="default_value", frame=f)

def add_cube(name, loc, scale=(1, 1, 1), material=None):
    bpy.ops.mesh.primitive_cube_add(size=2, location=loc)
    o = bpy.context.active_object; o.name = name; o.scale = scale
    if material: o.data.materials.append(material)
    return o

def add_sphere(name, loc, radius=1, material=None):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=loc)
    o = bpy.context.active_object; o.name = name
    if material: o.data.materials.append(material)
    return o

def add_cyl(name, loc, radius=0.5, depth=2, material=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, location=loc)
    o = bpy.context.active_object; o.name = name
    if material: o.data.materials.append(material)
    return o

# --- camera rig ---
bpy.ops.object.empty_add(location=(0, 0, 2))
target = bpy.context.active_object; target.name = "CamTarget"
bpy.ops.object.camera_add(location=(10, -12.5, 8))
cam = bpy.context.active_object; cam.name = "MainCam"
scene.camera = cam
con = cam.constraints.new(type='TRACK_TO')
con.target = target; con.track_axis = 'TRACK_NEGATIVE_Z'; con.up_axis = 'UP_Y'

def render_frame(frame, name):
    p = os.path.join(OUT, name)
    if os.path.exists(p) and os.path.getsize(p) > 0:
        print("SKIP existing", name, flush=True)
        return
    scene.frame_set(frame)
    scene.render.filepath = p
    bpy.ops.render.render(write_still=True)
    print("RENDERED", name, "frame", frame, flush=True)

# --- primitives (hidden scale 0 until their formation range) ---
cube = add_cube("Cube", (0, 0, 1), material=BLUE)
key_scale(cube, 10, 57, (1, 1, 1))
sphere = add_sphere("Sphere", (3, 0, 1), radius=1, material=PURPLE)
key_scale(sphere, 70, 117, (1, 1, 1))
cyl = add_cyl("Cylinder", (-3, 0, 1), radius=1, depth=2, material=CYAN)
key_scale(cyl, 130, 177, (1, 1, 1))

# --- custom pyramid: vertex markers, then the mesh itself ---
pyr_loc = (-5.0, 2.0, 0.0)
verts = [(-1.0, -1.0, 0.0), (1.0, -1.0, 0.0), (1.0, 1.0, 0.0),
         (-1.0, 1.0, 0.0), (0.0, 0.0, 2.0)]
markers = []
for i, v in enumerate(verts):
    loc = (pyr_loc[0] + v[0], pyr_loc[1] + v[1], pyr_loc[2] + v[2])
    m = add_sphere(f"Vert{i}", loc, radius=0.14, material=mat(f"VertMat{i}", (0.9, 0.9, 0.9), 0.0, 0.6))
    key_scale(m, 190 + i * 12, 190 + i * 12 + 11, (1, 1, 1))
    m.keyframe_insert(data_path="hide_render", frame=319)
    m.hide_render = True
    m.keyframe_insert(data_path="hide_render", frame=320)
    markers.append(m)

faces = [(0, 1, 2, 3), (0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4)]
pyr_mesh = bpy.data.meshes.new("PyramidMesh")
pyr_mesh.from_pydata(verts, [], faces)
pyr_mesh.update()
pyr_mat = mat("Pyramid_Purple", (0.66, 0.33, 0.97))
pyr_mesh.materials.append(pyr_mat)
pyr_obj = bpy.data.objects.new("CustomPyramid", pyr_mesh)
pyr_obj.location = pyr_loc
coll = bpy.data.collections.new("CustomMeshes")
scene.collection.children.link(coll)
coll.objects.link(pyr_obj)
key_scale(pyr_obj, 262, 309, (1, 1, 1))

# --- move demo shapes aside, then humanoid (grey first) ---
key_loc(cube, 332, 367, (6, 3, 1))
key_loc(sphere, 332, 367, (8, 3, 1))
key_loc(cyl, 332, 367, (4, 3, 1))

parts = {}
def humanoid(kind, name, loc, span, scale=(1, 1, 1), radius=None, depth=None):
    m = body_mat(name + "_Mat")
    if kind == 'cube':
        o = add_cube(name, loc, scale=scale, material=m)
    elif kind == 'sphere':
        o = add_sphere(name, loc, radius=radius, material=m)
    else:
        o = add_cyl(name, loc, radius=radius, depth=depth, material=m)
    key_scale(o, span[0], span[1], scale)
    parts[name] = (o, m)
    return o

humanoid('cyl', 'Leg_L', (-0.45, 0, 1.0), (380, 415), radius=0.28, depth=2)
humanoid('cyl', 'Leg_R', (0.45, 0, 1.0), (420, 455), radius=0.28, depth=2)
humanoid('cube', 'Torso', (0, 0, 3.0), (468, 503), scale=(0.9, 0.5, 1.2))
humanoid('cyl', 'Arm_L', (-1.15, 0, 3.1), (516, 551), radius=0.22, depth=1.8)
humanoid('cyl', 'Arm_R', (1.15, 0, 3.1), (556, 591), radius=0.22, depth=1.8)
humanoid('sphere', 'Head', (0, 0, 4.9), (604, 639), radius=0.6)
humanoid('sphere', 'Eye_L', (-0.22, -0.55, 5.0), (652, 675), radius=0.09)
humanoid('sphere', 'Eye_R', (0.22, -0.55, 5.0), (680, 703), radius=0.09)
humanoid('sphere', 'ChestCore', (0, -0.52, 3.1), (716, 739), radius=0.18)

# --- materials: body parts dark, then eyes/core cyan ---
for name in ('Leg_L', 'Leg_R', 'Torso', 'Arm_L', 'Arm_R', 'Head'):
    key_colour(parts[name][1], 752, 775, DARK)
for name in ('Eye_L', 'Eye_R', 'ChestCore'):
    key_colour(parts[name][1], 800, 823, EYEC)

# --- studio lights (energy 0 until the lighting range; EEVEE shows them) ---
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
sun = bpy.context.active_object
sun.data.energy = 0.0
sun.data.keyframe_insert(data_path="energy", frame=839)
sun.data.energy = 3.0
sun.data.keyframe_insert(data_path="energy", frame=887)
bpy.ops.object.light_add(type='AREA', location=(-6, -4, 6))
a1 = bpy.context.active_object
a1.data.energy = 0.0; a1.data.color = (0.0, 0.83, 1.0)
a1.data.keyframe_insert(data_path="energy", frame=839)
a1.data.energy = 800.0
a1.data.keyframe_insert(data_path="energy", frame=887)
bpy.ops.object.light_add(type='AREA', location=(6, 4, 6))
a2 = bpy.context.active_object
a2.data.energy = 0.0; a2.data.color = (0.66, 0.33, 0.97)
a2.data.keyframe_insert(data_path="energy", frame=839)
a2.data.energy = 800.0
a2.data.keyframe_insert(data_path="energy", frame=887)

bpy.ops.wm.save_as_mainfile(filepath=os.path.join(BASE, "formation.blend"))
print("SCENE BUILT, objects =", len(bpy.data.objects), flush=True)

# --- render Workbench formation frames ---
def render_range(a, b, prefix):
    for f in range(a, b + 1):
        render_frame(f, f"{prefix}_{f:04d}.png")

render_frame(0, "empty_0000.png")
render_range(10, 57, "f")
render_range(70, 117, "f")
render_range(130, 177, "f")
render_range(190, 249, "f")
render_range(262, 309, "f")
render_frame(320, "solid_0320.png")
render_range(332, 367, "f")
render_range(380, 415, "f")
render_range(420, 455, "f")
render_range(468, 503, "f")
render_range(516, 551, "f")
render_range(556, 591, "f")
render_range(604, 639, "f")
render_range(652, 675, "f")
render_range(680, 703, "f")
render_range(716, 739, "f")
render_range(752, 775, "f")
render_range(800, 823, "f")

# --- EEVEE lighting ramp (Workbench cannot visualise scene lights) ---
scene.render.engine = 'BLENDER_EEVEE_NEXT'
try:
    scene.eevee.use_soft_shadows = False
except Exception:
    pass  # removed in Blender 4.5 EEVEE-Next; shadow softness is per-light now
try:
    scene.eevee.taa_render_samples = 16
except Exception:
    pass
scene.world.color = (0.04, 0.04, 0.07)
for f in range(840, 888):
    render_frame(f, f"light_{f:04d}.png")

# --- Workbench orbit: 24 angles around the final scene ---
scene.render.engine = 'BLENDER_WORKBENCH'
for i in range(24):
    ang = 2 * math.pi * i / 24
    cam.location = (12 * math.cos(ang), 12 * math.sin(ang), 7.5)
    scene.frame_set(900)
    scene.render.filepath = os.path.join(OUT, f"orbit_{i:02d}.png")
    if os.path.exists(scene.render.filepath) and os.path.getsize(scene.render.filepath) > 0:
        print("SKIP existing orbit", i, flush=True)
        continue
    bpy.ops.render.render(write_still=True)
    print("RENDERED orbit", i, flush=True)
print("FORMATION RENDER DONE")
