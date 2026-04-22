# Mini Tesla — Autonomous Mecanum Robot Platform

## Members
Daksh Gupta, Computer Engineering Student (2028)
mailtodaksh@vt.edu

## Mentor
MENTOR NAME HERE

## Current Status
IN PROGRESS

## Project Overview

The Mini Tesla is an autonomous omnidirectional robotic platform built on a four-wheel mecanum drivetrain, capable of moving in any direction — forward, lateral, diagonal, and rotational — without needing to reorient itself. The platform is designed as a full-stack research and engineering vehicle that bridges mechanical design, embedded systems, and autonomous robotics software.

At the mechanical core, the robot features a custom-built two-ratio gearbox designed and fabricated in-house, enabling adaptive gear shifting between high-speed flat terrain mode and high-torque incline traversal mode. The drivetrain uses four Pololu 37D bare DC motors (24V, 64 CPR encoder, no internal gearbox) feeding directly into the custom transmission — maximizing regenerative braking efficiency by eliminating the energy loss of a factory gearbox. Custom spring-damper shock absorbers are designed and tuned for outdoor terrain traversal, and a hydraulic braking circuit — engineered from first principles including master/slave cylinder sizing and fluid bleeding — provides active braking and hill-hold capability.

The autonomy stack runs on an NVIDIA Jetson Orin Nano Super (67 TOPS) executing ROS 2, with a Teensy 4.1 microcontroller handling real-time motor control, PID velocity loops, encoder feedback, and actuator commands over CAN/serial. Perception is handled by an Intel RealSense D435 RGB-D camera and an RPLIDAR A1 2D LiDAR, enabling SLAM-based mapping, Nav2 autonomous navigation, and an Automatic Emergency Braking (AEB) system via depth threshold detection. An AI pipeline running YOLO on the Jetson GPU enables object detection and person-following behavior. The robot also supports WiFi and Bluetooth remote control for manual override alongside full autonomous operation.

A digital twin of the platform is built in NVIDIA Isaac Sim, enabling hardware-in-the-loop (HIL) simulation and algorithm validation before deployment to the physical robot. The project spans three semesters — Spring, Summer, and Fall 2026 — with three defined milestones culminating in a full autonomous demonstration.

## Educational Value Added

This project develops hands-on expertise across six engineering disciplines simultaneously, making it one of the most comprehensive student robotics projects in scope:

**Mechanical Design & Manufacturing** — Students learn to design a multi-ratio planetary gearbox from scratch, understanding gear ratio theory, torque multiplication, and how automotive transmissions work at a fundamental level. Custom shock absorbers are designed using spring-damper physics, spring rate selection (k = F/x), and damping coefficient tuning. A hydraulic brake circuit is engineered from Pascal's Law up — including master/slave cylinder bore sizing, brake fluid selection, and system bleeding technique. FEA (Finite Element Analysis) is used to validate structural components before fabrication.

**Embedded Systems & Real-Time Control** — The Teensy 4.1 runs deterministic real-time firmware handling four simultaneous quadrature encoder interrupts, four independent PID velocity loops, PWM motor command output, servo control for the gear selector, and solenoid actuation for the hydraulic brake — all at 1 kHz without timing conflicts. Students learn CAN bus communication, hardware timer configuration, and interrupt-driven architecture.

**Robotics Software (ROS 2)** — The full ROS 2 stack is implemented from scratch: mecanum inverse kinematics node, wheel odometry, IMU-fused localization, SLAM mapping with RPLIDAR, and Nav2 goal-directed navigation with dynamic obstacle avoidance. Students learn node architecture, topic/service communication, and real-time sensor fusion.

**AI & Computer Vision** — YOLO object detection and person re-identification pipelines run on the Jetson GPU for human-following behavior. The AEB system uses raw RealSense depth data — not AI — for sub-25ms obstacle detection latency, teaching students the difference between classification tasks and safety-critical sensor pipelines.

**Simulation & Digital Twin** — NVIDIA Isaac Sim is used to build a full digital twin of the robot including geometry, sensors, and drivetrain physics. Students learn hardware-in-the-loop testing workflows and sim-to-real transfer techniques used in industry robotics development.

**Communications & Controls** — WiFi and Bluetooth modules provide remote control capability alongside the autonomous stack. Students implement mode-switching logic, teleop integration in ROS 2, emergency stop handling, and failsafe behavior.

## Tasks

