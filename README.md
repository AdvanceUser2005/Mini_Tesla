# Mini Tesla — Autonomous Regenerative EV Robot Platform

> A custom four-wheel robotic EV platform for regenerative braking, autonomous navigation, fast obstacle response, and full-stack robotics development.

## Project Lead

**Daksh Gupta**  
Computer Engineering — Controls, Robotics & Autonomy  
Virginia Tech  
mailtodaksh@vt.edu

**Status:** In Progress — Mechanical CAD / Milestone 1  
**Last Updated:** October 5, 2026

---

## Overview

**Mini Tesla** is a custom electric robotic platform being developed to combine mechanical design, embedded control, perception, autonomy, and regenerative braking in one system.

The project is currently focused on building a mechanically sound and modular four-wheel chassis around the **real purchased components** before full electronics and autonomy integration.

The current architecture uses:

- **Pololu 37D 20:1 gearmotors with encoders**
- **Cytron bidirectional motor drivers**
- **Teensy 4.1** for low-level real-time control
- **ASUS Zephyrus G14** as the primary development/onboard compute platform
- **OAK-D Lite** stereo/depth camera
- **8× Time-of-Flight sensors** for close-range perimeter sensing
- **IMU + wheel odometry** for state estimation
- **TI IWR6843AOPEVM** mmWave radar as the initial front radar
- **ROS 2 Jazzy**, Gazebo Harmonic, and NVIDIA Isaac Sim for autonomy and simulation

One of the central goals is to experimentally study **regenerative braking on a small robotic EV**. During controlled deceleration, the drivetrain will be instrumented to measure generated voltage, current, recovered energy, and stopping behavior.

> Features listed as goals are not presented as completed functionality. The robot is currently in the mechanical design and prototype stage.

---

# Main Goals

The final platform is intended to support:

- Autonomous indoor and outdoor navigation
- Fast obstacle detection and emergency deceleration
- Regenerative braking and energy-recovery measurement
- Stereo depth perception and visual SLAM
- Wheel-encoder + IMU sensor fusion
- Near-field obstacle detection around the full chassis
- Front mmWave radar sensing
- ROS 2 navigation and behavior logic
- Real-time motor control through Teensy 4.1
- Teleoperation and emergency override
- Gazebo / Isaac Sim digital twin development
- Modular and serviceable mechanical construction

A target demonstration is an indoor test where an object such as a football enters the robot's path, the robot detects it, decelerates rapidly, and records the electrical energy recovered during the braking event.

---

# System Architecture

## High-Level Compute — ASUS Zephyrus G14

The current chassis is being designed with enough top-deck space to carry the laptop with the lid closed.

The laptop will handle tasks such as:

- ROS 2
- OAK-D processing
- VSLAM / localization
- Sensor fusion
- Navigation
- Object detection
- Radar processing
- Data logging
- Simulation and development tools

A dedicated Jetson may be considered later, but it is not required for the current mechanical prototype.

## Low-Level Control — Teensy 4.1

The Teensy handles timing-critical functions including:

- Motor commands
- Encoder acquisition
- Wheel-speed estimation
- PID velocity control
- Emergency braking commands
- Drivetrain telemetry
- Communication with the high-level computer

Timing-critical motor control should remain independent of high-level perception and navigation workloads.

---

# Drivetrain & Regenerative Braking

## Motors

Current drivetrain hardware is based on:

- **4× Pololu 37D gearmotors**
- **20:1 reduction**
- Integrated quadrature encoders

The exact SKU must match the purchased component and supplied CAD model.

## Current Drive / Regen Concept

The current concept separates the front and rear drivetrain roles:

- **Rear pair:** primary propulsion
- **Front pair:** regenerative-braking / energy-recovery experimentation

The final electrical topology will be validated experimentally before claiming that recovered energy can safely be returned to the battery.

### Regen Tests

The system should measure:

