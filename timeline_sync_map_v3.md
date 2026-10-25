# PyBlitz Daily Tutorial — Timeline Sync Map v3 (VOICE-ONLY, LINE-SCHEDULED typing)

Supersedes v2's BUILD METHOD (typing pace + audio) only. Teaching content,
formation frame ranges, chapter times, voice track, SRT timings and captions
are IDENTICAL to v1/v2. v1's `timeline_sync_map.md` and v2's
`timeline_sync_map_v2.md` are NOT overwritten — this is a separate v3 record.

## Why v3 exists (owner's orders, 2026-10-25 ~03:21 UTC, direct chat)

Upload of v2 was STOPPED before upload and two fixes ordered, plus
best-of-best quality from internet research:
1. REMOVE the typing sound entirely — he calls it bekar. v3 audio is
   VOICE ONLY.
2. TYPING MUST BE PROPER — speed matched to the voiceover, line by line,
   readable pace, short pause after each line.
3. Best-of-best practices that fit his standing rules (see below).

## Fix 1 — Voice-only audio (typing sound fully removed)

- Sole audio source: `audio/voice_track_sync.wav` (720.000 s, Piper
  en_US-ryan-medium, unchanged — voice is NOT stretched or sped up).
- NO keyboard clicks, NO keyboard bed, NO music, NO beeps, NO songs
  anywhere in v3. The v2 gated-click mix was discarded, not reused.
- Measured proof on the FINAL v3 file (ffmpeg volumedetect):
  - Voice cue 6 window (32–37 s): mean −14.8 dB / max −0.5 dB (voice clear).
  - Voice cube cue (139–141.5 s): mean −14.9 dB / max −0.0 dB.
  - Typing-visual but voice-silent window (101–129 s, cube lines typing
    on screen, no voice cue): mean −91.0 dB / max −91.0 dB = digital
    silence. v2's same window measured −33.8 dB / max −4.2 dB (clicks).
    This is the decisive proof: where v2 clicked, v3 is silent.
  - Silent hold (143–149 s): −91.0 / −91.0 dB. Outro silence
    (695–710 s): −91.0 / −91.0 dB.
  - Note: a visual typing PAUSE that falls inside a voice cue (e.g.
    95–96.5 s, inside cue 9) correctly measures voice levels, not
    silence — the pause is visual (no new characters), the voice keeps
    speaking, and no clicks ride on top of it (proven by the silent
    windows above, which use the identical audio track).

## Fix 2 — Line-scheduled typing matched to the voiceover

### The honest constraint (measured, not assumed)

The voice track is sparse by design: only 156.7 s of voice in 720 s
(SRT cues), the rest is watching time. Per-step voice inside each typing
window ranges from 0.0 s (s5_legL, s5_armL, s5_eyeL — silent stretches
where the NEXT voice cue explains the assembled result) to 22.1 s
(s4_verts). A literal "each line finishes exactly when its voice line
finishes" is impossible for every line, because voice lines are 1–8 s
while code lines need readable typing time. v3 therefore implements the
achievable version, and reports it exactly:
- Typing is LINE-BASED, not a continuous char drip: a line types at a
  steady readable rate, then a PAUSE before the next line.
- The KEY (causal) line of each step completes and parks, and its
  formation plays, aligned to that step's voice cue(s) — formation ends
  are UNCHANGED from v2, so every formation/voice alignment is preserved.
- Reading time is supplied by the line pauses PLUS the parked KEY-line
  hold during formation and the following gap.

### Schedule (presenter_v3.py, computed from the fixed windows)

Rate band 5–11 chars/s. Pause = largest in {2.5, 2.0, 1.5, 1.0, 0.5,
0.25, 0.0} s that keeps the rate ≤ 11; if the computed rate falls below
5, the rate is floored at 5 and typing ends early with a parked KEY-line
hold until formation. Block-switch steps (s4_verts → custom,
s5_move → daily) get a 1.0 s switch hold, on top of the genuine gaps
that already precede them (260–270 s, 394–400 s).