### Spring 2026 (Now → May 13)
- [ ] Finalize BOM and place all component orders (motors, MCU, sensors, battery, structural hardware)
- [ ] CAD — Full chassis design in SolidWorks/Fusion 360
- [ ] CAD — Custom 2-ratio gearbox (planetary stages, selector collar, housing)
- [ ] CAD — Shock absorber assemblies (spring-damper bodies, mount points)
- [ ] CAD — Hydraulic brake system (caliper, rotor, master cylinder, lines)
- [ ] FEA — Structural analysis on chassis and gearbox housing
- [ ] Receive and inventory all ordered components
- [ ] Begin manufacturing drawings for CNC/3D print parts

### Summer 2026 (May 26 → July 6)
- [ ] 3D print and CNC machine all custom parts (gearbox bodies, shock housings, brake calipers)
- [ ] Full mechanical assembly — chassis, wheels, gearboxes, shock absorbers
- [ ] Wire all electronics — Teensy, motor drivers, IMU, LiDAR, RealSense, AI PC, WiFi/BT module
- [ ] Flash Teensy firmware — encoder interrupts, PID loops, CAN comms
- [ ] Validate mecanum kinematics — test all four motion vectors
- [ ] Test power regeneration — verify BTS7960 back-EMF current return
- [ ] Test gearbox shifting — servo-actuated selector under load
- [ ] Test hydraulic brakes — caliper engagement, hill-hold force
- [ ] Test remote control — WiFi/BT manual override
- [ ] Isaac Sim — build digital twin, run full-scale simulation tests
- [ ] **MILESTONE #2 target: June 13** — Assembly complete, all wiring done, basic subsystem testing done

### Fall 2026 (Aug 24 → Dec 16)
- [ ] Camera integration — RealSense depth layer into Nav2 costmap
- [ ] AEB system — depth threshold node with real-time priority, direct Teensy serial path
- [ ] YOLO object detection pipeline on Jetson GPU
- [ ] Person-following behavior node
- [ ] Full Nav2 autonomous navigation on real hardware
- [ ] SLAM map generation and localization validation
- [ ] Full system integration testing — all subsystems running simultaneously
- [ ] Documentation — architecture writeup, wiring diagrams, software README
- [ ] **MILESTONE #3 target: Dec 16** — Full autonomous run demonstration

## Design Decisions

**Motor Selection — Pololu 37D Bare Motor (24V, no internal gearbox)**
Chosen over motors with factory gearboxes specifically because the custom gearbox IS the project. Using a bare motor means the only reduction stage is our custom 2-ratio transmission, which maximizes back-drive efficiency for regenerative braking (no factory gearbox eating energy in reverse) and gives us full control over gear ratios. The 64 CPR encoder provides tight velocity feedback for PID.

**Motor Driver — Cytron MDD10A × 2**
Chosen over BTS7960 because it is purpose-built for the 10-12A peak current range of our motors, includes proper overcurrent/overheat protection, has cleaner PWM response, and covers two motors per board — reducing wiring complexity from four boards to two. Supports regenerative braking current routing.

**Microcontroller — Teensy 4.1**
600 MHz ARM Cortex-M7 provides sufficient headroom to run four encoder interrupts, four PID loops, CAN comms to Jetson, servo PWM for gear selector, and hydraulic brake solenoid control simultaneously without timing conflicts. Native CAN bus and solid micro-ROS support for ROS 2 integration via serial.

**Perception — RealSense D435 + RPLIDAR A1 (no OAK-D)**
LiDAR handles 2D SLAM with superior reliability on blank walls and in low light. RealSense adds 3D depth for AEB and close-range obstacle detection. The OAK-D was evaluated and dropped — once LiDAR is in the stack, OAK-D has no unique role. The combo of RealSense + LiDAR outperforms OAK-D + LiDAR in both indoor reliability and outdoor sunlight conditions.

**AEB Design — Depth Threshold, Not Image Recognition**
AEB latency requirement is sub-25ms. Neural network inference adds 50-120ms before a brake signal is even sent. The AEB node reads raw RealSense depth frames, checks the minimum depth value in a forward-facing region of interest, and fires directly to the Teensy over a dedicated high-priority serial path — bypassing the ROS nav stack entirely. Total pipeline latency: ~15-20ms.

**Gearbox — Per-Wheel (not shared axle)**
Each mecanum wheel must spin at an independently controlled speed. Any mechanical coupling between two wheels (e.g. shared differential) destroys omnidirectional capability. All four gearboxes shift simultaneously via a single servo command from Teensy, maintaining synchronized gear state across all wheels.