- Motor back-EMF during deceleration
- Regenerated voltage
- Regenerated current
- Recovered energy per braking event
- Braking distance and response time
- Battery / DC-bus voltage rise
- Thermal behavior
- Repeatability

A bidirectional motor driver alone does **not** guarantee safe battery regeneration. The driver, battery, BMS, wiring, and protection circuitry must all be verified for reverse-current operation.

---

# Perception & Localization

## OAK-D Lite

The OAK-D Lite is the current front stereo/depth camera choice.

Planned uses:

- Stereo depth
- Visual odometry / VSLAM
- Front obstacle detection
- Object/person detection
- Navigation perception

## Time-of-Flight Sensors

Current layout target:

| Side | Quantity |
|---|---:|
| Front | 2 |
| Rear | 2 |
| Left | 2 |
| Right | 2 |
| **Total** | **8** |

### ToF Placement Rule

The sensing cone must remain clear of the wheels, tires, motor mounts, chassis walls, and neighboring sensors.

Do **not** place a ToF sensor directly beside a wheel if the wheel blocks one side of its field of view.

Sensor brackets should be removable and adjustable so height and angle can be changed during testing.

## IMU + Wheel Odometry

Encoder odometry will be fused with IMU measurements for motion estimation.

The final IMU model is still subject to BOM confirmation.

## mmWave Radar

Preferred radar: **TI IWR6843AOPEVM**

Initial configuration:

- 1× front-facing radar
- Chassis architecture should allow additional radar modules later if testing justifies them

Possible uses include longer-range obstacle awareness, motion detection, and relative radial velocity.

---

# Mechanical CAD Requirements

These requirements are mandatory for the current chassis design.

## 1. Purchased Components Are Fixed Geometry

All supplied STEP/CAD models, drawings, dimensions, and purchased components are treated as fixed geometry.

Custom parts must be designed around them.

Do not:

- Resize purchased components
- Change connector locations
- Approximate mounting patterns when dimensions are available
- Invent dimensions
- Modify a purchased component to make the assembly easier

## 2. Modular Chassis

The chassis must be split into printable structural sections because the complete base may exceed the printer build volume.

Requirements:

- Replaceable chassis sections
- Reinforced joints
- Repeatable alignment between sections
- Overlapping/interlocking joints where useful
- No weak butt joints carrying major drivetrain loads

## 3. Standard Fastener — M2.5

Use M2.5 hardware throughout where practical:

- M2.5 machine screws
- Heat-set inserts for repeatedly serviced joints
- Through-holes + nuts where appropriate

Fasteners must have sufficient surrounding material and must remain accessible after assembly.

## 4. Separate Motor Mounts

Motor mounts should be separate removable parts rather than being permanently printed into the chassis.

Benefits:

- Easier motor replacement
- Easier drivetrain revisions
- Better printing orientation
- Local reinforcement
- Less risk of reprinting the full chassis

The mount must use the real motor geometry and mounting pattern.

## 5. Wheel Adapters / Hubs

Wheel interfaces must:

- Match the real motor/gearbox output shaft
- Resist torque without slipping
- Maintain wheel concentricity
- Minimize unnecessary cantilever loading
- Allow the wheel to be removed independently

## 6. Structural Reinforcement

High-load regions should use ribs, gussets, boxed sections, large-radius fillets, or local thickness increases around:

- Motor mounts
- Wheel interfaces
- Chassis section joints
- Battery mounts
- Laptop deck supports

Avoid unnecessary solid mass when geometry can provide stiffness more efficiently.

## 7. Electronics Space

Reserve accessible mounting volume for:

- Teensy 4.1
- Motor drivers
- Power distribution
- Battery / energy storage
- Voltage regulators
- Emergency-stop hardware
- Sensor interfaces
- Wiring junctions
- Future expansion electronics

Individual electronics modules should be removable without dismantling the full robot.

## 8. Laptop Deck

The top structure must support the **ASUS Zephyrus G14 with the lid closed**.

