"""
10C4I fit/tolerance coupon. Print it in the SAME filament + settings you'll use for the chassis.
Plate (flat, like the chassis floors):   M2.5 insert holes, M2.5 clearance holes, tongue slots
Wall  (standing, like the motor towers): horizontal M3 motor-face holes, M2.5 holes, gearbox-bushing holes
Key bar (print next to it):              5.00 mm wide, test it in the slots
"""
import cadquery as cq

T_PLATE, L, W = 8.0, 104.0, 52.0
WALL_T, WALL_H = 6.0, 34.0

def label(wp_face, txt, x, y, size=3.2, depth=0.6):
    return (cq.Workplane(wp_face).text(txt, size, -depth, combine=False, halign="center", valign="center")
            .translate((x, y, 0)))

plate = cq.Workplane("XY").box(L, W, T_PLATE, centered=(False, False, False))
plate = plate.edges("|Z").fillet(3)

insert_d = [2.9, 3.0, 3.1, 3.2, 3.3]           # Pofsnnx M2.5 inserts, 3.5 mm OD
clear25  = [2.7, 2.8, 2.9, 3.0, 3.1]           # M2.5 clearance (vertical)
slots    = [5.1, 5.2, 5.3, 5.4]                # 5.00 key -> 0.05..0.20 per side

xs5 = [12 + i * 20 for i in range(5)]
cuts = []
for x, d in zip(xs5, insert_d):     # blind 6.5 mm, like the chassis bosses
    cuts.append(cq.Workplane("XY").workplane(offset=T_PLATE - 6.5).center(x, 42).circle(d / 2).extrude(7))
for x, d in zip(xs5, clear25):      # through
    cuts.append(cq.Workplane("XY").workplane(offset=-1).center(x, 26).circle(d / 2).extrude(T_PLATE + 2))
xs4 = [16 + i * 24 for i in range(4)]
for x, w in zip(xs4, slots):
    cuts.append(cq.Workplane("XY").box(w, 12, 4.01, centered=(True, False, False)).translate((x, 4, T_PLATE - 4)))
for c in cuts:
    plate = plate.cut(c)

# engraved labels on top face
top = cq.Workplane("XY").workplane(offset=T_PLATE)
for x, d in zip(xs5, insert_d):
    plate = plate.cut(label("XY", f"{d:.1f}", x, 34.5).translate((0, 0, T_PLATE)))
for x, d in zip(xs5, clear25):
    plate = plate.cut(label("XY", f"{d:.1f}", x, 19.5).translate((0, 0, T_PLATE)))
for x, w in zip(xs4, slots):
    plate = plate.cut(label("XY", f"{w:.1f}", x + 8, 10, size=2.8).translate((0, 0, T_PLATE)))
plate = plate.cut(label("XY", "INS", 3.5, 47.5, size=2.4).translate((0, 0, T_PLATE)))

# standing wall along the back edge (holes print horizontal, same as the motor towers)
wall = cq.Workplane("XY").box(L, WALL_T, WALL_H, centered=(False, False, False)).translate((0, W, 0))
bush = [12.0, 12.2, 12.4, 12.6]                 # gearbox bushing is 12.0 nominal
m3   = [3.2, 3.3, 3.4, 3.5]                     # motor face screws
m25h = [2.7, 2.8, 2.9, 3.0]                     # M2.5 clearance, horizontal
def hole_y(x, z, d):
    return (cq.Workplane("XZ").workplane(offset=-(W - 1)).center(x, z).circle(d / 2).extrude(-(WALL_T + 2)))
for x, d in zip([12 + i * 24 for i in range(4)], bush):
    wall = wall.cut(hole_y(x, 16, d))
for i, d in enumerate(m3 + m25h):
    wall = wall.cut(hole_y(9 + i * 12.2, 26, d))
# labels on the wall's front face (normal -Y)
for x, d in zip([12 + i * 24 for i in range(4)], bush):
    t = cq.Workplane("XZ").text(f"{d:.1f}", 2.4, -0.6, combine=False, halign="center", valign="center").translate((x + 12.0, W, 16))
    wall = wall.cut(t)
for i, d in enumerate(m3 + m25h):
    t = cq.Workplane("XZ").text(f"{d:.1f}", 2.2, -0.6, combine=False, halign="center").translate((9 + i * 12.2, W, 31.3))
    wall = wall.cut(t)
coupon = plate.union(wall)

key = cq.Workplane("XY").box(40, 5.0, 4.0, centered=(False, True, False)).edges("|Z").chamfer(0.4)

if __name__ == "__main__":
    import os
    out = os.environ.get("OUT_DIR", ".")
    both = coupon.union(key.translate((L / 2 - 20, -10, 0)))
    cq.exporters.export(both, os.path.join(out, "10C4I_tolerance_coupon.stl"), tolerance=0.02, angularTolerance=0.1)
    cq.exporters.export(both, os.path.join(out, "10C4I_tolerance_coupon.step"))
    bb = both.val().BoundingBox()
    print("coupon bbox %.1f x %.1f x %.1f  vol %.1f cm3  valid %s solids %d" % (bb.xlen, bb.ylen, bb.zlen, both.val().Volume()/1000, both.val().isValid(), len(both.solids().vals())))