**No AK60-6 Actuators**
CubeMars AK60-6 was evaluated — excellent motors with integrated FOC and CAN — but at ~$220/unit ($880 for 4 wheels) they consume over half the total budget before any other component is purchased. The Pololu 37D + custom gearbox achieves the educational objectives of the project at a fraction of the cost.

## Design Misc

- **Gearbox Ratios**: High gear 1:1 (flat terrain, max speed), Low gear 2:1 (inclines, max torque). With Pololu 37D at 24V, low gear provides approximately 2× the climbing force.
- **Shock Absorber Tuning**: Spring rate selected based on estimated robot mass ~10-12 kg. Rebound damping oil viscosity to be tuned empirically during summer assembly phase.
- **Hydraulic Brake Hold Force**: Sized to hold robot stationary on 20° incline at full load. Master cylinder bore sized for solenoid actuation force available from Teensy-controlled valve.
- **Regenerative Braking Efficiency**: With bare motor (no internal gearbox) and 1:1 or 2:1 custom transmission, estimated 45-55% energy recovery vs ~12% with a factory 50:1 gearbox.
- **Stereo LiDAR**: If additional 3D mapping capability is needed beyond RealSense, stereo depth from RealSense is fed into RTAB-Map as a second mapping layer. No OAK-D needed.
- **WiFi/BT Remote Control**: Implemented as a ROS 2 teleop node. Autonomous mode and teleop mode are mutually exclusive with a hardware-level mode switch. Emergency stop works in both modes.

## Steps for Documenting Your Design Process

1. **CAD Files** — All SolidWorks/Fusion 360 files version-controlled in project GitHub repo under `/cad`. Export STLs and STEP files for each manufactured part alongside manufacturing drawings (PDF).
2. **FEA Reports** — Document load cases, boundary conditions, mesh parameters, and safety factors for each analyzed component. Export simulation screenshots and summary tables to `/docs/fea`.
3. **Wiring Diagrams** — Full schematic in KiCad or Fritzing showing every electrical connection: Teensy pinout, motor driver wiring, sensor connections, power distribution. Stored in `/docs/electrical`.
4. **Firmware** — Teensy firmware in `/firmware` with inline comments explaining each PID parameter, CAN message format, and interrupt configuration. Include a README with flash instructions.
5. **ROS 2 Packages** — Each subsystem (kinematics, navigation, perception, AEB) is its own ROS 2 package in `/ros2_ws/src`. Include launch files and parameter YAML files.
6. **Test Logs** — After each milestone, document test results: motor RPM vs command, PID step response plots, LiDAR scan accuracy, navigation success rate. Stored in `/docs/test_logs`.
7. **Weekly Log** — Update the Log section of this document every week with what was completed, what blocked progress, and what is planned next.

## BOM + Component Cost

| Component | Category | Qty | Unit Cost | Total |
|---|---|---|---|---|
| NVIDIA Jetson Orin Nano Super (8GB) | Compute | 1 | $249 | $249 |
| Teensy 4.1 Microcontroller | Embedded Control | 1 | $30 | $30 |
| Pololu 37D Bare DC Motor (24V, 64 CPR Encoder) | Drivetrain | 4 | $37.50 | $150 |
| Custom CNC Gearbox — Aluminum, 2-ratio (materials est.) | Transmission | 4 | ~$40 | ~$160 |
| Servo Motor (Gear Selector Actuator) | Transmission | 1 | $30 | $30 |
| Cytron MDD10A Dual Motor Driver | Power Electronics | 2 | $30 | $60 |
| Intel RealSense D435 RGB-D Camera | Perception | 1 | $399 | $399 |
| RPLIDAR A1 (2D LiDAR) | Perception | 1 | $100 | $100 |
| IMU — BNO055 | Sensing | 1 | $25 | $25 |
| WiFi / Bluetooth Module | Communications | 1 | $25 | $25 |
| LiPo Battery Pack (22.2V, 10Ah) | Power | 1 | $150 | $150 |
| Power Management / BMS Board | Power | 1 | $80 | $80 |
| Robot Chassis (Aluminum Frame, Final Stage) | Structure | 1 | $180 | $180 |
| Wiring, Connectors, Fasteners, Misc. Hardware | Misc. | — | — | $120 |
| **TOTAL** | | | | **~$1,758** |

> Custom gearbox cost is a materials estimate only. Machining is done in-house using university shop access. ROS 2, NVIDIA Isaac Sim, and all software tools are free / open-source.

