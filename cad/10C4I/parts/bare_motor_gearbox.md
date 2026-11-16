# Bare-motor 2-stage gearbox ×2 (not modeled yet)

**Status:** the concept and the parts list are settled, but there's **no CAD yet**. It's blocked on measurements of Pololu's pinion (below).

**Why it exists:** two of the four motors are bare Pololu #4690s (24 V, 10,000 RPM free, ~0.55 kg·cm stall) with no gearbox. They need a fixed ~18.75:1 printed reduction so they match the #4691 19:1 gearmotors on the other corners. Mecanum drifts if the corners don't match.

## Concept

```
bare motor ─► Pololu helical pinion ─► [stage 1: printed helical gear ~4.3:1]
                                             │  (intermediate 5 mm hex shaft)
                                             ▼
                                      [stage 2: printed spur pinion → gear ~4.3:1]
                                             │  (output 5 mm hex shaft, through the chassis wall)
                                             ▼
                                        REV hex adapter → wheel
```

- **Why two stages:** a single 18.75:1 stage (10T to 188T) needs a ~94 mm gear. That's bigger than the 75 mm wheel, so it would hit the floor. Two stages of ~4.3:1 keep the largest gear around 43 mm.
- **Stage 1:** a printed helical gear matched to Pololu's pinion. The pinion is permanently fixed to its 2 mm shaft, so keeping it was the only option.
- **Stage 2:** spur gears with bigger teeth, since this stage carries about 4× the torque.
- **Shafts:** both run in REV flanged bearings on 5 mm hex shafts.
- **Load target:** survive Pololu's own gearbox rating, 10 kg·cm continuous and 25 kg·cm in short bursts. Output is ~530 RPM and ~10 kg·cm at stall.
- **Layout (proposed, not confirmed):** both bare motors on the same axle, for example the rear. Then the front end section stays as is, and only the rear becomes a new variant with gearbox mounts.

## Known motor geometry (Pololu #4690/#4750 drawing)

- 6× **M2.5** threaded holes in the face, on a ~26.5 mm circle, **3.5 mm max** depth
- Pinion is 5 mm long and ends 9 mm from the motor face, with an 8 mm boss at the base, on a 2 mm shaft
- Pinion tip diameter is ~6.0 mm per Pololu's CAD, which shows it as a plain cylinder

## Needed before modeling

- [ ] Pinion **tooth count** (mark one tooth)
- [ ] Diameter **across the tooth tips** (calipers)
- [ ] **Helix hand:** with the shaft up, do the teeth lean `/` or `\`?
- [ ] A sharp side photo of the pinion with a ruler in frame (for the helix angle)
- [ ] Confirm both bare motors go on the same axle

## Parts to buy (~$55 from REV)

| Part | Qty needed | Pack | ~Price |
|---|---|---|---|
| 8×12×3.5 flanged bearings (REV-49-1559) | 8 | 10-pack | $18.50 |
| 5 mm hex to 8 mm round bearing inserts (REV-41-1528) | 8 | 20-pack | $11.00 |
| 5 mm × 90 mm hex shaft (cut to length with a Dremel; it's stainless) | 4 | 4-pack | ~$13 |
| Shaft collars (Slim if in stock) + 1.5 mm hex key | as needed | 10-pack | $9.75 |
| Plain nylon (PA12/PA6, **not** CF) for the gears | 50–100 g | spool | $30–50 |
| PTFE grease (Super Lube) | – | – | ~$10 |
| M2.5 screws, motor to housing (length TBD, under 3.5 mm engagement) | 12 | – | – |

Print the gears in plain nylon. Carbon fiber grinds down both the printed teeth and the steel pinion.
