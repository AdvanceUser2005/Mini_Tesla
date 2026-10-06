# 10C4I Chassis: Design Decisions

Oct 5, 2026 · Daksh Gupta

> **How this was made:** I set the requirements, chose and supplied the parts (with their CAD models), and designed the first version of the chassis (MINI_T_V3). Claude (Anthropic's AI assistant) was used to help generate part of the design and to improve on my version: the parametric CadQuery model, the automated fit and interference checks, the print files and parts of this write-up. Every design decision was reviewed and directed by me.

## Overview

The 10C4I is a 356 × 310 mm indoor mecanum robot (279 mm across the body, 310 mm across the wheels). Its 3D-printed chassis carries an ASUS Zephyrus G14 laptop as the main computer, 8 ToF sensors, 1 to 4 mmWave radars and an OAK-D Lite camera. Every decision below traces back to one of these hard constraints:

| Constraint | What it forced |
| --- | --- |
| Prusa MK4S bed (250 × 210 × 220 mm) | Chassis split into 3 bolted sections plus bolt-on parts, all support-free |
| "Insane loads", long life | X-braced rib grids, lap joints with pegs, heat-set inserts instead of screws into plastic |
| M2.5 everywhere printed; M3/M4 only where a bought part dictates | One screw size, one insert type, one hex key for almost the whole robot |
| Real parts, not guesses | Pololu, Cytron, Adafruit, Luxonis and TI STEP files placed in the CAD and interference-checked |
| Laptop on top, lid open or closed | A ribbed deck above a 50 mm electronics bay |
| Sensors removable and reachable from outside | Every sensor sits on its own pod or cradle, held by outside screws |
| Ask, don't assume | Open questions were asked (motor ratio, battery, radar count, laptop model) before building |

## How the design evolved

The chassis went through six versions. Each one was driven by a new requirement or a problem found in the previous one, newest first:

| Version | What changed | Why |
| --- | --- | --- |
| FINAL rev 2 | Bolt-on side extensions fill the gap between the wheels; side ToFs and radar spots move onto them | Side ToF cones cleared the wheels by only ~2 mm, and the wheels sat about 5° inside the radar's 120° view |
| FINAL | Real Cytron MDD10A, VL53L1X and OAK-D Lite models placed; driver trays, breadboard tray, camera bracket redone | Parts pulled out of the MINI_T_V3 STEP replaced estimates |
| v5 | Radar cradle built around TI's IWR6843AOPEVM model: tip clip + 2 posts + 2 screws | The board's "holes" turned out to be edge notches; only 2 real holes |
| v4 | Battery out from below, removable sensor pods, body widened to laptop width (222 mm), 50 mm wiring bay | More room for wires and boards; sensors were buried too deep |
| v3 | Laptop deck replaces the Jetson/lidar layout; 8 ToF + radar + OAK-D | New requirement: carry the G14 laptop |
| v2 | Built around real Pololu 19:1 motors and REV mecanum wheels; printed wheel adapter with 8 inserts | Real parts replaced assumed ones |
| v1 | 3-section X-grid chassis to match the reference photo | First pass from photos |

## Splitting for the bed

The 356 mm robot is cut into three 118.7 mm sections across its length, because nothing longer than 250 mm fits the MK4S bed.

```
            Top view, front to the right (roughly to scale)

     [ wheel ]  [====== side extension 182 x 28.5 ======]  [ wheel ]
   +----------------+----------------+----------------+
   |                |                |                |
   |   REAR END     |    CENTRE      |   FRONT END    |   front -->
   |   118.7 x 222  |   118.7 x 222  |   118.7 x 222  |
   |  (front part,  |  battery bay,  |   2 motors,    |
   |  rotated 180)  |  hatch below   |  driver tray   |
   |                |                |                |
   +----------------+----------------+----------------+
                  joint            joint
     [ wheel ]  [====== side extension (same part) =====]  [ wheel ]
```

- **Equal lengths:** three equal sections spread the print time and keep each one well inside the bed.
- **Front and rear are the same part:** the rear section is the front one rotated 180°. That halves the design work, and one spare covers either end.
- **Width set by the laptop, not the bed:** the 222 mm sections only fit with their long side left to right, which the 250 mm X axis allows.
- **Bolt-on parts for everything wider:** the side extensions (182 × 28.5 mm) and the 2 deck halves add width and height without making any single print bigger than the bed.
- **Support-free:** every part prints in the orientation of its STL, using 45° undersides and bridges instead of supports.

## Structure

The chassis is an open-top box stiffened by an X-braced rib grid. That gives most of the strength of a solid block at a fraction of the plastic, and it matches the reference photo.

- **Box walls:** 5.5 mm sides, 5 mm bumpers, 6 mm bulkheads, 3 mm floor, all 49 mm tall. Tall thin walls tied by a floor and ribs act like an I-beam in bending.
- **X-grid:** 3 mm ribs in roughly 50 mm cells, crossed diagonally, with triangular windows in the floor. The diagonals take twist (one wheel on a bump) that a plain square grid would not.
- **Ladder ribs next to the joints:** inside the end sections, behind the joint, the ribs run straight with no diagonals. That keeps a clear lane to every joint screw (see Serviceability).
- **Section joints:** three things share the load at each joint. A 45° lap lip from the centre section hooks over the end section, which takes vertical shear. Two diamond pegs set the alignment. Eight M2.5 screws clamp the faces together. The 45° underside means the lip prints without support.
- **Full-height columns:** every top mounting point is an 8 mm column running from floor to top, so a load on top goes straight to the floor instead of tearing an insert out of a thin rib.
- **Gussets at the motors:** triangular webs tie each motor saddle to the side wall and floor, because the motors push the wheels' load into the walls.
- **Side extensions as rails:** each one bolts across both section joints, so it also stiffens the joints against bending.

## Fasteners and tolerances

Every printed joint is an M2.5 screw into a brass heat-set insert (Pofsnnx M2.5 × 4 × 3.5 OD). Screws cut directly into plastic strip after a few removals; inserts survive hundreds and spread the load into the surrounding plastic.

- **Only two exceptions:** M3 countersunk screws into the Pololu gearbox face (its threads are M3, max 3 mm deep, so the screws are 8 mm through a 5.5 mm wall), and M4 into the OAK-D Lite's back. Those threads are fixed by the bought parts.
- **Material around every insert:** each insert sits in at least 6 mm of solid plastic. Thin walls get a 3.5 mm pad on the inside, and the checks confirm ≥97 % of a ring around each insert is solid.
- **Inserts go in from an outside face:** every insert can be pressed in with a soldering iron before assembly, with nothing in the way.
- **Counts:** about 200 inserts and 8 screw sizes. M2.5 × 10 is the most common (68).

The tolerances are parameters at the top of the script, so one change regenerates every part:

| Fit | Value (mm) | Used for |
| --- | --- | --- |
| Insert hole | 3.1 | All heat-set inserts (pending the coupon) |
| M2.5 clearance | 2.9 vertical / 3.0 horizontal | Holes print slightly smaller when horizontal, so they get more room |
| M3 clearance + countersink | 3.4 / 6.4 | Motor faces |
| Sliding fit | 0.25 per side | Pegs, lap joint |
| Pocket fit | 0.2 per side | Sensor pods in their pockets |
| Gearbox bore | 37.2 | Motor clamp over the 36.8 mm gearbox |
| Bushing hole | 12.3 | Gearbox bushing (12.0 nominal) |

The tolerance coupon is printed first in the final material. Its results replace these values before the real parts are printed, because every printer and filament shrinks differently.

## Drivetrain

Four Pololu #4691 19:1 37D gearmotors with encoders drive REV 75 mm mecanum wheels. All four motors are identical, so the robot drives the same in every direction and one spare covers any wheel.

- **Clamped, not just bolted:** each gearbox sits in a printed saddle with a bolted cap (4 × M2.5 × 16) wrapped around it, and its face is held by 6 M3 screws. The face screws alone would put all the wheel load into 3 mm of thread; the clamp carries it through the gearbox can instead.
- **Encoder clocked out of the way:** each motor is clocked on its face so the encoder tab clears the saddle and the walls.
- **Install path designed in:** each motor slides 22.5 mm inboard, then back out until its bushing seats in the wall. The checks run the motor along that path to prove nothing blocks it.
- **Printed wheel adapter:** a D-bore hub (6.15 mm bore with a flat) on the 6 mm shaft, locked by a radial M2.5 set screw onto the flat. The wheel bolts to it with 8 M2.5 screws into inserts on the wheel's own hole pattern (4 on a 24 mm circle, 4 on 16 mm). A 7.8 mm pilot centres the wheel in its 8.1 mm bore.
- **3 mm gaps everywhere:** wheel to chassis, wheel to deck legs, wheel to side extensions. That is enough for rollers and print tolerance without making the robot wider.

## Laptop deck and electronics bay

The G14 (311 × 220 × 16.3 mm, 1.5 kg) lies lengthwise on a ribbed deck whose top is 110 mm above the chassis underside. Under the deck is a 50 mm clear bay for all the wiring and boards.

- **Why 50 mm:** the first deck sat lower, and you pointed out the wires, PCBs and boards would not fit. 50 mm clears the MDD10A drivers, the breadboard and connectors with room for cable bends.
- **Two identical halves:** the deck is 311 mm long, more than the bed, so it splits across the middle. The rear half is the front half rotated 180°, so there is one STL to print twice.
- **12 legs on inserts:** each half stands on 6 legs (12 mm, or 10 mm next to the wheels) that flare into the deck and screw into chassis-top inserts. Each half stands on its own, so there is no joint to fail between them.
- **Ribbed, windowed plate:** 3 mm plate on 8 mm ribs with X-cells and windows. It is stiff under 1.5 kg and lets the laptop's underside breathe, which matters because the G14 gets hot.
- **Lid open or closed:** 4 corner guards (2 tall at the front edge, 2 low at the hinge side so the screen can open) hold the laptop. Strap slots let you belt it down when the lid is closed.
- **Width:** the body is 222 mm, laptop width plus wall, as you asked.

## Power and control

The 6S 5200 mAh battery (156 × 54 × 45 mm) sits low in the middle of the centre section. That keeps the centre of gravity low and between the wheels.

- **Out from below:** you wanted the battery easy to remove. It drops out through a hatch in the floor, held by a 3 mm cover with 6 flat-head screws, so you never touch the laptop, deck or wiring to swap it. Bay walls run the full width as extra ribs, and stop posts keep the battery from sliding.
- **Breadboard right above it:** a full-size breadboard (Teensy 4.1 + TCA9548A I2C mux) sits on a tray over the bay, which you asked to keep clear. The tray screws into the bay walls and also holds the battery down from above (with 1 mm foam).
- **Motor drivers over their motors:** each Cytron MDD10A sits on a tray above its end section, centred between the two motors it drives. Motor wires stay short, and the high-current wiring is kept away from the breadboard's signal wiring. The tray sits on 4 new columns that the motor install path was re-checked against.
- **Everything under the laptop:** drivers, breadboard and mux all live in the 50 mm bay, so the laptop shields them and the top of the robot stays flat.

## Sensors

Every sensor sits on its own small printed pod or cradle that screws on from outside. You can swap a sensor, fix a cable or reprint a broken mount without opening the chassis.

| Sensor | Where | Why there |
| --- | --- | --- |
| 8 × VL53L1X ToF (27° view, 4 m) | 2 on each bumper (y ±84), 2 on each side extension (x ±78), all 44 mm above the floor | 2 per side, as you asked; bumper pairs flank the radar and camera |
| TI IWR6843AOPEVM radar (120° view) | Front bumper now; side and rear spots built in | 1 now, mounts for 4 later |
| OAK-D Lite | Bracket on the front bumper top, with a guard | Forward stereo view above the bumper sensors |

- **Pods sit in 2.5 mm pockets:** the pocket locates the pod, so screws only clamp. Each ToF pod has 3 screws and a slot for the STEMMA QT cable; the board mounts at your desk first.
- **Radar cradle built from TI's model:** the board has only 2 real holes (the others are edge notches), so the cradle holds it with a tip clip, 2 support posts and 2 screws. A groove on the back carries the 90° micro-USB cable into the wall.
- **OAK-D bracket:** the camera's USB-C port is on its bottom, so the bracket has a 12 mm base with a channel for a 90° plug, and the cable leaves out the back. Two horns and a low bar stick out 8 mm past the lens as a bumper guard.
- **Side extensions fix the field of view:** on the original 222 mm body, the side ToF cones cleared the wheels by only about 2 mm, and the wheels sat about 5° inside the radar's view. Mecanum rollers would have shown up as phantom obstacles. The bolt-on extensions fill the gap between the wheels and carry the sensors out to the wheel line, so the radar's front is level with the wheel faces and nothing is in any cone.
- **Nothing carbon-fibre in front of the radar:** CF blocks 60 GHz, so the radar always looks out through open air.

## Serviceability

Every screw has a tool path, and almost all of the robot goes together with one 2 mm hex key.

| Screws | How you reach them |
| --- | --- |
| Section joints (16) | Heads face into a 34 mm gap with no diagonal ribs and an open top; L-key from above, or a ball-end key through holes in the divider |
| Side extensions (16) | Straight driver through 6 mm access holes in the outer face; the screw head fits through the hole |
| Deck legs (12) | Down a 5.6 mm bore in each leg, about 55 mm deep; needs a long magnetised driver |
| Motor faces, M3 (24) | From outside, before the adapter and wheel go on |
| Motor caps, ToF pods, radar, breadboard tray, wheels | From above or outside, with nothing in the way |
| Battery cover (6) | From underneath |

A few screws get covered by the part mounted after them, so the assembly order matters:

1. Press all inserts (each from an outside face).
2. Motors, then motor caps.
3. Join the three sections.
4. Side extensions, then the side ToF pods and radar over their access holes.
5. Driver trays, then the MDD10A boards on top of their screws.
6. Battery, cover, breadboard tray.
7. Camera bracket, then the OAK-D on top of its screws.
8. Deck halves, corner guards, laptop.
9. Wheel adapter set screw, then the wheel over it.

## How it was verified

The whole chassis is one parametric Python script (CadQuery), and a separate check script tests the assembled model after every change. The final run reported no problems.

- **Interference:** every part against every other part, plus the real STEP models of the motors, drivers, ToF boards, radar board and camera. The result must be zero overlap.
- **Motion paths:** each motor is moved along its install path (12 and 22.5 mm inboard) to prove it can go in and out.
- **Tool paths:** a 7 mm key lane to every joint screw, a 5 mm driver path through each extension access hole, and a 2.4 mm screw shank through every extension screw hole.
- **Alignment:** pins through each driver-board and radar-board hole, M4 paths into the camera, USB plug and cable space under the camera, cable rods through the radar windows.
- **Insert strength:** a ring of material around each extension insert must be at least 97 % solid.
- **Fields of view:** ToF cones at 30° (27° + 3° margin) and radar cones at 130° (120° + 10°) are checked against the wheels.
- **Printability:** every part is a single valid solid that fits the 250 × 210 × 220 mm bed.
- **Key clearances:** 3.05 mm from extension to wheel, 3.12 mm from deck leg to wheel.

## Open items

- [ ] Print the tolerance coupon in the final material and update the insert hole and fits from it
- [ ] Pick the final material: PLA for the fit-check prototype, then PETG or PA612-CF (PLA softens near 55–60 °C, under a hot laptop and warm motors)
- [ ] Confirm the 90° cable directions: USB-C for the OAK-D, micro-USB for the radar
- [ ] Check whether the radar board needs a heatsink (TI's model shows none)
- [ ] Optional: move the camera-bracket screws out from under the camera
- [ ] Optional: add mouse ears to the big parts' corners to stop warping
- [ ] Order a second insert kit (about 200 needed, 120 in the current kit)
