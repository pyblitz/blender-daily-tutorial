"""PyBlitz Daily Tutorial — SYNC v2 presenter (REAL Blender GUI capture).

Fixes the owner's 3 rejections of the v1 sync video:
  1. THEME: no PIL editor anywhere — the screen IS the real Blender 4.5.15
     window (Text Editor + Viewport + Outliner/Properties + Timeline).
  2. KEYBOARD: real keyboard clicks gated to typing windows, one click per
     visible keypress (post step, not a faint looped bed).
  3. BLENDER-ONLY: every frame is the live Blender GUI, except the light
     segment (665-680 s) where the viewport 3D area shows pre-rendered
     EEVEE light frames of the SAME scene in post (disclosed in report).

How it runs (flag-gated so the capture starts clean):
  Phase A (setup, first timer tick): fullscreen, split main viewport
    vertically (editor left ~769 px / viewport right ~813 px), split the
    editor horizontally (editor top ~820 px / console bottom ~129 px, so
    burned captions at MarginV 90 never overlap code), Timeline bottom
    strip, Workbench SOLID/MATERIAL viewport, view look-at framing.
    Writes /tmp/v2_setup_done (or /tmp/v2_setup_bad + aborts on bad geometry).
  Phase B (wait): polls for /tmp/v2_start every 0.5 s. Pre-start state:
    frame 0 (empty scene), both text blocks empty, view at initial angle.
  Phase C (presentation, wall-clock schedule, ~720 s): typing windows,
    formation frame playback, orbit previews, cursor parking on causal
    lines — all driven by absolute video time (no drift accumulation).
    Writes /tmp/v2_done at t=720 and stops (caller kills Blender).

Schedule = v1 timeline_sync_map.md EXACTLY (same typing windows, same
formation frame ranges, same voice placements in post). Content = STEPS
lines from build_video.py (own script excerpts, not copied reference).

Run: Xvfb :97 + blender formation.blend --python presenter_v2.py
Capture: ffmpeg x11grab :97, 1920x1080, 24 fps (started after setup_done,
before v2_start, so the empty->finished transition at t=0 is captured).
"""
import bpy
import math
import os
import time
from mathutils import Vector, Matrix, Quaternion

B = os.path.dirname(os.path.abspath(__file__))
SETUP_DONE = "/tmp/v2_setup_done"
SETUP_BAD = "/tmp/v2_setup_bad"
START_FLAG = "/tmp/v2_start"
DONE_FLAG = "/tmp/v2_done"