## Timeline

### Spring 2026 — Now → May 13
**Goal**: All CAD complete, all parts ordered and received, FEA validated

| Week | Focus |
|---|---|
| Now – Week 2 | Finalize BOM, place all component orders |
| Week 2 – 4 | CAD — Chassis, gearbox, shock absorbers, hydraulic brakes |
| Week 4 – 5 | FEA analysis on chassis and gearbox housing |
| Week 5 – 6 | Manufacturing drawings, send files to shop / begin 3D printing |
| **May 13** | **🏁 MILESTONE #1 — Chassis (physical), Wheels (mounted), Gearbox (CAD), Brakes (CAD), Shockers (CAD)** |

---

### Summer 2026 — May 26 → July 6
**Goal**: Fully assembled and wired robot with all subsystems individually tested

| Week | Focus |
|---|---|
| Week 1 | 3D print and CNC all custom parts |
| Week 2 | Full mechanical assembly — chassis, gearboxes, shock absorbers, wheels |
| Week 3 | All electronics wiring — Teensy, motor drivers, LiDAR, RealSense, IMU, WiFi/BT, AI PC |
| Week 4 | Teensy firmware — encoders, PID, CAN/serial, gear selector, brake solenoid |
| Week 5 | Testing — mecanum kinematics, regen braking, gearbox shifting, hydraulic brakes |
| Week 6 | Remote control integration + Isaac Sim full-scale simulation |
| **June 13** | **🏁 MILESTONE #2 — Full assembly complete, all wiring done, gearbox + brakes + remote tested** |

> *Break period: July 6 – August 24*

---

### Fall 2026 — Aug 24 → Dec 16
**Goal**: Full autonomous robot with AI perception, SLAM navigation, and AEB — demonstrated live

| Week | Focus |
|---|---|
| Week 1 – 2 | Camera integration — RealSense depth into Nav2 costmap + SLAM |
| Week 3 – 4 | AEB system — depth threshold node, dedicated serial path to Teensy |
| Week 5 – 6 | AI pipeline — YOLO object detection + person following on Jetson |
| Week 7 – 8 | Full ROS 2 stack on hardware — Nav2, localization, sensor fusion |
| Week 9 – 10 | System integration — all subsystems running simultaneously |
| Week 11 – 12 | Testing, debugging, performance tuning |
| Week 13 – 14 | Documentation — architecture writeup, wiring diagrams, software README |
| **Dec 16** | **🏁 MILESTONE #3 — Full autonomous demo: SLAM map, navigate to goal, detect person, AEB trigger** |

## Useful Links

- [Pololu 37D Metal Gearmotor (Bare, 24V, Encoder)](https://www.pololu.com/category/116/37d-mm-metal-gearmotors)
- [Cytron MDD10A Dual Motor Driver](https://www.cytron.io/p-10amp-5v-30v-dc-motor-driver-2-channels)
- [Teensy 4.1 — PJRC](https://www.pjrc.com/store/teensy41.html)
- [NVIDIA Jetson Orin Nano Super Developer Kit](https://developer.nvidia.com/embedded/jetson-orin-nano-developer-kit)
- [Intel RealSense D435](https://www.intelrealsense.com/depth-camera-d435/)
- [RPLIDAR A1](https://www.slamtec.com/en/Lidar/A1)
- [ROS 2 Humble Documentation](https://docs.ros.org/en/humble/)
- [Nav2 Documentation](https://docs.nav2.org/)
- [NVIDIA Isaac Sim](https://developer.nvidia.com/isaac-sim)
- [micro-ROS for Teensy](https://micro.ros.org/)
- [SimpleFOC Library](https://simplefoc.com/)
- [RTAB-Map ROS 2](https://github.com/introlab/rtabmap_ros)

## Log

### Week of April 21, 2026
- Project proposal drafted and submitted
- Component decisions finalized: Pololu 37D bare motor, Cytron MDD10A, Teensy 4.1, RealSense D435 + RPLIDAR A1
- Decided against OAK-D Lite (redundant with RealSense + LiDAR combo)
- Decided against AK60-6 actuators (over budget at $880 for 4 wheels)
- AEB architecture decided: depth threshold on raw RealSense frames, dedicated high-priority serial path to Teensy — no image recognition in the braking loop
- Three-semester timeline established with three milestones (May 13, June 13, Dec 16)
- PowerPoint proposal finalized and submitted
- **Next steps**: Begin chassis CAD, finalize BOM pricing, place first component orders