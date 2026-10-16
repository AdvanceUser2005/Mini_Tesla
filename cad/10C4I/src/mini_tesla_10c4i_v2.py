"""
Mini Tesla 10C4I - chassis v2 (built around the real parts)

Parts (print qty):
  center_section  x1  battery bay + X-grid strips          (floor on bed)
  end_section     x2  front AND rear are the same part      (floor on bed)
  motor_cap       x4  top half of each can clamp            (flat top on bed)
  wheel_adapter   x4  6 mm D-shaft -> REV DUO 75 mm wheel, 8x M2.5 inserts (hub end on bed)

Real parts used:
  Pololu #4691 19:1 37D gearmotor w/ encoder (STEP from Pololu)
  REV DUO 75 mm mecanum (REV-41-1656/1657): web holes 4x 4.0 on 24 BC, 4x 3.0 on 16 BC, 8.1 bore
  Turnigy 6S 5200 mAh: 156 x 54 x 45

Fasteners: M3 countersunk only at the motor faces (Pololu thread depth max 3.0 mm),
           M2.5 + heat-set inserts everywhere else.
Coordinates: X forward, Y left, Z up. Z = 0 is the chassis underside. mm.
"""
import math, os
import numpy as np
import cadquery as cq
from shapely.geometry import Polygon

# =============================================================================
# 1. TOLERANCES  <-- update these from the coupon, then re-run
# =============================================================================
INS_M25   = 3.1    # M2.5 heat-set pilot hole (Pofsnnx M2.5 x 4 x 3.5 OD). Coupon will confirm.
INS_DEPTH = 6.0    # blind depth for inserts
CLR_M25_V = 2.9    # M2.5 clearance, hole axis vertical in print
CLR_M25_H = 3.0    # M2.5 clearance, hole axis horizontal in print
CLR_M3_H  = 3.4    # M3 clearance through the motor walls (horizontal in print)
CSK_M3_D  = 6.4    # 90 deg countersink for M3 flat heads (flush, wheel is 3 mm away)
BUSH_D    = 12.3   # gearbox bushing (12.0 nominal)
SLIDE     = 0.25   # per-side clearance on pegs / lap joint
GB_BORE   = 36.8 + 0.4   # clamp bore over the gearbox housing
CLAMP_GAP = 0.8    # cap sits this high so the screws actually clamp the can
DBORE_D, DFLAT = 6.15, 2.45        # 6 mm D-shaft (flat at 2.4 from centre)
PILOT_D = 7.8                      # centres the wheel in its 8.1 bore

# =============================================================================
# 2. LAYOUT
# =============================================================================
BED = (250.0, 210.0, 220.0)          # Prusa MK4S
L_S   = 118.7        # every section is the same length (356 total ~ 16" MacBook Pro)
W     = 170.0        # body width (battery rides crosswise inside)
H     = 49.0         # box height; everything tucks under this plane
GROUND = 21.0        # floor underside to ground
FLOOR, SIDE_T, BULK_T, END_T, RIB_T = 3.0, 5.5, 6.0, 5.0, 3.0
HX = L_S / 2         # centre-section half length
Y_IN = W / 2 - SIDE_T

# Wheel (REV DUO 75 mm)
WHEEL_R, WHEEL_RMAX, WHEEL_W, WHEEL_WEB, WEB_T = 37.5, 39.0, 40.8, 19.2, 2.4
WHEEL_GAP = 3.0
AXLE_Z = WHEEL_R - GROUND
AXLE_XL = L_S - 45.0            # axle x in end-section local coords (x=0 at joint face)

# Motor (Pololu 37D 19:1 + encoder), clocked so the encoder cable tab clears the floor
MOTOR_L, GB_L, CAN_R, GB_R = 67.6, 21.5, 17.4, 18.4
GB_DX, GB_DZ = 2.39, 6.58      # gearbox centre relative to shaft (left motor; right = -dx)
FACE_BC_R = 15.5
MOTOR_CZ = AXLE_Z + GB_DZ

