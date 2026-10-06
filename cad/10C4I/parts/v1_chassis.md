# Chassis v1 (superseded)

**Status:** replaced by v2. Its files are **not** in the repo. This page records what it was and why it changed.

v1 was a first pass built entirely on **assumed** dimensions, before the real part files and datasheets were available. It kept the same idea: 3 printed sections, with front and rear as the same part.

| | v1 | v2 |
|---|---|---|
| Parts | center ×1, end ×2, motor cap ×4, splice plate ×2 | center ×1, end ×2, motor cap ×4, wheel adapter ×4 |
| Body | 420 × 190 × 30 (200 center + 2 × 110 ends) | 356 × 170 × 49 (3 × 118.7) |
| Wheels | assumed 100 mm, 45 wide | real REV DUO 75 mm |
| Motor clamp | around the Ø37 "can" (assumed) | around the Ø36.8 gearbox, from Pololu's STEP |
| Joints | stepped lap, tongue/groove, 8× M5 flange bolts, bottom splice plate | 45° lap lip, diamond pegs, 8× M2.5 into inserts |
| Fasteners | M5 / M4 / M3 inserts | M3 at motor faces only, M2.5 + inserts everywhere else |
| Battery | no bay; flat deck with a 44-hole M3 insert grid | in a bay inside the center section |
| Cross grid | on the underside | on the top face, to match the reference photo |

## Why it changed

- The real Pololu STEP showed the can is Ø34.8, not 37, so the v1 clamp would have been loose. The M3 face threads are also only 3 mm deep.
- The real wheels are 75 mm with a specific hub pattern, which changed the axle height, track and adapter.
- The design constraints were set: fit the MK4S bed in equal sections, cross grid like the reference, M2.5 everywhere except the motor faces, and a MacBook-sized footprint.
- The battery moved inside for a lower CG and a free top deck.