Requirements:

- Stable flat support
- Retention against acceleration/braking
- Ventilation clearance
- Access to USB/Ethernet/power ports
- Cable strain relief
- Quick removal for normal laptop use

## 9. Removable Sensor Mounts

Use separate brackets for:

- OAK-D Lite
- ToF sensors
- Radar
- IMU where appropriate

Sensor mounts should allow adjustment where useful and must not obstruct the sensor field of view.

## 10. Cable Routing

The chassis should include intentional wiring paths:

- Cable channels / pass-throughs
- Strain-relief points
- Clearance from wheels and other moving parts
- Separation of high-current motor wiring from sensitive sensor wiring where practical
- No cables crossing service fasteners
- No sharp printed edges contacting wires

## 11. Accessibility & Serviceability

The design should allow independent removal of:

- Motor
- Wheel
- Motor mount
- Sensor module
- Laptop
- Battery
- Electronics tray

Do not create assemblies where a required screw or nut becomes inaccessible after another component is installed.

## 12. Printability

### Prototype

- **Material:** PLA
- Purpose: fit checks, assembly validation, cable routing, and geometry iteration

### Final Printed Structure

- **Target material:** PA12 / PA612 carbon-fiber-reinforced nylon
- **Nominal chassis thickness target:** ~5 mm, adjusted locally according to load
- Hardened nozzle required for abrasive CF-filled filament

Part orientation should consider both printability and load direction.

## 13. Weight Reduction

Perforations and pockets are allowed only where they do not compromise:

- Motor-mount stiffness
- Chassis joints
- Battery support
- Electronics mounting
- Impact resistance

Structural ribs are preferred over random material removal.

---

# Safety Requirements

The finished robot should include:

- Physical emergency stop
- Software emergency stop
- Motor-command watchdog / timeout
- Defined startup state
- Defined communication-loss behavior
- Battery voltage monitoring
- Current monitoring where practical
- Safe regenerative-voltage limits
- Sensor-loss fallback behavior
- Indoor speed limits during early testing

Emergency obstacle response should use the fastest reliable sensor information available rather than depending only on neural-network object classification.

---

# Software Stack

## Primary Environment

- **ROS 2 Jazzy**
- Linux
- **Gazebo Harmonic**
- NVIDIA Isaac Sim when useful and sufficient GPU resources are available

Planned ROS 2 modules include:

- Hardware interface
- Encoder acquisition
- Wheel odometry
- IMU fusion
- OAK-D perception
- ToF interface
- Radar interface
- VSLAM / localization
- Navigation
- Emergency braking
- Regenerative-braking telemetry
- Diagnostics
- Data logging

Simulation is used to accelerate development, but physical testing remains the source of truth for braking, regeneration, thermal behavior, and structural performance.

---

# Current BOM

| Component | Qty | Status / Notes |
|---|---:|---|
| Pololu 37D 20:1 gearmotor with encoder | 4 | Selected; exact SKU must match purchased CAD |
| Wheels | 4 | Geometry must match supplied CAD |
| Cytron bidirectional dual-channel motor driver | 2 | Selected architecture; reverse-current behavior must be verified |
| Teensy 4.1 | 1 | Selected |
| ASUS Zephyrus G14 | 1 | Existing high-level compute |
| OAK-D Lite | 1 | Selected |
| ToF distance sensors | 8 | Planned — 2 per side |
| TI IWR6843AOPEVM | 1 | Preferred initial front radar |
| IMU | 1 | Final model TBD |
| Battery / energy-storage system | 1 | Final specification pending regen validation |
| Power distribution / protection | 1 set | Required |
| Emergency-stop hardware | 1 set | Required |
| M2.5 screws | — | Standard project fastener |
| M2.5 heat-set inserts | — | Serviceable printed joints |
| PLA | — | Prototype parts |
| PA12 / PA612 CF nylon | — | Final structural parts |
| Hardened nozzle | 1 | Required for CF-filled nylon |
| Wiring / connectors / strain relief | — | Required |