| Step | Window | Chars | Rate c/s | Pause s | Typing ends | Formation ends | Voice in window |
|---|---|---|---|---|---|---|---|
| s2_import | 30–48 | 64 | 6.10 | 2.5 | 48.0 | 48 | 7.1 s (31–38) |
| s2_clean | 48–78 | 97 | 5.00 | 2.5 | 77.4 | 80 | 9.3 s (55–60, 70–74) |
| s3_cube | 90–140 | 187 | 5.00 | 2.5 | 139.9 | 142 | 8.3 s (91–98, 139–141) |
| s3_sphere | 150–195 | 206 | 6.34 | 2.5 | 195.0 | 197 | 9.3 s (160–168, 194–197) |
| s3_cyl | 205–258 | 205 | 5.39 | 2.5 | 258.0 | 260 | 1.0 s (257–260) |
| s4_verts | 270–315 | 127 | 5.00 | 2.5 | 306.4 | 317.5 | 22.1 s |
| s4_faces | 320–355 | 84 | 5.00 | 2.5 | 341.8 | 357 | 1.0 s (354–357) |
| s4_mesh | 360–392 | 283 | 10.48 | 0.5 | 392.0 | 394 | 1.0 s (391–394) |
| s5_move | 400–412 | 104 | 10.95 | 0.5 | 412.0 | 413.5 | 9.2 s (401–409, 411–414) |
| s5_legL | 414–426 | 93 | 10.33 | 1.0 | 426.0 | 427.5 | 0.0 s (silent stretch) |
| s5_legR | 428–440 | 70 | 10.00 | 2.5 | 440.0 | 441.5 | 10.0 s (430–440) |
| s5_torso | 442–456 | 97 | 10.21 | 1.5 | 456.0 | 457.5 | 3.0 s (453–457) |
| s5_armL | 458–470 | 95 | 10.56 | 1.0 | 470.0 | 471.5 | 0.0 s (silent stretch) |
| s5_armR | 472–484 | 94 | 10.44 | 1.0 | 484.0 | 485.5 | 2.4 s (478–480) |
| s5_head | 486–498 | 71 | 10.14 | 2.5 | 498.0 | 499.5 | 1.0 s (497–499) |
| s5_eyeL | 500–510 | 94 | 10.16 | 0.25 | 510.0 | 511 | 0.0 s (silent stretch) |
| s5_eyeR | 512–522 | 68 | 9.71 | 1.5 | 522.0 | 523 | 1.0 s (521–524) |
| s5_done | 523–552 | 88 | 5.00 | 2.5 | 545.6 | 552 | 5.5 s (521–524, 535–539) |
| s6_core | 560–572 | 95 | 10.56 | 1.5 | 572.0 | 573 | 6.1 s (561–567) |
| s6_body | 574–596 | 124 | 8.55 | 2.5 | 596.0 | 597 | 1.0 s (595–598) |
| s6_eyes | 598–616 | 124 | 10.33 | 2.0 | 616.0 | 617 | 1.0 s (615–617) |
| s6_light | 618–665 | 281 | 10.41 | 2.0 | 665.0 | 665/680 | 13.5 s (620–628, 632–636, 664–668) |
| s1_header | 2–22 | 58 | 5.00 | 2.5 | 18.6 | (orbit to 30) | cues 1–4 (1–8 s) + cue 5 (15–19 s) |

Reading holds where typing ends early (parked KEY line, block held until
formation): s4_faces 13.2 s (341.8→355), s4_verts 8.6 s (306.4→315),
s5_done 6.4 s (545.6→552), s2_clean 0.6 s, s3_cube 0.1 s.
v2 comparison (uniform drip, no pauses): rates swung 2.0–9.4 c/s
(s4_faces 2.40, s4_mesh 8.84, s5_eyeL 9.40) with no line pauses at all.
v3 rates sit in the 5–11 band with a pause after (almost) every line.

### Best-of-best practices applied (internet research, fitted to his rules)

- Per-segment timed sync: typing scheduled per step from measured voice
  durations and the fixed windows — never an average speed, never
  stretched audio (voice track untouched).
- Result payoff in the first 30 seconds: KEPT (0–30 s finished-scene orbit
  while header lines type; teaching restarts at 30 s).
- A visual change every 10–20 seconds: KEPT via the existing
  code→formation→result loop (no jump cuts added — they would break sync).
- Clean audio first (voice-only), captions second (sentence-level SRT,
  technical terms correct: from_pydata, primitive names, coordinates),
  current line highlighted (cursor parked on the causal line during
  formation — KEPT).
- Chapters KEPT (7, same times). Tight edits, no repeated points
  (content unchanged from v2).
- NOT applied, by his rules: background music (forbidden), pasted code
  blocks (typing stays live char-by-char), anything breaking the sync
  rule (code types → its shape forms, line by line).

## Capture method (exact, honest)

- Machine: 2 cores, Blender 4.5.15 LTS portable, Xvfb display :97,
  1920×1080, ffmpeg x11grab @ 24 fps, libx264 ultrafast CRF 20 (capture),
  final re-encode libx264 fast CRF 18, faststart.
- Presenter: `presenter_v3.py` (NEW file, derived from presenter_v2.py).
  Wall-clock state machine (0.05 s ticks, absolute video time). Setup,
  formation playback, orbit, block switching, separator newline, cursor
  parking: identical to v2 except the typing engine (line schedule above)
  and flag names (/tmp/v3_*). Log shows all 23 steps firing on schedule.
- Alignment: video t=0 = first captured frame showing the finished
  scene. Raw frame at 2.50 s shows empty scene (frame 0); raw frame at
  3.00 s already shows the finished scene (frame 900). Trim offset
  2.88 s (±0.13 s). Verified after post: t=141 grab shows cube forming
  (frame 32) with cursor parked on `primitive_cube_add` — see QC.
