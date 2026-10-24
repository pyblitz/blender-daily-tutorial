"""PyBlitz Daily Tutorial - master script (Blender 4.5.15 LTS).
Builds: primitives (cube/sphere/cylinder) + stylised low-poly humanoid
from primitives + materials + studio lighting. Renders Workbench stills
per build stage + a 24-frame camera orbit around the final model.
Run headless: blender -b -P daily_tutorial.py
"""
import bpy, math, os

OUT = os.path.expanduser("~/workspace/blender-daily-tutorial-build/renders")
os.makedirs(OUT, exist_ok=True)

# --- clean ---
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for coll in (bpy.data.meshes, bpy.data.materials, bpy.data.lights, bpy.data.cameras):
    for x in list(coll):
        coll.remove(x)

# --- world / render setup: Workbench viewport-style, 1920x1080 ---
scene = bpy.context.scene
scene.render.engine = 'BLENDER_WORKBENCH'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.display.shading.type = 'SOLID'
scene.display.shading.color_type = 'MATERIAL'
scene.display.shading.show_xray = False
scene.world.color = (0.04, 0.04, 0.07)

def mat(name, rgb, metallic=0.7, roughness=0.25):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    m.diffuse_color = (*rgb, 1.0)  # Workbench renders use diffuse_color, not Principled base color
    return m

BLUE   = mat("Neon_Blue",   (0.0, 0.83, 1.0))
PURPLE = mat("Neon_Purple", (0.66, 0.33, 0.97))
CYAN   = mat("Neon_Cyan",   (0.0, 1.0, 0.85))
DARK   = mat("Body_Dark",   (0.05, 0.05, 0.12), 0.8, 0.35)
EYE    = mat("Eye_Cyan",    (0.0, 1.0, 1.0), 0.0, 0.2)
GREY   = mat("Flat_Grey",   (0.5, 0.5, 0.5), 0.0, 0.6)

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

# --- camera rig: empty target + camera tracking it ---
bpy.ops.object.empty_add(location=(0, 0, 2))
target = bpy.context.active_object; target.name = "CamTarget"
bpy.ops.object.camera_add(location=(9, -11, 7))
cam = bpy.context.active_object; cam.name = "MainCam"
scene.camera = cam
con = cam.constraints.new(type='TRACK_TO')
con.target = target; con.track_axis = 'TRACK_NEGATIVE_Z'; con.up_axis = 'UP_Y'

def render(name):
    scene.render.filepath = os.path.join(OUT, name)
    bpy.ops.render.render(write_still=True)
    print("RENDERED:", name)

render("empty.png")

# --- PHASE: shapes ---
cube = add_cube("Cube", (0, 0, 1), material=BLUE)
render("shape_cube.png")
sphere = add_sphere("Sphere", (3, 0, 1), radius=1, material=PURPLE)
render("shape_cube_sphere.png")
cyl = add_cyl("Cylinder", (-3, 0, 1), radius=1, depth=2, material=CYAN)
render("shapes.png")

# --- PHASE: humanoid (built untextured first, then materials) ---
# Move the demo shapes aside so the character stands centre-frame
cube.location = (6, 3, 1); sphere.location = (8, 3, 1); cyl.location = (4, 3, 1)
leg_l = add_cyl("Leg_L", (-0.45, 0, 1.0), radius=0.28, depth=2)
leg_r = add_cyl("Leg_R", (0.45, 0, 1.0), radius=0.28, depth=2)
render("char_legs.png")
torso = add_cube("Torso", (0, 0, 3.0), scale=(0.9, 0.5, 1.2))
render("char_torso.png")
arm_l = add_cyl("Arm_L", (-1.15, 0, 3.1), radius=0.22, depth=1.8)
arm_r = add_cyl("Arm_R", (1.15, 0, 3.1), radius=0.22, depth=1.8)
head = add_sphere("Head", (0, 0, 4.9), radius=0.6)
eye_l = add_sphere("Eye_L", (-0.22, -0.55, 5.0), radius=0.09)
eye_r = add_sphere("Eye_R", (0.22, -0.55, 5.0), radius=0.09)
render("char_grey.png")

# --- PHASE: materials + studio lighting ---
for o in (leg_l, leg_r, torso, arm_l, arm_r):
    o.data.materials.append(DARK)
head.data.materials.append(DARK)
eye_l.data.materials.append(EYE); eye_r.data.materials.append(EYE)
core = add_sphere("ChestCore", (0, -0.52, 3.1), radius=0.18, material=EYE)
bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
sun = bpy.context.active_object; sun.data.energy = 3.0
bpy.ops.object.light_add(type='AREA', location=(-6, -4, 6))
a1 = bpy.context.active_object; a1.data.energy = 800; a1.data.color = (0.0, 0.83, 1.0)
bpy.ops.object.light_add(type='AREA', location=(6, 4, 6))
a2 = bpy.context.active_object; a2.data.energy = 800; a2.data.color = (0.66, 0.33, 0.97)
render("char_final.png")

# --- hero: wider camera, demo shapes hidden so the character is clean centre-frame ---
for o in (cube, sphere, cyl):
    o.hide_render = True
cam.location = (11, -13, 8)
render("hero.png")

# --- orbit: 24 frames around final model ---
for i in range(24):
    ang = 2 * math.pi * i / 24
    cam.location = (11 * math.cos(ang), 11 * math.sin(ang), 6.5)
    render(f"orbit_{i:02d}.png")

bpy.ops.wm.save_as_mainfile(filepath=os.path.expanduser(
    "~/workspace/blender-daily-tutorial-build/daily_tutorial.blend"))
print("DONE: objects =", len(bpy.data.objects))