---

# Budget

**Target total project budget: approximately $1,700**

Approximately **$724** had been spent through the AMP Lab as of the latest budget update.

Current cost-control choices include:

- Using the existing Zephyrus G14 instead of immediately buying dedicated compute
- OAK-D Lite instead of the older RealSense + LiDAR architecture
- One initial front radar instead of four radar units
- ToF sensors for inexpensive near-field perimeter coverage
- In-house printed chassis and mounts
- Replaceable mechanical modules so revisions do not require rebuilding the full robot

---

# Milestones

## Milestone 1 — Mechanical Platform

**Current focus**

- [ ] Complete chassis CAD
- [ ] Finalize modular chassis sections
- [ ] Verify every purchased component against supplied CAD
- [ ] Complete removable motor mounts
- [ ] Complete wheel interfaces/adapters
- [ ] Finalize M2.5 fastening strategy
- [ ] Finalize laptop top deck
- [ ] Finalize sensor positions
- [ ] Reserve electronics space
- [ ] Add cable-routing features
- [ ] Print and assemble PLA prototype
- [ ] Document the physical prototype

## Milestone 2 — Drivetrain + Electronics

- [ ] Integrate motors and encoders
- [ ] Wire motor drivers
- [ ] Implement Teensy firmware
- [ ] Integrate battery and power distribution
- [ ] Closed-loop wheel control
- [ ] Emergency-stop system
- [ ] Encoder + IMU odometry
- [ ] Regenerative-braking instrumentation
- [ ] Initial regen testing
- [ ] OAK-D / ToF / radar integration

## Milestone 3 — Autonomy + Demonstration

- [ ] ROS 2 hardware interfaces
- [ ] VSLAM / localization
- [ ] Sensor fusion
- [ ] Obstacle detection
- [ ] Emergency deceleration
- [ ] Autonomous navigation
- [ ] Regenerative-energy logging
- [ ] Gazebo / Isaac Sim digital twin
- [ ] Final integrated demonstration

---

# AI-Assisted CAD Rules

When AI is used to help create the mechanical design:

1. Read the requirements file first.
2. Inspect every supplied STEP/CAD model, drawing, dimension sheet, image, and reference before generating geometry.
3. Treat purchased-component geometry as fixed.
4. Never invent a mounting dimension that exists in the supplied files.
5. Use reference images for design intent, not blind copying.
6. Improve geometry where required for strength, printability, accessibility, or serviceability.
7. Use M2.5 screws and heat-set inserts as the default fastening strategy.
8. Keep motor mounts, sensor mounts, and electronics modules removable.
9. Split the chassis into printable sections.
10. Reinforce motor and wheel load paths.
11. Keep ToF, camera, and radar fields of view clear of wheels and bodywork.
12. Include cable routing and strain relief.
13. Preserve access to every service fastener.
14. Check tool access for every screw.
15. Check connector access for every electrical component.
16. Verify wheel clearance through the full rotating envelope.
17. Verify a realistic assembly sequence.
18. Avoid decorative geometry that reduces serviceability.
19. Use parametric dimensions / user parameters for repeated tolerances.
20. Complete functional assembly geometry before cosmetic refinement.

---

# Validation Plan

## Mechanical

- Chassis deflection under full payload
- Motor-mount deflection
- Wheel alignment
- Fastener loosening
- Chassis-joint durability
- Thermal behavior of printed mounts

## Drivetrain / Regen

- Wheel RPM vs command
- Motor current
- Closed-loop response
- Braking distance
- Generated voltage/current
- Recovered energy per stop
- Battery/DC-bus voltage rise
- Repeatability

## Perception

- ToF blind spots and wheel occlusion
- Stereo depth accuracy
- VSLAM stability
- Radar range / velocity quality
- Sensor latency

## Autonomy

