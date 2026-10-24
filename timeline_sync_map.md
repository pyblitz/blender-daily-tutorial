# PyBlitz Daily Tutorial — SYNC VERSION: shared timeline map

One timeline drives all three tracks. A viewport event NEVER starts
before its code line finishes typing: formation starts at the typing
completion timestamp, and the section voice line overlaps that same
typing + formation window. Viewport = real Blender 4.5.15 LTS
animation frames (formation.py keyframes), NOT stills — except the
two labelled still holds (clean = empty frame; solidify = one frame
where vertex markers switch off). Lighting ramp = EEVEE frames,
because Workbench shading cannot visualise scene lights.
Editor = PIL rendering of the real script text, typed character by
character (not a Blender screenshot). Split: LEFT 40% editor (768 px),
RIGHT 60% viewport (1152 px). Total 720 s, 1920x1080, H.264 + AAC.

| Step | Section | Code typed | Typing window | Typing completes | Viewport event at that moment |
|---|---|---|---|---|---|
| s1_header | Intro & Hook | `# RESULT FIRST: finished scene` (+2 lines) | 2.0–22.0 s | 22.0 s | RESULT-FIRST preview: final-scene orbit loop (24 Blender orbit frames @12 fps) 0–30 s while result lines type; teaching restarts from empty at 30 s |
| s2_import | Environment & Script Setup | `import bpy` (+3 lines) | 30.0–48.0 s | 48.0 s | holds previous state (empty (teaching restart)); no new shape (comment/setup line) |
| s2_clean | Environment & Script Setup | `bpy.ops.object.select_all(` (+4 lines) | 48.0–78.0 s | 78.0 s | still empty_0000.png holds 78.0–80.0 s (clean = empty; solidify = markers off) |
| s3_cube | Generating 3D Shapes | `blue = neon_material(` (+5 lines) | 90.0–140.0 s | 140.0 s | Blender frames f_0010–f_0057 play at 24 fps: object scales 0→1 (140.0–142.0 s) |
| s3_sphere | Generating 3D Shapes | `purple = neon_material(` (+5 lines) | 150.0–195.0 s | 195.0 s | Blender frames f_0070–f_0117 play at 24 fps: object scales 0→1 (195.0–197.0 s) |
| s3_cyl | Generating 3D Shapes | `cyan = neon_material(` (+6 lines) | 205.0–258.0 s | 258.0 s | Blender frames f_0130–f_0177 play at 24 fps: object scales 0→1 (258.0–260.0 s) |
| s4_verts | Custom Mesh From Data | `# Our own pyramid: base + apex` (+4 lines) | 270.0–315.0 s | 315.0 s | Blender frames f_0190–f_0249 play at 24 fps: object scales 0→1 (315.0–317.5 s) |
| s4_faces | Custom Mesh From Data | `faces = [(0, 1, 2, 3), (0, 1, 4),` (+2 lines) | 320.0–355.0 s | 355.0 s | Blender frames f_0262–f_0309 play at 24 fps: object scales 0→1 (355.0–357.0 s) |
| s4_mesh | Custom Mesh From Data | `mesh = bpy.data.meshes.new(` (+10 lines) | 360.0–392.0 s | 392.0 s | still solid_0320.png holds 392.0–394.0 s (clean = empty; solidify = markers off) |
| s5_move | Humanoid Character | `# Slide demo shapes aside` (+3 lines) | 400.0–412.0 s | 412.0 s | Blender frames f_0332–f_0367 play at 24 fps: object scales 0→1 (412.0–413.5 s) |
| s5_legL | Humanoid Character | `# Legs: two cylinders` (+3 lines) | 414.0–426.0 s | 426.0 s | Blender frames f_0380–f_0415 play at 24 fps: object scales 0→1 (426.0–427.5 s) |
| s5_legR | Humanoid Character | `leg_r = add_cyl('Leg_R',` (+2 lines) | 428.0–440.0 s | 440.0 s | Blender frames f_0420–f_0455 play at 24 fps: object scales 0→1 (440.0–441.5 s) |
| s5_torso | Humanoid Character | `# Torso: a box, scaled tall` (+3 lines) | 442.0–456.0 s | 456.0 s | Blender frames f_0468–f_0503 play at 24 fps: object scales 0→1 (456.0–457.5 s) |
| s5_armL | Humanoid Character | `# Arms: two cylinders` (+3 lines) | 458.0–470.0 s | 470.0 s | Blender frames f_0516–f_0551 play at 24 fps: object scales 0→1 (470.0–471.5 s) |
| s5_armR | Humanoid Character | `arm_r = add_cyl('Arm_R',` (+2 lines) | 472.0–484.0 s | 484.0 s | Blender frames f_0556–f_0591 play at 24 fps: object scales 0→1 (484.0–485.5 s) |
| s5_head | Humanoid Character | `# Head: a sphere` (+2 lines) | 486.0–498.0 s | 498.0 s | Blender frames f_0604–f_0639 play at 24 fps: object scales 0→1 (498.0–499.5 s) |
| s5_eyeL | Humanoid Character | `# Eyes: two tiny spheres` (+3 lines) | 500.0–510.0 s | 510.0 s | Blender frames f_0652–f_0675 play at 24 fps: object scales 0→1 (510.0–511.0 s) |
| s5_eyeR | Humanoid Character | `eye_r = add_sphere('Eye_R',` (+2 lines) | 512.0–522.0 s | 522.0 s | Blender frames f_0680–f_0703 play at 24 fps: object scales 0→1 (522.0–523.0 s) |
| s5_done | Humanoid Character | `# Same pattern, arranged` (+2 lines) | 523.0–552.0 s | 552.0 s | holds previous state (s5_eyeR formed); no new shape (comment/setup line) |
| s6_core | Materials / Lighting / Rendering | `# Chest core: a glowing sphere` (+2 lines) | 560.0–572.0 s | 572.0 s | Blender frames f_0716–f_0739 play at 24 fps: object scales 0→1 (572.0–573.0 s) |
| s6_body | Materials / Lighting / Rendering | `# Dark material for the body` (+3 lines) | 574.0–596.0 s | 596.0 s | Blender frames f_0752–f_0775 play at 24 fps: object scales 0→1 (596.0–597.0 s) |
| s6_eyes | Materials / Lighting / Rendering | `# Cyan eyes and chest core` (+3 lines) | 598.0–616.0 s | 616.0 s | Blender frames f_0800–f_0823 play at 24 fps: object scales 0→1 (616.0–617.0 s) |
| s6_light | Materials / Lighting / Rendering | `# Sun + blue and purple areas` (+10 lines) | 618.0–665.0 s | 665.0 s | EEVEE frames light_0840–light_0887: sun + area energies ramp 0→full (665.0–667.0 s) |

