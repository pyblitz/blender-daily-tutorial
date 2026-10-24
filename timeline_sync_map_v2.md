# PyBlitz Daily Tutorial — Timeline Sync Map v2 (REAL Blender GUI capture)

Supersedes the v1 sync map's BUILD METHOD only. Teaching content, voice
lines, typing windows, formation frame ranges, chapters, captions and SRT
timings are IDENTICAL to v1 (same schedule, same voice track). v1's file
`timeline_sync_map.md` is NOT overwritten — this is a separate v2 record.

## What changed vs v1 (the owner's 3 rejections, all fixed)

1. THEME IS NOT LIKE BLENDER (v1: PIL-rendered editor) → FIXED: there is
   NO PIL anywhere in v2. The whole screen is the REAL Blender 4.5.15
   window, captured live with ffmpeg x11grab: Text Editor (left, ~769 px)
   + Viewport (middle, ~813 px) + Outliner/Properties (right column) +
   Python Console (bottom-left strip) + Timeline (bottom strip) + top
   menu bar. Syntax highlighting, line numbers, cursor, gizmos, Timeline
   playhead and frame counter are all real Blender.
2. KEYBOARD SOUND IS NOT RIGHT (v1: 0.12 looped bed, ~27 dB below voice,
   not per-key) → FIXED: gated per-keypress clicks (see "Keyboard" below).
   Measured: keyboard during typing −33.6 dB mean in the final mix,
   ~18 dB below voice during speech (−15.1 dB), silent (−91 dB) in holds.
3. EVERYTHING MUST BE DONE ON BLENDER → FIXED except ONE disclosed
   15-second exception (see "Capture method" below): the light segment's
   viewport 3D area (665–680 s) shows pre-rendered EEVEE frames of the
   SAME scene, because live EEVEE viewport compile under Xvfb software GL
   is slow and the light ramp would be stepped/choppy. The editor side
   stays live GUI throughout, including during 665–680 s.

## Capture method (exact, honest)

- Machine: 2 cores, Blender 4.5.15 LTS portable, Xvfb display :97,
  1920×1080, ffmpeg x11grab @ 24 fps, libx264 ultrafast CRF 20 (capture),
  final re-encode libx264 fast CRF 18.
- Presenter: `presenter_v2.py` (in this repo). Wall-clock state machine
  (0.05 s ticks, absolute video time, no drift accumulation). Flag-gated:
  setup (fullscreen, vertical split editor/viewport, horizontal split
  editor/console so captions never overlap code, Timeline 1–900, view
  look-at framing) → setup_done → ffmpeg starts → start flag → t=0.