# ------------------------------------------------------------------ data
# (id, block, lines, type_start, type_end, formation, form_end)
# formation: None | ("frames", first, last) | ("still", frame)
# form_end: timestamp the formation clip ENDS.
STEPS = [
    ("s2_import", "daily", [
        "import bpy",
        "",
        "# Scripting workspace:",
        "# Text Editor, new text block"], 30, 48, None, 48),
    ("s2_clean", "daily", [
        "bpy.ops.object.select_all(",
        "    action='SELECT')",
        "bpy.ops.object.delete()",
        "",
        "# Every run starts clean"], 48, 78, ("still", 0), 80),
    ("s3_cube", "daily", [
        "blue = neon_material(",
        "    'Neon_Blue', (0.0, 0.83, 1.0))",
        "bpy.ops.mesh.primitive_cube_add(",
        "    size=2, location=(0, 0, 1))",
        "cube = bpy.context.active_object",
        "cube.data.materials.append(blue)"], 90, 140, ("frames", 10, 57), 142),
    ("s3_sphere", "daily", [
        "purple = neon_material(",
        "    'Neon_Purple', (0.66, 0.33, 0.97))",
        "bpy.ops.mesh.primitive_uv_sphere_add(",
        "    radius=1, location=(3, 0, 1))",
        "sphere = bpy.context.active_object",
        "sphere.data.materials.append(purple)"], 150, 195, ("frames", 70, 117), 197),
    ("s3_cyl", "daily", [
        "cyan = neon_material(",
        "    'Neon_Cyan', (0.0, 1.0, 0.85))",
        "bpy.ops.mesh.primitive_cylinder_add(",
        "    radius=1, depth=2,",
        "    location=(-3, 0, 1))",
        "cyl = bpy.context.active_object",
        "cyl.data.materials.append(cyan)"], 205, 258, ("frames", 130, 177), 260),
    ("s4_verts", "custom", [
        "# Our own pyramid: base + apex",
        "verts = [(-1, -1, 0), (1, -1, 0),",
        "         (1, 1, 0), (-1, 1, 0),",
        "         (0, 0, 2)]",
        "edges = []"], 270, 315, ("frames", 190, 249), 317.5),
    ("s4_faces", "custom", [
        "faces = [(0, 1, 2, 3), (0, 1, 4),",
        "         (1, 2, 4), (2, 3, 4),",
        "         (3, 0, 4)]"], 320, 355, ("frames", 262, 309), 357),
    ("s4_mesh", "custom", [
        "mesh = bpy.data.meshes.new(",
        "    'PyramidMesh')",
        "mesh.from_pydata(verts, edges, faces)",
        "mesh.update()",
        "obj = bpy.data.objects.new(",
        "    'CustomPyramid', mesh)",
        "coll = bpy.data.collections.new(",
        "    'CustomMeshes')",
        "bpy.context.scene.collection",
        "    .children.link(coll)",
        "coll.objects.link(obj)"], 360, 392, ("still", 320), 394),
    ("s5_move", "daily", [
        "# Slide demo shapes aside",
        "cube.location = (6, 3, 1)",
        "sphere.location = (8, 3, 1)",
        "cyl.location = (4, 3, 1)"], 400, 412, ("frames", 332, 367), 413.5),
    ("s5_legL", "daily", [
        "# Legs: two cylinders",
        "leg_l = add_cyl('Leg_L',",
        "    (-0.45, 0, 1.0),",
        "    radius=0.28, depth=2)"], 414, 426, ("frames", 380, 415), 427.5),
    ("s5_legR", "daily", [
        "leg_r = add_cyl('Leg_R',",
        "    (0.45, 0, 1.0),",
        "    radius=0.28, depth=2)"], 428, 440, ("frames", 420, 455), 441.5),
    ("s5_torso", "daily", [
        "# Torso: a box, scaled tall",
        "torso = add_cube('Torso',",
        "    (0, 0, 3.0),",
        "    scale=(0.9, 0.5, 1.2))"], 442, 456, ("frames", 468, 503), 457.5),
    ("s5_armL", "daily", [
        "# Arms: two cylinders",
        "arm_l = add_cyl('Arm_L',",
        "    (-1.15, 0, 3.1),",
        "    radius=0.22, depth=1.8)"], 458, 470, ("frames", 516, 551), 471.5),
    ("s5_armR", "daily", [
        "# Arms: two cylinders",
        "arm_r = add_cyl('Arm_R',",
        "    (1.15, 0, 3.1),",
        "    radius=0.22, depth=1.8)"], 472, 484, ("frames", 556, 591), 485.5),
    ("s5_head", "daily", [
        "# Head: a sphere",
        "head = add_sphere('Head',",
        "    (0, 0, 4.9), radius=0.6)"], 486, 498, ("frames", 604, 639), 499.5),
    ("s5_eyeL", "daily", [
        "# Eyes: two tiny spheres",
        "eye_l = add_sphere('Eye_L',",
        "    (-0.22, -0.55, 5.0),",
        "    radius=0.09)"], 500, 510, ("frames", 652, 675), 511),
    ("s5_eyeR", "daily", [
        "eye_r = add_sphere('Eye_R',",
        "    (0.22, -0.55, 5.0),",
        "    radius=0.09)"], 512, 522, ("frames", 680, 703), 523),
    ("s5_done", "daily", [
        "# Same pattern, arranged",
        "# like a person - character done",
        "# Next: materials make it real"], 523, 552, None, 552),
    ("s6_core", "daily", [
        "# Chest core: a glowing sphere",
        "core = add_sphere('ChestCore',",
        "    (0, -0.52, 3.1), radius=0.18)"], 560, 572, ("frames", 716, 739), 573),
    ("s6_body", "daily", [
        "# Dark material for the body",
        "for o in (leg_l, leg_r, torso,",
        "          arm_l, arm_r, head):",
        "    o.data.materials.append(DARK)"], 574, 596, ("frames", 752, 775), 597),
    ("s6_eyes", "daily", [
        "# Cyan eyes and chest core",
        "eye_l.data.materials.append(EYE)",
        "eye_r.data.materials.append(EYE)",
        "core.data.materials.append(EYE)"], 598, 616, ("frames", 800, 823), 617),
    ("s6_light", "daily", [
        "# Sun + blue and purple areas",
        "bpy.ops.object.light_add(",
        "    type='SUN', location=(5, -5, 10))",
        "bpy.ops.object.light_add(",
        "    type='AREA',",
        "    location=(-6, -4, 6))",
        "# area colour: neon blue",
        "bpy.ops.object.light_add(",
        "    type='AREA',",
        "    location=(6, 4, 6))",
        "# area colour: neon purple"], 618, 665, None, 665),
]
# Result-first header lines (typed 2-22 s, cleared at 30 s)
S1_LINES = [
    "# RESULT FIRST: finished scene",
    "# Built by code - no mouse",
    "",
]
# KEY: 0-based line index within the step, parked on during formation/dwell
KEY = {"s1_header": 0, "s2_import": 0, "s2_clean": 2, "s3_cube": 2,
       "s3_sphere": 2, "s3_cyl": 2, "s4_verts": 1, "s4_faces": 0,
       "s4_mesh": 2, "s5_move": 0, "s5_legL": 1, "s5_legR": 0,
       "s5_torso": 1, "s5_armL": 1, "s5_armR": 0, "s5_head": 1,
       "s5_eyeL": 1, "s5_eyeR": 0, "s5_done": 1, "s6_core": 1,
       "s6_body": 3, "s6_eyes": 1, "s6_light": 1}