- Localization drift
- Obstacle-detection latency
- Emergency-stop latency
- Navigation success rate
- Failure behavior after sensor or communication loss

---

# Repository Structure

```text
Mini-Tesla/
├── README.md
├── cad/
│   ├── purchased_components/
│   ├── chassis/
│   ├── motor_mounts/
│   ├── wheel_adapters/
│   ├── sensor_mounts/
│   └── exports/
├── firmware/
│   └── teensy/
├── ros2_ws/
│   └── src/
├── simulation/
│   ├── gazebo/
│   └── isaac_sim/
├── electronics/
│   ├── wiring/
│   └── power/
├── docs/
│   ├── mechanical/
│   ├── regen/
│   ├── test_logs/
│   └── photos/
└── bom/
```

For each major hardware revision, document:

- CAD screenshot
- What changed
- Why it changed
- Physical prototype photo when available
- Test result when experimentally validated

---

# Current Development Log — October 2026

- Mechanical architecture moved away from the older mecanum / custom transmission concept.
- Current robot uses a conventional four-wheel chassis architecture.
- Pololu 37D 20:1 encoder gearmotors are being used for the current drivetrain design.
- Motor mounts are separate replaceable modules.
- The chassis is being split into printable structural sections.
- PLA is being used for fit and prototype validation.
- PA12 / PA612 CF nylon is planned for stronger final printed parts.
- M2.5 screws and heat-set inserts are the standard fastening system.
- CAD is being designed around the actual supplied component geometry.
- The top deck must support the ASUS Zephyrus G14.
- OAK-D Lite is the current stereo/depth camera choice.
- Current ToF concept uses two sensors per side.
- ToF placement is being designed so wheels do not block the sensor field of view.
- TI IWR6843AOPEVM is the preferred initial front radar.
- Teensy 4.1 remains the low-level controller.
- Regenerative braking remains a core project experiment.
- Current priority is completing Milestone 1 mechanical CAD and the physical chassis prototype.

---

# Engineering Principles

- **Build around real hardware, not guessed dimensions.**
- **Do not claim performance before measuring it.**
- **Make important modules replaceable.**
- **Design for assembly and repair, not just appearance.**
- **Keep safety-critical control independent of slow perception pipelines.**
- **Use simulation to accelerate development, not replace physical validation.**
- **Treat regenerative braking as a complete power-electronics problem, not only a motor-control feature.**

---

# Useful Links

- [ROS 2 Jazzy Documentation](https://docs.ros.org/en/jazzy/)
- [Nav2 Documentation](https://docs.nav2.org/)
- [Gazebo Harmonic Documentation](https://gazebosim.org/docs/harmonic/)
- [NVIDIA Isaac Sim](https://developer.nvidia.com/isaac-sim)
- [Teensy 4.1 — PJRC](https://www.pjrc.com/store/teensy41.html)
- [Luxonis OAK Documentation](https://docs.luxonis.com/)
- [TI IWR6843AOPEVM](https://www.ti.com/tool/IWR6843AOPEVM)
- [Pololu 37D Gearmotors](https://www.pololu.com/category/116/37d-mm-metal-gearmotors)

---

## Current Configuration Summary

| System | Current Choice |
|---|---|
| Platform | Four-wheel autonomous robotic EV |
| Motors | Pololu 37D 20:1 gearmotors + encoders |
| Low-Level Control | Teensy 4.1 |
| High-Level Compute | ASUS Zephyrus G14 |
| Stereo / Depth | OAK-D Lite |
| Near-Field Sensing | 8× ToF |
| Radar | TI IWR6843AOPEVM — front initially |
| State Estimation | Wheel odometry + IMU |
| Software | ROS 2 Jazzy |
| Simulation | Gazebo Harmonic + Isaac Sim |
| Prototype Material | PLA |
| Final Material Target | PA12 / PA612 CF nylon |
| Primary Fastener | M2.5 |
| Current Phase | Mechanical CAD / Milestone 1 |