## Voice placements (all Piper en_US-ryan-medium; exact spec lines verbatim)

- s1_exact: 1.0–8.2 s — Welcome back! Today, we are building 3D elements in Blender purely through Python code. No mouse needed—just pure code. Let's get started!
- s1_fill: 15.0–19.4 s — By the end, you will have a character built entirely from code, with materials and lights.
- s2_exact: 31.0–38.1 s — First, we switch to Blender's Scripting workspace and import the bpy library, which allows Python to control the 3D viewport.
- s2_fill: 55.0–60.3 s — We open a new text block, type import bpy, and clear the scene, so every run starts clean.
- f_clean: 70.0–74.0 s — Every run starts clean, so the same script always builds the same scene.
- s3_exact: 91.0–98.3 s — Next, we write functions to spawn primitive meshes—cubes, spheres, and cylinders—positioning them accurately using coordinate parameters.
- f_cube: 139.0–141.5 s — And there it is. The cube, right at the origin.
- s3_fill: 160.0–168.3 s — The cube sits at the origin. The sphere moves to X equals three. The cylinder moves to X equals minus three. Change one number, and the object moves.
- f_sphere: 194.0–196.8 s — The sphere appears beside it, at X equals three.
- f_cyl: 257.0–260.4 s — And the cylinder, on the other side, at X equals minus three.
- s4_exact: 271.0–288.2 s — Primitives are fast, but what if you want a shape Blender does not give you? Then you describe the shape yourself. Vertices for the corners, faces for the surfaces, and one call, from_pydata, turns your lists into a real mesh. Wrap it in an object, put it in its own collection, and it is part of your scene. That is how every custom procedural shape begins.
- f_verts2: 295.0–298.9 s — Four corners for the base, plus one apex on top. Five points in total.
- f_pyr_points: 314.0–317.3 s — Five points appear. Four for the base, one for the apex.
- f_pyr_faces: 354.0–356.7 s — Now the faces fill in, and the pyramid takes shape.
- f_pyr_solid: 391.0–395.0 s — Wrapped in an object, linked to its own collection. A real custom mesh.
- s5_exact: 401.0–409.2 s — Now, let's combine these basic elements into a low-poly character structure, defining torso, head, and limbs automatically using procedural code.
- f_move: 411.0–414.0 s — We slide the demo shapes aside, to make room for the character.
- s5_fill: 430.0–440.4 s — Two cylinders for the legs. A box for the torso. Two more cylinders for the arms. A sphere for the head, and two tiny spheres for the eyes. Same pattern as before, just arranged like a person.
- f_torso: 453.0–456.5 s — The torso is a box, scaled tall, sitting on the legs.
- f_arms: 478.0–480.4 s — Two cylinders for the arms, left and right.
- f_head: 497.0–499.1 s — A sphere for the head, sitting on the torso.
- f_eyes: 521.0–524.1 s — Two tiny spheres for the eyes, and the character is assembled.
- f_assembled: 535.0–539.4 s — Legs, torso, arms, head, eyes. The character stands on its own.
- s6_exact: 561.0–567.1 s — Finally, we attach shader materials, set base colors, and add studio lighting to finalize our 3D render.
- f_body_mat: 595.0–597.7 s — Watch the body turn dark, as the material applies.
- f_eye_mat: 615.0–617.4 s — And the eyes and chest core light up cyan.
- s6_fill: 620.0–628.2 s — Dark material for the body, bright cyan for the eyes and chest core, then a sun lamp and two coloured area lights, blue and purple, for the studio look.
- f_light_detail: 632.0–636.3 s — Sun first, then two area lights. Blue on one side, purple on the other.
- f_light: 664.0–667.9 s — Now the studio lights fade up, blue and purple, and the render comes alive.
- s7_exact: 681.0–689.7 s — That's how easy it is to program 3D models in Blender using Python. Download the code in the description, subscribe for daily tutorials, and see you tomorrow!