OUTRO_START, TOTAL = 680.0, 720.0

# ---------------------------------------------------------------- helpers
def look_at_rotation(eye, target, up=(0, 0, 1)):
    fwd = (Vector(target) - Vector(eye)).normalized()
    upv = Vector(up)
    right = fwd.cross(upv).normalized()
    up2 = right.cross(fwd).normalized()
    m = Matrix((right.to_3d(), up2.to_3d(), (-fwd).to_3d()))
    m.transpose()
    return m.to_quaternion()


INIT_ROT = look_at_rotation((10, -12.5, 8), (0, 0, 2))
INIT_LOC = Vector((1, 1, 2.5))
INIT_DIST = 20.0

# ---------------------------------------------------------------- state
S = {
    "phase": "setup", "ed": None, "vp": None, "ed_region": None,
    "daily": None, "custom": None,
    "t0": None, "cur_step": None, "typed_chars": 0, "parked": False,
    "state_frame": 0, "cleared": False, "cur_block": "daily",
    "last_frame": None, "done": False,
}


def ed_space():
    for sp in S["ed"].spaces:
        if sp.type == 'TEXT_EDITOR':
            return sp
    return None


def vp_space():
    for sp in S["vp"].spaces:
        if sp.type == 'VIEW_3D':
            return sp
    return None


def move_to_cursor():
    """Scroll editor view to cursor (proven in pilot5)."""
    try:
        with bpy.context.temp_override(window=bpy.context.window,
                                       screen=bpy.context.window.screen,
                                       area=S["ed"], region=S["ed_region"]):
            bpy.ops.text.move(type='LINE_END')
    except Exception as e:
        print("V2: move override failed:", e, flush=True)