- Viewport = live GUI capture throughout, EXCEPT the same disclosed
  15-second exception as v2: 665–680 s viewport 3D area ONLY (rect
  820,57,764,918; header/toolbar/gizmo stay live GUI) overlaid in post
  with real Blender 4.5.15 EEVEE-Next renders of the SAME scene (ramp
  light_0840–0887 for 665–667 s + light_0887 hold to 680 s). Editor stays
  live GUI throughout, including 665–680 s. Framing shifts slightly at
  665 s (MainCam vs free view), at a narrated section boundary.
- Editor = REAL Blender Text Editor, typed live char-by-char. NO PIL
  anywhere. Workspace tab reads "Layout" (formation.blend's saved
  screen); the panel arrangement is the scripting arrangement, as in v2.
- Captions: `captions.ass` burned in (bottom-centre, MarginV 90, code
  area ends y≈847, captions start y≈900+). SRT: 51 sentence-level cues,
  timings identical to v2 (voice unchanged). Chapters: 7, exact times.

## QC (final file, 8 grabs visually inspected, all PASS; 18 extracted)

- t=15 result-first: header line 2 typing ("# Built by code - no" +
  cursor), finished scene orbiting (frame 900), cue-5 caption. PASS.
- t=95.5 LINE-PAUSE PROOF: cube line 1 (`blue = neon_material(`)
  complete, cursor on empty next line, line 2 NOT yet typed, viewport
  frame 0, cue-9 caption speaking. This is the 94.4–96.9 s pause. PASS.
- t=141 cube: cursor parked on `primitive_cube_add`, teal cube forming
  (frame 32; ideal 33, 1-frame lag), caption "The cube, right at the
  origin." PASS.
- t=316 verts: editor switched to custom_mesh.py, cursor on `verts =`,
  vertex markers forming (frame 211; ideal ~214, ~0.1–0.2 s lag). PASS.
- t=393 solid: cursor on `mesh.from_pydata`, solid pyramid (frame 320),
  caption "Wrapped in an object, linked to its own collection." PASS.
- t=499 head: cursor on head line, head sphere formed on torso
  (frame 629), caption "A sphere for the head, sitting on the torso." PASS.
- t=678 light-overlay tail: EEVEE lit scene still covering the viewport
  3D area 2 s before overlay end, GUI editor/header intact. PASS.
- t=700 outro: full script, cursor at end, finished scene orbiting
  (frame 900). PASS.
- Audio: voice above silence everywhere (see Fix 1); audio present in
  every voice window, silent in every voice gap and hold.
- File: 720.000 s, 1920×1080, H.264 + AAC mono 22,050 Hz, faststart,
  7 chapters, SRT 51 cues, 29,527,082 bytes.

## Deviations, failures, caveats (nothing hidden)

1. FIRST POST WAS MISALIGNED AND DISCARDED (caught by QC, never shown
   as final): the first post script placed `-ss` between inputs, which
   seeked the OVERLAY instead of the main video, leaving the video
   2.88 s behind voice/captions (proven by its t=141 grab: cube line
   still typing, viewport empty, while the caption already said the
   cube line). The script was fixed (`-ss` before the main input) and
   the file was fully re-encoded; the faulty file was overwritten by
   the corrected encode and does not remain as v3. The re-encode also
   fixed the overlay tail (the faulty run's seeked overlay clip was
   12.12 s, which would have dropped EEVEE coverage for ~677–680 s).
2. Tight-step pauses are short by necessity (fixed windows + formation
   anchors): s5_eyeL inter-line pause is only 0.25 s (94 chars in a
   10 s window at 10.16 c/s); s4_mesh/s5_move pauses are 0.5 s. Reading
   time there comes from the formation hold with the cursor parked on
   the KEY line, as documented above — not from longer pauses, which
   the windows cannot hold at a readable rate.
3. Transient formation lag ≤ ~0.5 s at instants (presenter tick gaps
   under 2-core load; observed: cube frame 32 vs ideal 33, verts frame
   211 vs ~214). Formations always complete by their end time and all
   holds are exact; inherent to live GUI capture.
4. Mouse pointer rests over the editor (I-beam) in most frames —
   authentic screen-recording chrome, left as-is.
5. Pyramid partially occluded by demo shapes from this view angle in a
   few frames (same composition as v2's renders).
6. Workspace tab reads "Layout", not "Scripting" (arrangement is the
   scripting arrangement; switching tabs would replace it).
7. Header typing ends at 18.6 s (rate floor 5 c/s) and holds parked to
   22 s; result-first orbit continues throughout — by design.

## Files

- Video: `blender-daily-tutorial-sync-long-v3.mp4` (720.000 s,
  1920×1080, H.264 + AAC, 29,527,082 bytes) + `.srt` (51 cues).
- Presenter: `presenter_v3.py` (NEW file).
- This map: `timeline_sync_map_v3.md` (NEW file).
- QC grabs: `qc_v3/` (18 files).
- formation.py UNCHANGED. v2 files (20:04), v1 files (18:32), rejected
  original (15:19), Lesson 1/2 files: all untouched (mtimes verified).
- Nothing uploaded anywhere. Show-first: upload only on the owner's OK
  for this v3 version.