## Outro
- 680–720 s: 360° orbit only (24 Blender orbit frames at 12 fps, looped). No typing. Voice s7_exact 681–689.7 s.

## Formation keyframes (formation.py, 24 fps Blender timeline)
- cube 10–57, sphere 70–117, cylinder 130–177, pyramid vertices 190–249 (12 f each),
  pyramid mesh 262–309, markers off 320, demo move 332–367, legs 380–415 / 420–455,
  torso 468–503, arms 516–551 / 556–591, head 604–639, eyes 652–675 / 680–703,
  chest core 716–739, body materials 752–775, eye/core materials 800–823, lights 840–887.

## Explainer style applied (inside the sync build, content still original)
- (1) Result FIRST: 0–30 s final-scene orbit preview while result lines type; teaching restarts from empty at 30 s.
- (2) Full-screen 1080p: 1920x1080, editor 768 px + viewport 1152 px, both legible; no tiny boxes.
- (3) Split-screen code-left / viewport-right throughout instruction + result (40/60).
- (4) Voice-forward: voice full level, real keyboard bed at 0.12, no music competing.
- (5) Captions burned bottom-center, MarginV=90 (clear of YouTube bottom UI); editor limited to 28 lines so captions never overlap code.
- (6) Visible cursor: typing cursor moves char by char; during formation/dwell the cursor parks on the highlighted causal line (KEY map above).
- (7) Same loop every step: result preview (0–30 s) then per step code types → formation (updated result); dwells trimmed (longest showcase hold 13 s at 667–680 s).
- (8) Chapters: 7 chapters embedded in the mp4 + listed in the SEO pack description.
- (9) Typing READABLE (slowest steps ~3–5 chars/s) with CLEAR real keyboard sound (0.12, under voice, no beeps) — not the reference's faint typing.
- (10) No copied reference content: all code/words are this project's own Blender Python script; reference style guide used for style points only.