def set_frame(f):
    if S["last_frame"] != f:
        bpy.context.scene.frame_set(int(f))
        S["last_frame"] = int(f)


def set_view_rot(rot):
    sp = vp_space()
    if sp is not None:
        sp.region_3d.view_rotation = rot


def cursor_to_end(txt):
    """Move cursor to the end of a text block's content (authoritative)."""
    try:
        lines = txt.lines
        n = len(lines)
        last = lines[n - 1].body if n else ""
        txt.cursor_set(n - 1, character=len(last))
    except Exception as e:
        print("V2: cursor_to_end failed:", e, flush=True)


def switch_block(block):
    """Point editor at block; cursor to end of that block's content."""
    if S["cur_block"] == block:
        return
    sp = ed_space()
    txt = S["daily"] if block == "daily" else S["custom"]
    sp.text = txt
    S["cur_block"] = block
    cursor_to_end(txt)
    move_to_cursor()
    print(f"V2: switched editor to {block}", flush=True)


def park_on_key(step_id, block):
    """Park cursor at start of the step's causal line (formation/dwell).
    KEY absolute line (0-based) = lines of earlier steps in the SAME block
    (s1 header lines were cleared at 30 s, so they never count) + KEY."""
    step = next(s for s in STEPS if s[0] == step_id)
    n_before = sum(len(s[2]) for s in STEPS if s[3] < step[3] and s[1] == block)
    key_abs = n_before + KEY[step_id]
    txt = S["daily"] if block == "daily" else S["custom"]
    try:
        txt.cursor_set(key_abs, character=0)
    except Exception as e:
        print("V2: park cursor_set failed:", e, flush=True)
    move_to_cursor()
    S["parked"] = True


def unpark(block):
    """Cursor back to end of current content before typing resumes."""
    txt = S["daily"] if block == "daily" else S["custom"]
    cursor_to_end(txt)
    move_to_cursor()
    S["parked"] = False


def type_upto(step, t):
    """Type step's chars up to video time t (char-by-char, incremental).
    Steps are separate line groups: before a step's first char, if its text
    block already holds content, write ONE separator newline first, so the
    step's first line starts on its own line (without this, step N+1's first
    line would merge onto step N's last line)."""
    sid, block, lines, ts, te, form, fe = step
    switch_block(block)
    if S["parked"]:
        unpark(block)
    if S.get("sep_pending") == sid:
        S["sep_pending"] = None
        txt0 = S["daily"] if block == "daily" else S["custom"]
        if txt0.as_string() != "":
            txt0.write("\n")
            move_to_cursor()
    text = "\n".join(lines)
    total = len(text)
    per = (te - ts) / max(1, total)
    target = total if t >= te else int((t - ts) / per)
    target = max(0, min(total, target))
    txt = S["daily"] if block == "daily" else S["custom"]
    start = S["typed_chars"]
    if target > start:
        chunk = text[start:target]
        for ch in chunk:
            txt.write(ch)
            if ch == "\n":
                move_to_cursor()
        S["typed_chars"] = target