# Motor clamp: grips the GEARBOX right behind the wall. The can/encoder (34.8/34.0) pass through the
# 37.2 bore, so the motor can slide in axially and the bushing drops into the wall hole.
SAD_U = (3.0, 19.0)            # distance from gearbox face (gearbox is 21.5 long)
SAD_HW = 28.0
CAP_TOP = MOTOR_CZ + GB_BORE / 2 + 5.0
CAP_BOLT_DX = 23.3

# Battery bay
BATT = (156.0, 54.0, 45.0)
BAY_IN = BATT[1] + 2.0         # along X
BAY_T = 3.5

# Joint
LIP = 6.0                                   # centre lip over end bulkhead
LIP_Z0 = H - 12.0                           # 45 deg underside starts here
PEG_Y, PEG_Z, PEG_R, PEG_L = 45.0, 20.0, 4.0, 5.0
JOINT_SCREWS = [(y, z) for z in (8.0, 32.0) for y in (-70.0, -25.0, 25.0, 70.0)]

# =============================================================================
# helpers
# =============================================================================
def box(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(x1 - x0, y1 - y0, z1 - z0, centered=False).translate((x0, y0, z0))

def cyl_x(x0, x1, y, z, d):
    return cq.Workplane("YZ").workplane(offset=x0).center(y, z).circle(d / 2).extrude(x1 - x0)

def cyl_y(y0, y1, x, z, d):
    return cq.Workplane("XZ").workplane(offset=-y0).center(x, z).circle(d / 2).extrude(-(y1 - y0))

def cyl_z(z0, z1, x, y, d):
    return cq.Workplane("XY").workplane(offset=z0).center(x, y).circle(d / 2).extrude(z1 - z0)

def cone(p0, direction, d0, d1, h):
    return cq.Workplane("XY").add(cq.Solid.makeCone(d0 / 2, d1 / 2, h, cq.Vector(*p0), cq.Vector(*direction)))

def prism_xz(pts, y0, y1):
    return cq.Workplane("XZ").workplane(offset=-y0).polyline(pts).close().extrude(-(y1 - y0))

def prism_yz(pts, x0, x1):
    return cq.Workplane("YZ").workplane(offset=x0).polyline(pts).close().extrude(x1 - x0)

def prism_xy(pts, z0, z1):
    return cq.Workplane("XY").workplane(offset=z0).polyline(pts).close().extrude(z1 - z0)

def diamond(cy, cz, r):
    return [(cy, cz - r), (cy + r, cz), (cy, cz + r), (cy - r, cz)]

def rib_between(x0, y0, x1, y1, z0, z1, clip):
    L = math.hypot(x1 - x0, y1 - y0) + RIB_T
    a = math.degrees(math.atan2(y1 - y0, x1 - x0))
    r = (cq.Workplane("XY").box(L, RIB_T, z1 - z0, centered=(True, True, False))
         .rotate((0, 0, 0), (0, 0, 1), a).translate(((x0 + x1) / 2, (y0 + y1) / 2, z0)))
    return r.intersect(clip)

def x_cell(x0, x1, y0, y1, z0, z1):
    """X-braced cell: two diagonal ribs clipped to the cell."""
    clip = box(x0, x1, y0, y1, z0, z1)
    return (rib_between(x0, y0, x1, y1, z0, z1, clip)
            .union(rib_between(x0, y1, x1, y0, z0, z1, clip)))

def x_windows(x0, x1, y0, y1, web=RIB_T / 2 + 2.0):
    """The four triangular floor windows of an X cell, inset so ribs keep a solid footing."""
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    cut = None
    for i in range(4):
        tri = Polygon([corners[i], corners[(i + 1) % 4], (cx, cy)]).buffer(-web, join_style=2)
        if tri.is_empty or tri.area < 20:
            continue
        pts = list(tri.exterior.coords)[:-1]
        w = prism_xy(pts, -1, FLOOR + 1)
        cut = w if cut is None else cut.union(w)
    return cut

def top_boss(x, y, z_top=H, d=8.0):
    return cyl_z(0.0, z_top, x, y, d)          # full-height column: no overhang, ties floor to top

def top_ins(x, y, z_top=H):
    return cyl_z(z_top - INS_DEPTH, z_top + 1, x, y, INS_M25)

# =============================================================================
# CENTER SECTION  (world coords)
# =============================================================================
def center_section():
    bay_o = BAY_IN / 2 + BAY_T
    body = box(-HX, HX, -W / 2, W / 2, 0, H).cut(
        box(-HX + BULK_T, HX - BULK_T, -Y_IN, Y_IN, FLOOR, H + 1))
    # battery bay walls
    for s in (-1, 1):
        body = body.union(box(*sorted((s * BAY_IN / 2, s * bay_o)), -Y_IN, Y_IN, 0, H))
    # X-grid strips between bay and bulkheads
    ycells = [-Y_IN, -40.0, 0.0, 40.0, Y_IN]
    nodes = []
    for s in (-1, 1):
        xa, xb = sorted((s * bay_o, s * (HX - BULK_T)))
        for y in ycells[1:-1]:
            body = body.union(box(xa, xb, y - RIB_T / 2, y + RIB_T / 2, 0, H))
        for y0, y1 in zip(ycells[:-1], ycells[1:]):
            body = body.union(x_cell(xa, xb, y0, y1, 0, H))
            body = body.cut(x_windows(xa, xb, y0, y1))
            nodes.append(((xa + xb) / 2, (y0 + y1) / 2))
    # lap lips (45 deg underside -> prints without support)
    for s in (-1, 1):
        pts = [(s * HX, LIP_Z0), (s * (HX + LIP), LIP_Z0 + LIP), (s * (HX + LIP), H), (s * HX, H)]
        body = body.union(prism_xz(pts, -W / 2, W / 2))
        # diamond alignment pegs
        for py in (-PEG_Y, PEG_Y):
            xa, xb = sorted((s * (HX - 1), s * (HX + PEG_L)))
            peg = prism_yz(diamond(py, PEG_Z, PEG_R), xa, xb)
            body = body.union(peg)
    # top mounting bosses (M2.5 inserts)
    tops = []
    for x in (-45.0, 45.0):                       # not inside the bay: the pack is 156 of 159 mm
        for s in (-1, 1):
            tops.append((x, s * (W / 2 - 4.0)))
    for s in (-1, 1):
        for y in (-60.0, -20.0, 20.0, 60.0):
            tops.append((s * (BAY_IN / 2 + 4.0), y))
    tops += nodes
    for (x, y) in tops:
        body = body.union(top_boss(x, y))
    for (x, y) in tops:
        body = body.cut(top_ins(x, y))
    # joint: inserts in the centre bulkheads, screws come from the end sections
    for s in (-1, 1):
        xa, xb = sorted((s * (HX - BULK_T - 1), s * (HX + 1)))
        for (y, z) in JOINT_SCREWS:
            body = body.cut(cyl_x(xa, xb, y, z, INS_M25))
        body = body.cut(cable_window(s * (HX - BULK_T - 1), s * (HX + 1)))
    # battery strap slots (2 straps across the pack)
    for sy in (-1, 1):
        for sx in (-1, 1):
            xs = sx * (BAY_IN / 2 - 3.5)
            body = body.cut(box(xs - 1.75, xs + 1.75, sy * 45 - 12.5, sy * 45 + 12.5, -1, FLOOR + 1))
    return body, tops

def cable_window(xa, xb):
    xa, xb = sorted((xa, xb))
    pts = [(-12.0, 9.0), (12.0, 9.0), (12.0, 20.0), (0.0, 32.0), (-12.0, 20.0)]
    return prism_yz(pts, xa, xb)

# =============================================================================
# MOTOR GEOMETRY (end-section local coords)
# =============================================================================
def motor_frame(s):
    """s=+1 left motor (shaft +Y), s=-1 right. Returns gearbox centre (x,z), face y, shaft dir angle."""
    gx = AXLE_XL + s * GB_DX
    return gx, MOTOR_CZ, s * Y_IN

def face_holes(s):
    gx, gz, _ = motor_frame(s)
    th_s = math.atan2(AXLE_Z - gz, AXLE_XL - gx)          # gearbox centre -> shaft
    return [(gx + FACE_BC_R * math.cos(th_s + math.radians(30 + 60 * k)),
             gz + FACE_BC_R * math.sin(th_s + math.radians(30 + 60 * k))) for k in range(6)]

# =============================================================================
# END SECTION  (local coords: x=0 joint face, x=L_S bumper face)
# =============================================================================
def end_section():
    body = box(0, L_S, -W / 2, W / 2, 0, H).edges("|Z and >X").fillet(10)
    inner = box(BULK_T, L_S - END_T, -Y_IN, Y_IN, FLOOR, H + 1).edges("|Z and >X").fillet(10 - SIDE_T)
    body = body.cut(inner)

    free_x1 = 40.0
    # divider between the electronics/X-grid zone and the motor strip
    body = body.union(box(free_x1 - RIB_T / 2, free_x1 + RIB_T / 2, -Y_IN, Y_IN, 0, H))
    # X-grid zone
    ycells = [-Y_IN, -40.0, 0.0, 40.0, Y_IN]
    nodes = []
    for y in ycells[1:-1]:
        body = body.union(box(BULK_T, free_x1, y - RIB_T / 2, y + RIB_T / 2, 0, H))
    for y0, y1 in zip(ycells[:-1], ycells[1:]):
        body = body.union(x_cell(BULK_T, free_x1, y0, y1, 0, H))
        body = body.cut(x_windows(BULK_T, free_x1, y0, y1))
        nodes.append(((BULK_T + free_x1) / 2, (y0 + y1) / 2))
    # (no centre rib here: each motor slides ~22 mm inboard during install)

    for s in (-1, 1):
        gx, gz, yf = motor_frame(s)
        ya, yb = sorted((s * (Y_IN - SAD_U[1]), s * (Y_IN - SAD_U[0])))
        body = body.union(box(gx - SAD_HW, gx + SAD_HW, ya, yb, FLOOR - 0.01, gz))
        # gussets: side wall -> floor, flanking the saddle
        for dx in (-1, 1):
            xg = gx + dx * (SAD_HW + 1.5)
            pts = [(s * (Y_IN + 0.5), 0), (s * (Y_IN + 0.5), H - 4), (s * (Y_IN - SAD_U[1] - 16.0), 0)]
            body = body.union(prism_yz(pts, xg - 1.5, xg + 1.5))

    # top mounting bosses
    tops = [(n[0], n[1]) for n in nodes]
    for xw in (80.0, 100.0, 160.0):        # world-grid x (= HX + local); none over the gearboxes
        for s in (-1, 1):
            tops.append((xw - HX, s * (W / 2 - 4.0)))
    for y in (-60.0, -20.0, 20.0, 60.0):
        tops.append((L_S - 4.0, y))
    for (x, y) in tops:
        body = body.union(top_boss(x, y))

    # ---- cuts ----
    for (x, y) in tops:
        body = body.cut(top_ins(x, y))
    for s in (-1, 1):
        gx, gz, yf = motor_frame(s)
        ya, yb = sorted((s * (Y_IN - 1), s * (W / 2 + 1)))
        body = body.cut(cyl_y(ya, yb, AXLE_XL, AXLE_Z, BUSH_D))
        body = body.cut(cone((AXLE_XL, s * (Y_IN - 0.01), AXLE_Z), (0, s, 0), BUSH_D + 2.0, BUSH_D - 0.1, 1.05))
        for (hx_, hz_) in face_holes(s):
            body = body.cut(cyl_y(ya, yb, hx_, hz_, CLR_M3_H))
            # countersink from the outside face
            body = body.cut(cone((hx_, s * (W / 2 + 0.01), hz_), (0, -s, 0), CSK_M3_D + 0.02, CLR_M3_H,
                                 (CSK_M3_D - CLR_M3_H) / 2 + 0.01))
        # clamp bore + cap-screw inserts
        ya, yb = sorted((s * (Y_IN - SAD_U[1] - 1), s * (Y_IN - SAD_U[0] + 1)))
        body = body.cut(cyl_y(ya, yb, gx, gz, GB_BORE))
        yc = s * (Y_IN - SAD_U[1] - 0.01)
        body = body.cut(cone((gx, yc, gz), (0, s, 0), GB_BORE + 2.4, GB_BORE - 0.1, 1.25))
        for dx in (-1, 1):
            for u in (SAD_U[0] + 5.0, SAD_U[1] - 5.0):
                body = body.cut(cyl_z(gz - 8.0, gz + 1, gx + dx * CAP_BOLT_DX, s * (Y_IN - u), INS_M25))

    # joint: 45 deg notch for the centre lip, peg sockets, screw clearance, cable window
    c = SLIDE * math.sqrt(2)
    notch = [(-1.0, LIP_Z0 - c - 1.0), (LIP + SLIDE, LIP_Z0 - c + LIP + SLIDE), (LIP + SLIDE, H + 1), (-1.0, H + 1)]
    body = body.cut(prism_xz(notch, -W / 2 - 1, W / 2 + 1))
    for py in (-PEG_Y, PEG_Y):
        body = body.cut(prism_yz(diamond(py, PEG_Z, PEG_R + SLIDE * 1.42), -1, PEG_L + 0.6))
    for (y, z) in JOINT_SCREWS:
        body = body.cut(cyl_x(-1, BULK_T + 1, y, z, CLR_M25_H))
    body = body.cut(cable_window(-1, BULK_T + 1))
    # bumper: 2x2 M2.5 inserts for a front sensor bracket (D435 etc.)
    for y in (-25.0, 25.0):
        for z in (18.0, 38.0):
            body = body.cut(cyl_x(L_S - INS_DEPTH, L_S + 1, y, z, INS_M25))
    return body, tops

# =============================================================================
# SMALL PARTS
# =============================================================================
def motor_cap(s=1):
    gx, gz, _ = motor_frame(s)
    ya, yb = sorted((s * (Y_IN - SAD_U[1]), s * (Y_IN - SAD_U[0])))
    cap = box(gx - SAD_HW, gx + SAD_HW, ya, yb, gz + CLAMP_GAP, CAP_TOP)
    cap = cap.edges("|Y and >Z").fillet(8)
    cap = cap.cut(cyl_y(ya - 1, yb + 1, gx, gz, GB_BORE))
    for dx in (-1, 1):
        for u in (SAD_U[0] + 5.0, SAD_U[1] - 5.0):
            x, y = gx + dx * CAP_BOLT_DX, s * (Y_IN - u)
            cap = cap.cut(cyl_z(gz, CAP_TOP + 1, x, y, CLR_M25_V))
            cap = cap.cut(cyl_z(gz + CLAMP_GAP + 10.0, CAP_TOP + 1, x, y, 5.0))   # counterbore
    return cap

def wheel_adapter():
    """Local frame: axis +Z, z = distance from the gearbox face."""
    u_hub0, u_face = SIDE_T + 2.5, SIDE_T + WHEEL_GAP + WHEEL_WEB   # 8.0 .. 27.7
    fl_t, hub_d, fl_d = 6.0, 18.0, 31.0
    hub = cyl_z(u_hub0, u_face - fl_t + 0.01, 0, 0, hub_d)
    c45 = cone((0, 0, u_face - fl_t - (fl_d - hub_d) / 2), (0, 0, 1), hub_d, fl_d, (fl_d - hub_d) / 2 + 0.01)
    flange = cyl_z(u_face - fl_t, u_face, 0, 0, fl_d)
    a = hub.union(c45).union(flange)
    a = a.union(cyl_z(u_face - 0.01, u_face + 2.0, 0, 0, PILOT_D))
    # 8x M2.5 heat-set inserts: 4 on the wheel's 24 mm circle (4.0 holes) + 4 on its 16 mm circle (3.0 holes)
    for k in range(4):
        for r, t0 in ((12.0, 0.0), (8.0, 45.0)):
            t = math.radians(t0 + 90 * k)
            a = a.cut(cyl_z(u_face - 5.5, u_face + 3, r * math.cos(t), r * math.sin(t), INS_M25))
    # D bore
    bore = cyl_z(u_hub0 - 1, u_hub0 + 14.6, 0, 0, DBORE_D).intersect(
        box(-10, DFLAT, -10, 10, u_hub0 - 2, u_hub0 + 20))
    a = a.cut(bore)
    a = a.cut(cone((0, 0, u_hub0 - 0.01), (0, 0, 1), DBORE_D + 1.2, DBORE_D - 0.2, 0.7))   # lead-in chamfer
    # radial M2.5 set screw onto the flat (heat-set insert from outside)
    a = a.cut(cyl_x(DFLAT - 0.5, hub_d / 2 + 1, 0, u_hub0 + 6.0, INS_M25))
    return a

def place_adapter(a, s):
    """Put the adapter on the left (s=1) or right (s=-1) axle in end-section local coords."""
    r = a.rotate((0, 0, 0), (1, 0, 0), -90) if s > 0 else a.rotate((0, 0, 0), (1, 0, 0), 90)
    return r.translate((AXLE_XL, s * Y_IN, AXLE_Z))

# --- reference-only: real motor STEP + a simplified wheel ---------------------
MOTOR_STEP = os.environ.get("MOTOR_STEP", "37d-gearmotor-19-30-encoder.step")
_motor_cache = {}
def motor_real(s):
    if "m" not in _motor_cache:
        m = cq.importers.importStep(MOTOR_STEP).translate((-19.93, 0, -19.92))
        _motor_cache["m"] = m
    m = _motor_cache["m"]
    base = m.rotate((0, 0, 0), (1, 0, 0), -90 if s > 0 else 90)
    clock = 200.0 if s > 0 else 340.0
    r = base.rotate((0, 0, 0), (0, 1, 0), clock)
    # place so the shaft centre sits on the axle and the face on the wall
    sh = np.array([0.0, -7.0, 0.0])
    def Rx(a):
        c, s_ = math.cos(a), math.sin(a); return np.array([[1, 0, 0], [0, c, -s_], [0, s_, c]])
    def Ry(a):
        c, s_ = math.cos(a), math.sin(a); return np.array([[c, 0, s_], [0, 1, 0], [-s_, 0, c]])
    R = Ry(math.radians(clock)) @ Rx(math.radians(-90 if s > 0 else 90))
    p = R @ sh
    return r.translate((AXLE_XL - p[0], s * Y_IN - p[1], AXLE_Z - p[2]))

def wheel_dummy(s):
    y0 = s * (W / 2 + WHEEL_GAP)
    ya, yb = sorted((y0, y0 + s * WHEEL_W))
    ring = cyl_y(ya, yb, AXLE_XL, AXLE_Z, 2 * WHEEL_RMAX).cut(cyl_y(ya - 1, yb + 1, AXLE_XL, AXLE_Z, 50))
    wa, wb = sorted((y0 + s * WHEEL_WEB, y0 + s * (WHEEL_WEB + WEB_T)))
    web = cyl_y(wa, wb, AXLE_XL, AXLE_Z, 52).cut(cyl_y(wa - 1, wb + 1, AXLE_XL, AXLE_Z, 8.1))
    for k in range(4):
        t = math.radians(45 + 90 * k)
        web = web.cut(cyl_y(wa - 1, wb + 1, AXLE_XL + 8 * math.cos(t), AXLE_Z + 8 * math.sin(t), 3.0))
        t = math.radians(90 * k)
        web = web.cut(cyl_y(wa - 1, wb + 1, AXLE_XL + 12 * math.cos(t), AXLE_Z + 12 * math.sin(t), 4.0))
    return ring.union(web)

# =============================================================================
def place_front(wp):
    return wp.translate((HX, 0, 0))

def place_rear(wp):
    return wp.rotate((0, 0, 0), (0, 0, 1), 180).translate((-HX, 0, 0))

def to_print(wp, flip=False):
    if flip:
        wp = wp.rotate((0, 0, 0), (1, 0, 0), 180)
    bb = wp.val().BoundingBox()
    return wp.translate((-(bb.xmin + bb.xmax) / 2, -(bb.ymin + bb.ymax) / 2, -bb.zmin))

def build(with_refs=True):
    center, c_tops = center_section()
    end, e_tops = end_section()
    adapter = wheel_adapter()
    parts = {
        "center_section_x1": to_print(center),
        "end_section_x2": to_print(end),
        "motor_cap_x4": to_print(motor_cap(1), flip=True),
        "wheel_adapter_x4": to_print(adapter),
    }
    asm = cq.Assembly(name="10C4I_v2")
    grey, white = cq.Color(0.32, 0.33, 0.36), cq.Color(0.88, 0.88, 0.86)
    asm.add(center, name="center_section", color=grey)
    asm.add(place_front(end), name="front_section", color=white)
    asm.add(place_rear(end), name="rear_section", color=white)
    for tag, place in (("F", place_front), ("R", place_rear)):
        for s, side in ((1, "L"), (-1, "R")):
            asm.add(place(motor_cap(s)), name=f"cap_{tag}{side}", color=white)
            asm.add(place(place_adapter(adapter, s)), name=f"adapter_{tag}{side}", color=cq.Color(0.85, 0.45, 0.1))
            if with_refs:
                asm.add(place(motor_real(s)), name=f"REF_motor_{tag}{side}", color=cq.Color(0.7, 0.7, 0.72))
                asm.add(place(wheel_dummy(s)), name=f"REF_wheel_{tag}{side}", color=cq.Color(0.1, 0.1, 0.1))
    asm.add(box(-BATT[1] / 2, BATT[1] / 2, -BATT[0] / 2, BATT[0] / 2, FLOOR, FLOOR + BATT[2]),
            name="REF_battery_6S_5200", color=cq.Color(0.2, 0.3, 0.6))
    return asm, parts, dict(center=center, end=end, adapter=adapter, c_tops=c_tops, e_tops=e_tops)

if __name__ == "__main__":
    out = os.environ.get("OUT_DIR", "out")
    os.makedirs(out, exist_ok=True)
    refs = os.path.exists(MOTOR_STEP)   # Pololu STEP is optional: without it, no REF_ motors/wheels
    if not refs:
        print(f"note: {MOTOR_STEP} not found, exporting without reference motors/wheels")
    asm, parts, raw = build(with_refs=refs)
    asm.export(os.path.join(out, "10C4I_v2_assembly.step"))
    for name, wp in parts.items():
        cq.exporters.export(wp, os.path.join(out, f"{name}.step"))
        cq.exporters.export(wp, os.path.join(out, f"{name}.stl"), tolerance=0.02, angularTolerance=0.05)
        bb = wp.val().BoundingBox()
        fits = (bb.xlen <= BED[0] and bb.ylen <= BED[1]) or (bb.ylen <= BED[0] and bb.xlen <= BED[1])
        print(f"{name:20s} {bb.xlen:6.1f} x {bb.ylen:6.1f} x {bb.zlen:5.1f}  vol {wp.val().Volume()/1000:6.1f} cm3  "
              f"fits MK4S: {fits and bb.zlen <= BED[2]}")