- Alignment: video t=0 = the first captured frame showing the finished
  scene (empty → finished transition, detected by bright-pixel count in
  the viewport 3D area, refined to ±1 frame). Capture 3 transition at
  capture 8.541667 s; cross-checked against the start-flag wall clock
  (0.44 s after the flag touch, inside the presenter's 0.5 s poll).
- Typing: real `Text.write()` char-by-char into the real Text Editor,
  readable speed (same windows as v1), cursor scrolled with a
  `text.move(LINE_END)` override after every line, parked on the step's
  causal (KEY) line during formation/dwell, unparked to end before the
  next step. One separator newline is written between steps (a missing
  separator in capture 1 merged step-boundary lines; fixed and verified).
- Formation: live `scene.frame_set()` time-based playback of the
  keyframed formation timeline (same frame ranges as v1). Held frame
  after each formation = the latest formation whose end time passed
  (robust scan every tick — a delayed tick can skip a 0.5–1 s dwell
  window, so the held frame is computed from time, never from dwell
  ticks; this fixed capture 2's one-eyed "character done" and grey-eyes
  holds).
- Result-first (0–30 s): editor types the header lines while the viewport
  orbits the finished scene (frame 900). Teaching restarts at 30 s
  (text cleared, frame 0, view reset). Outro (680–720 s): orbit again.
- Text blocks: `daily_tutorial.py` for s2/s3/s5/s6, `custom_mesh.py`
  (fresh block) for s4; the editor switches blocks at the s4/s5
  boundaries, like a real user would.
- Viewport chrome cleanup (Blender-native, not a fake): the scene camera
  object is hidden from the viewport (`hide_viewport`, rendering
  unaffected) because it sits between the view eye and the scene and its
  frustum wireframe would float across the frame; selection cleared so
  no random light stays highlighted. Light gizmos, empty axes and the 3D
  cursor remain visible (authentic viewport chrome).
- Workspace tab reads "Layout" (formation.blend's saved screen); the panel
  arrangement is the scripting arrangement (editor + viewport + console
  + timeline). Switching to the Scripting tab would replace this layout
  with Blender's default Scripting arrangement, so the tab name was left
  as-is; the arrangement is what the viewer sees.
- THE 15-SECOND EXCEPTION (665–680 s): the viewport 3D area ONLY
  (rect 820,57,764,918; header/toolbar/gizmo stay live GUI) is overlaid
  in post with real Blender 4.5.15 EEVEE-Next renders of the same scene:
  ramp light_0840–0887 @ 24 fps (665–667 s) + light_0887 hold
  (667–680 s), centre-cropped to the 3D-area aspect, no distortion.
  At 680 s the GUI viewport returns (frame 900, SOLID) for the outro
  orbit. Framing shifts slightly at 665 s because the EEVEE renders use
  MainCam while the GUI viewport uses the free view — same framing shift
  v1 had at its light segment, at a section boundary, narrated by the
  "lights fade up" voice line.
- NO other reuse: every other frame is live GUI capture. The v1
  pre-rendered formation frames were NOT composited into v2 (except the
  EEVEE light frames above, which are renders of this same scene).

## Keyboard (the fix for fault 2)

- Source: the REAL keyboard MP3 (`real-keyboard-typing.mp3`), onset
  detection (amplitude envelope, peak threshold 0.2×max, ≥0.06 s apart)
  → 64 distinct click samples (0.15 s windows, 5 ms fades).
- Placement: ONE click per visible keypress, at the presenter's char-tick
  times (typing window start + (i+0.5) × per-char, newlines included),
  2,809 clicks total across 23 typing windows (s1 header + 22 steps),
  round-robin samples, gain jitter 0.9–1.1.
- Mix: voice 1.0 + keyboard 0.8 (amix normalize=0), AAC 192k, mono
  22,050 Hz. Measured on the FINAL mix: voice+typing (91–98 s)
  mean −15.1 dB / max −0.5 dB (voice dominates); typing-only (100–130 s)
  mean −33.6 dB / max −4.2 dB (clearly audible, ~18 dB below speech, no
  clipping); silent hold (142–150 s) −91.0 dB (gating proven: zero
  keyboard outside typing windows). Stem check: typing window (100–130 s)
  −31.6 dB at gain 1.0 → −33.5 dB at gain 0.8 (matches the mix); hold
  window −91.0 dB. Old v1 bed was −49.3 dB (~27 dB below voice overall)
  and judged too faint; v2 is ~15 dB louder during typing, still below
  the voice. No beeps, no music, no songs.

## Voice

Piper en_US-ryan-medium, calm teacher. Same 6 exact lines + fillers as
v1; assembled track `audio/voice_track_sync.wav` (720.000 s) reused
as-is. Captions: `captions.ass` (ASS, PlayRes 1920×1080, bottom-centre
Alignment 2, MarginV 90, semi-transparent black box) burned in; the
editor's code area ends at top-down y≈847 and caption boxes start at
y≈900+, so captions never overlap code (verified in QC grabs). SRT:
51 sentence-level cues (same timings as v1, schedule unchanged).

## Chapters (7, same times as v1)

0–30 Intro & Hook — Result First · 30–90 Environment & Script Setup ·
90–270 Generating 3D Shapes · 270–400 Custom Mesh From Data ·
400–560 Humanoid Character · 560–680 Materials / Lighting / Rendering ·
680–720 Outro & Daily CTA.

## Schedule (same as v1; formation = Blender timeline frames @ 24 fps)

| Video time | Step | Typing | Formation | Formation end |
|---|---|---|---|---|
| 0–30 | s1_header (result-first orbit, frame 900) | 2–22 | orbit | 30 (clear, frame 0) |
| 30–48 | s2_import | 30–48 | — (empty hold) | 48 |
| 48–80 | s2_clean | 48–78 | still frame 0 | 80 |
| 90–142 | s3_cube | 90–140 | frames 10–57 | 142 |
| 150–197 | s3_sphere | 150–195 | frames 70–117 | 197 |
| 205–260 | s3_cyl | 205–258 | frames 130–177 | 260 |
| 270–317.5 | s4_verts (custom_mesh.py) | 270–315 | frames 190–249 | 317.5 |
| 320–357 | s4_faces | 320–355 | frames 262–309 | 357 |
| 360–394 | s4_mesh | 360–392 | still frame 320 | 394 |
| 400–413.5 | s5_move (back to daily_tutorial.py) | 400–412 | frames 332–367 | 413.5 |
| 414–427.5 | s5_legL | 414–426 | frames 380–415 | 427.5 |
| 428–441.5 | s5_legR | 428–440 | frames 420–455 | 441.5 |
| 442–457.5 | s5_torso | 442–456 | frames 468–503 | 457.5 |
| 458–471.5 | s5_armL | 458–470 | frames 516–551 | 471.5 |
| 472–485.5 | s5_armR | 472–484 | frames 556–591 | 485.5 |
| 486–499.5 | s5_head | 486–498 | frames 604–639 | 499.5 |
| 500–511 | s5_eyeL | 500–510 | frames 652–675 | 511 |
| 512–523 | s5_eyeR | 512–522 | frames 680–703 | 523 |
| 523–560 | s5_done | 523–552 | — (hold 703) | 552 |
| 560–573 | s6_core | 560–572 | frames 716–739 | 573 |
| 574–597 | s6_body | 574–596 | frames 752–775 | 597 |
| 598–617 | s6_eyes | 598–616 | frames 800–823 | 617 |
| 618–680 | s6_light | 618–665 | GUI hold 823; EEVEE overlay 665–680 | 665/680 |
| 680–720 | outro (orbit, frame 900) | — | orbit | 720 |

KEY (causal) lines parked on during formation/dwell, 0-based within
step: s1 0 · s2_import 0 · s2_clean 2 · s3_cube 2 · s3_sphere 2 ·
s3_cyl 2 · s4_verts 1 · s4_faces 0 · s4_mesh 2 · s5_move 0 · s5_legL 1 ·
s5_legR 0 · s5_torso 1 · s5_armL 1 · s5_armR 0 · s5_head 1 · s5_eyeL 1 ·
s5_eyeR 0 · s5_done 1 · s6_core 1 · s6_body 3 · s6_eyes 1 · s6_light 1.

## QC (final file, 15 grabs inspected, all PASS)

- t=15 result-first: header typing + finished scene orbiting (frame 900)
  + caption, no code overlap. PASS.
- t=100 typing hold: s2+s3_cube lines typing, viewport empty (frame 0).
  PASS.
- t=141 cube: cursor on `primitive_cube_add`, teal cube forming
  (frame 33, exact), caption "The cube, right at the origin." PASS.
- t=196 sphere: cursor on `primitive_uv_sphere_add`, sphere forming
  (frame 83; ideal 93 — transient tick lag ~0.45 s, see Limitations).
  PASS.
- t=259 cyl: cursor on `primitive_cylinder_add`, cylinder forming
  (frame 147; ideal 153, lag ~0.27 s). PASS.
- t=316 verts: editor switched to custom_mesh.py, cursor on `verts =`,
  vertex markers forming (frame 217; ideal 214). PASS.
- t=356 faces: cursor on `faces =`, pyramid mesh forming (frame 287;
  ideal 285). PASS.
- t=393 solid: cursor on `mesh.from_pydata`, solid pyramid (frame 320,
  markers hidden). PASS.
- t=427 legL: cursor on `leg_l = add_cyl`, leg forming (frame 397;
  ideal 403, lag ~0.26 s). PASS.
- t=457 torso: cursor on `torso = add_cube`, torso forming (frame 494;
  ideal 491). PASS.
- t=499 head: cursor on `head = add_sphere`, head sphere formed
  (frame 629; ideal 627). PASS.
- t=596 body: cursor on `o.data.materials.append(DARK)` (grab at the
  exact typing-end boundary shows the last typing frame; park follows
  within ~0.05 s), viewport holding frame 739 pre-formation. PASS.
- t=616 eyes: cursor on `eye_l.data.materials.append(EYE)`, viewport
  holding frame 775 pre-formation, caption "eyes… light up cyan." PASS.
- t=666 light overlay: editor GUI (cursor parked on SUN `light_add`),
  viewport 3D area = EEVEE lit scene (cyan eyes + chest core, blue/purple
  lights), GUI header/toolbar/gizmo intact. PASS.
- t=700 orbit: full daily script, cursor at end, viewport orbiting
  (frame 900). PASS.
- Audio: voice above keyboard in every overlap (see Keyboard); typing
  windows audible, holds silent; audio present in every 120 s window
  except genuinely silent windows (0–1 s pre-voice, 700–701 s outro
  hold, both by schedule).
- File: 720.000 s, 1920×1080, H.264 + AAC mono 22,050 Hz, faststart,
  7 chapters, SRT 51 cues. Video frames 17,272 vs nominal 17,280 (8
  frames, 0.33 s of duplicated frames from x11grab under load; duration
  is timestamp-exact 720.000 s, sync unaffected).

## Limitations (stated plainly, not hidden)

1. Formation frames can lag the ideal schedule by up to ~0.5 s at an
   instant (presenter tick gaps under 2-core load + x11grab contention;
   observed: −0.45 s at t=196, −0.27 s at t=259, −0.26 s at t=427).
   Formations always complete by their end time and all holds are
   exact; the qualitative sync (shape forming while its code is shown)
   holds throughout. This is inherent to live GUI capture; v1's
   pre-rendered frames had no lag because they were cut, not played.
2. The 665–680 s viewport 3D area is EEVEE renders, not live GUI
   (framing shifts slightly at 665 s; MainCam vs free view). Everything
   else is live GUI.
3. The mouse pointer rests over the editor (I-beam) in most frames —
   authentic screen-recording chrome, not moved (moving it would need
   extra automation and risks disturbing the capture).
4. The pyramid is partially occluded by the demo shapes from this view
   angle in a few frames (same composition as v1's renders).
5. Workspace tab reads "Layout", not "Scripting" (see Capture method).

## Files

- Video: `blender-daily-tutorial-sync-long-v2.mp4` (720.000 s,
  1920×1080, H.264 + AAC, 34,435,944 bytes) + `.srt` (51 cues).
- Presenter: `presenter_v2.py` (this repo, NEW file).
- This map: `timeline_sync_map_v2.md` (this repo, NEW file).
- formation.py UNCHANGED (no re-push needed for it).
- Nothing uploaded anywhere. Show-first: upload only on the owner's OK
  for this v2 version.