# ---------------------------------------------------------------- setup
def do_setup():
    win = bpy.context.window
    screen = win.screen
    try:
        bpy.ops.wm.window_fullscreen_toggle()
    except Exception as e:
        print("V2: fullscreen failed:", e, flush=True)
    v3d = None
    for a in screen.areas:
        if a.type == 'VIEW_3D':
            if v3d is None or a.width * a.height > v3d.width * v3d.height:
                v3d = a
    win_region = None
    for r in v3d.regions:
        if r.type == 'WINDOW':
            win_region = r
            break
    win.cursor_warp(v3d.x + v3d.width // 2, v3d.y + v3d.height // 2)
    oy, oh = v3d.y, v3d.height
    with bpy.context.temp_override(window=win, screen=screen, area=v3d, region=win_region):
        bpy.ops.screen.area_split(direction='VERTICAL', factor=0.485)
    # wait a beat for redraw (next tick) is handled by caller staging
    return ("vsplit", oy, oh)


def finish_setup():
    win = bpy.context.window
    screen = win.screen
    # find vertical split result (two VIEW_3D with original y/height)
    # (orig y/h stored by caller in S)
    oy, oh = S["v_orig"]
    cands = [a for a in screen.areas if a.type == 'VIEW_3D' and a.y == oy and a.height == oh and a.width > 10]
    cands.sort(key=lambda a: a.x)
    print("V2: vertical split candidates:", [(a.x, a.width) for a in cands], flush=True)
    if len(cands) < 2:
        return False, "vertical split failed"
    ed, vp = cands[0], cands[1]
    ed.ui_type = 'TEXT_EDITOR'
    # horizontal split of editor: editor top (~820) / console bottom (~129)
    ed_region = None
    for r in ed.regions:
        if r.type == 'WINDOW':
            ed_region = r
            break
    win.cursor_warp(ed.x + ed.width // 2, ed.y + ed.height // 2)
    ey, eh = ed.y, ed.height
    with bpy.context.temp_override(window=win, screen=screen, area=ed, region=ed_region):
        bpy.ops.screen.area_split(direction='HORIZONTAL', factor=0.136)
    S["h_orig"] = (ey, eh, ed.x, ed.width)
    return True, "vsplit ok, hsplit pending"


def finish_hsplit():
    win = bpy.context.window
    screen = win.screen
    ey, eh, ex, ew = S["h_orig"]
    parts = [a for a in screen.areas if a.x == ex and a.width == ew and a.y >= ey and a.y + a.height <= ey + eh and a.height > 10]
    parts.sort(key=lambda a: a.y)
    print("V2: horizontal split parts:", [(a.type, a.x, a.y, a.width, a.height) for a in parts], flush=True)
    if len(parts) < 2:
        return False, "horizontal split failed"
    bottom, top = parts[0], parts[-1]
    # editor must be the TALL TOP part, console the SHORT BOTTOM part
    if not (top.height > bottom.height and top.height > 600 and bottom.height < 300):
        return False, f"hsplit geometry wrong: top={top.height} bottom={bottom.height}"
    top.ui_type = 'TEXT_EDITOR'
    bottom.ui_type = 'CONSOLE'
    S["ed"], S["vp"] = top, None
    # viewport = the VIEW_3D from vertical split (unchanged by hsplit)
    oy, oh = S["v_orig"]
    cands = [a for a in screen.areas if a.type == 'VIEW_3D' and a.y == oy and a.height == oh and a.width > 10]
    cands.sort(key=lambda a: a.x)
    # viewport is the right one (editor was left); after hsplit, editor is top
    # (a TEXT_EDITOR now, not VIEW_3D), so remaining VIEW_3D candidate is viewport
    if len(cands) < 1:
        return False, "viewport lost after hsplit"
    S["vp"] = cands[-1]
    for a in screen.areas:
        if a.type == 'DOPESHEET_EDITOR':
            a.ui_type = 'TIMELINE'
    # editor region + text blocks
    for r in S["ed"].regions:
        if r.type == 'WINDOW':
            S["ed_region"] = r
            break
    daily = bpy.data.texts.new("daily_tutorial.py")
    custom = bpy.data.texts.new("custom_mesh.py")
    S["daily"], S["custom"] = daily, custom
    for sp in S["ed"].spaces:
        if sp.type == 'TEXT_EDITOR':
            sp.text = daily
            sp.show_line_numbers = True
            sp.show_syntax_highlight = True
            sp.show_word_wrap = False
            try:
                sp.font_size = 20
            except Exception as e:
                print("V2: font_size failed:", e, flush=True)
    for sp in S["vp"].spaces:
        if sp.type == 'VIEW_3D':
            sp.shading.type = 'SOLID'
            sp.shading.color_type = 'MATERIAL'
            r3d = sp.region_3d
            r3d.view_location = INIT_LOC
            r3d.view_distance = INIT_DIST
            r3d.view_rotation = INIT_ROT
            r3d.view_perspective = 'PERSP'
    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = 900
    scene.frame_set(0)
    S["state_frame"] = 0
    S["last_frame"] = 0
    # Viewport chrome cleanup (Blender-native, not a fake):
    # - hide the scene camera's wireframe: MainCam sits between the view eye
    #   and the scene, so its frustum pyramid would float across the frame
    #   (hide_viewport never affects rendering).
    # - clear selection so the Outliner/Properties don't highlight a random
    #   light for the whole video.
    for o in bpy.data.objects:
        try:
            o.select_set(False)
        except Exception:
            pass
    try:
        bpy.context.view_layer.objects.active = None
    except Exception:
        pass
    cam_obj = bpy.data.objects.get("MainCam")
    if cam_obj is not None:
        cam_obj.hide_viewport = True
    print("V2: setup complete: editor", (S["ed"].x, S["ed"].y, S["ed"].width, S["ed"].height),
          "viewport", (S["vp"].x, S["vp"].y, S["vp"].width, S["vp"].height), flush=True)
    return True, "ok"


# ---------------------------------------------------------------- tick
def tick():
    import time as _time
    ph = S["phase"]
    if ph == "setup":
        try:
            kind, oy, oh = do_setup()
            S["v_orig"] = (oy, oh)
            S["phase"] = "vsplit_wait"
            print("V2: vsplit called", flush=True)
        except Exception:
            import traceback
            traceback.print_exc()
            S["phase"] = "failed"
        return 0.8
    if ph == "vsplit_wait":
        try:
            ok, msg = finish_setup()
            print("V2: finish_setup:", ok, msg, flush=True)
            if not ok:
                open(SETUP_BAD, "w").write(msg)
                S["phase"] = "failed"
                return None
            S["phase"] = "hsplit_wait"
        except Exception:
            import traceback
            traceback.print_exc()
            S["phase"] = "failed"
        return 0.8
    if ph == "hsplit_wait":
        try:
            ok, msg = finish_hsplit()
            print("V2: finish_hsplit:", ok, msg, flush=True)
            if not ok:
                open(SETUP_BAD, "w").write(msg)
                S["phase"] = "failed"
                return None
            for p in (SETUP_DONE,):
                open(p, "w").write("ok")
            S["phase"] = "wait_start"
            print("V2: SETUP DONE, waiting for start flag", flush=True)
        except Exception:
            import traceback
            traceback.print_exc()
            S["phase"] = "failed"
        return 0.5
    if ph == "wait_start":
        if os.path.exists(START_FLAG):
            S["t0"] = _time.monotonic()
            S["phase"] = "run"
            # t=0 state: finished scene + orbit angle 0 + empty editor
            set_frame(900)
            set_view_rot(INIT_ROT)
            print("V2: STARTED, t0 set", flush=True)
            return 0.05
        return 0.5
    if ph == "run":
        t = _time.monotonic() - S["t0"]
        if t >= TOTAL:
            open(DONE_FLAG, "w").write("done")
            S["phase"] = "done"
            print("V2: DONE at t=720", flush=True)
            return None
        apply_state(t)
        return 0.05
    return None


def apply_state(t):
    # ---- result-first orbit 0-30 s
    if t < 30.0:
        set_frame(900)
        ang = (t / 30.0) * 2 * math.pi
        set_view_rot(Quaternion((0, 0, 1), ang) @ INIT_ROT)
        if t >= 2.0 and t < 22.0:
            type_header(t)
        elif t >= 22.0:
            if not S["parked"]:
                type_header(22.0)  # finish any trailing header chars
                # park on s1 KEY line (line 1, 0-based 0)
                try:
                    S["daily"].cursor_set(0, character=0)
                except Exception:
                    pass
                move_to_cursor()
                S["parked"] = True
        return
    # ---- teaching restart at 30 s (once)
    if not S["cleared"]:
        S["daily"].clear()
        S["cur_block"] = "daily"
        sp = ed_space()
        if sp is not None:
            sp.text = S["daily"]
        set_frame(0)
        S["state_frame"] = 0
        set_view_rot(INIT_ROT)
        S["parked"] = False
        S["cur_step"] = None
        S["typed_chars"] = 0
        S["cleared"] = True
        print("V2: teaching restart at 30 s (text cleared, frame 0)", flush=True)
    # ---- outro orbit 680-720 s
    if t >= OUTRO_START:
        set_frame(900)
        ang = ((t - OUTRO_START) / (TOTAL - OUTRO_START)) * 2 * math.pi
        set_view_rot(Quaternion((0, 0, 1), ang) @ INIT_ROT)
        if S["parked"]:
            # cursor back to end for outro hold
            cursor_to_end(S["daily"])
            move_to_cursor()
            S["parked"] = False
        return
    # ---- teaching steps (window = [ts, next step's ts), so None steps
    # keep their dwell: typing, then formation if any, then parked hold)
    set_view_rot(INIT_ROT)
    # ROBUST state frame: the latest formation whose end time has passed.
    # (Do NOT rely on a tick landing inside a short dwell window — a delayed
    # tick can skip a 0.5-1 s dwell entirely, and a step with fe == next_ts
    # has no dwell window at all. This scan makes the held frame correct
    # for ANY tick timing, as soon as t passes each formation's end.)
    for s in STEPS:
        if s[6] <= t and s[5] is not None:
            if s[5][0] == "frames":
                S["state_frame"] = s[5][2]
            else:
                S["state_frame"] = s[5][1]
    step = None
    for i, s in enumerate(STEPS):
        next_ts = STEPS[i + 1][3] if i + 1 < len(STEPS) else OUTRO_START
        if s[3] <= t < next_ts:
            step = s
            break
    if step is None:
        # true gap between steps (e.g., 78-90, 142-150): hold state, parked
        set_frame(S["state_frame"])
        return
    sid, block, lines, ts, te, form, fe = step
    # step change: reset typed counter, handle block switch
    if S["cur_step"] != sid:
        S["cur_step"] = sid
        S["typed_chars"] = 0
        S["sep_pending"] = sid
        switch_block(block)
        print(f"V2: step {sid} at t={t:.1f}", flush=True)
    if t < te:
        type_upto(step, t)
        set_frame(S["state_frame"])
    else:
        if not S["parked"]:
            type_upto(step, te)  # finish any trailing chars, then park
            park_on_key(sid, block)
        if form is not None and t < fe:
            # formation: play frames time-based
            if form[0] == "frames":
                f0, f1 = form[1], form[2]
                f = f0 + (t - te) / (fe - te) * (f1 - f0)
                set_frame(int(round(f)))
            else:  # still
                set_frame(form[1])
        else:
            # dwell / post-formation hold
            if form is not None:
                if form[0] == "frames":
                    set_frame(form[2])
                    S["state_frame"] = form[2]
                else:
                    set_frame(form[1])
                    S["state_frame"] = form[1]
            else:
                set_frame(S["state_frame"])


def type_header(t):
    """s1 header lines typed 2-22 s into daily block (pre-clear)."""
    if S["parked"]:
        return
    text = "\n".join(S1_LINES)
    total = len(text)
    per = 20.0 / max(1, total)
    target = total if t >= 22.0 else int((t - 2.0) / per)
    target = max(0, min(total, target))
    start = S["typed_chars"]
    if target > start:
        chunk = text[start:target]
        for ch in chunk:
            S["daily"].write(ch)
            if ch == "\n":
                move_to_cursor()
        S["typed_chars"] = target


bpy.app.timers.register(tick, first_interval=3.0)
print("V2: presenter registered", flush=True)
