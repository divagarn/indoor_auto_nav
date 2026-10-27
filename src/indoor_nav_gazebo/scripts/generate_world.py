#!/usr/bin/env python3
"""Generates worlds/indoor_house.world (walls + furniture/objects). Run: python3 generate_world.py > ../worlds/indoor_house.world"""

WALL_H, WALL_T = 2.5, 0.15
models = []


def box_model(name, x, y, z, sx, sy, sz, rgba, yaw=0.0, static=True):
    r, g, b, a = rgba
    return f"""    <model name="{name}">
      <static>{str(static).lower()}</static>
      <pose>{x} {y} {z} 0 0 {yaw}</pose>
      <link name="link">
        <collision name="c"><geometry><box><size>{sx} {sy} {sz}</size></box></geometry></collision>
        <visual name="v"><geometry><box><size>{sx} {sy} {sz}</size></box></geometry>
          <material><ambient>{r} {g} {b} {a}</ambient><diffuse>{r} {g} {b} {a}</diffuse></material></visual>
      </link>
    </model>"""


def cyl_model(name, x, y, radius, length, rgba):
    r, g, b, a = rgba
    return f"""    <model name="{name}">
      <static>true</static>
      <pose>{x} {y} {length/2} 0 0 0</pose>
      <link name="link">
        <collision name="c"><geometry><cylinder><radius>{radius}</radius><length>{length}</length></cylinder></geometry></collision>
        <visual name="v"><geometry><cylinder><radius>{radius}</radius><length>{length}</length></cylinder></geometry>
          <material><ambient>{r} {g} {b} {a}</ambient><diffuse>{r} {g} {b} {a}</diffuse></material></visual>
      </link>
    </model>"""


def sphere_model(name, x, y, radius, rgba):
    r, g, b, a = rgba
    return f"""    <model name="{name}">
      <static>true</static>
      <pose>{x} {y} {radius} 0 0 0</pose>
      <link name="link">
        <collision name="c"><geometry><sphere><radius>{radius}</radius></sphere></geometry></collision>
        <visual name="v"><geometry><sphere><radius>{radius}</radius></sphere></geometry>
          <material><ambient>{r} {g} {b} {a}</ambient><diffuse>{r} {g} {b} {a}</diffuse></material></visual>
      </link>
    </model>"""


n = 0
def wall(x1, y1, x2, y2):
    global n
    n += 1
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    length = max(abs(x2 - x1), abs(y2 - y1)) + WALL_T
    horizontal = abs(x2 - x1) > abs(y2 - y1)
    sx, sy = (length, WALL_T) if horizontal else (WALL_T, length)
    models.append(box_model(f"wall_{n}", cx, cy, WALL_H / 2, sx, sy, WALL_H, (0.85, 0.85, 0.8, 1)))


def wall_with_doors(fixed, a, b, doors, vertical):
    """Wall along the varying axis from a..b at position `fixed`, with door gaps [(centre, width)]."""
    cur = a
    for c, w in sorted(doors):
        s, e = c - w / 2, c + w / 2
        if s > cur:
            wall(fixed, cur, fixed, s) if vertical else wall(cur, fixed, s, fixed)
        cur = e
    if cur < b:
        wall(fixed, cur, fixed, b) if vertical else wall(cur, fixed, b, fixed)


# Layout (metres): 12 x 8 house, x in [-6,6], y in [-4,4]
#   Room A (bedroom)  x[-6,-2]
#   Room B (living)   x[-2, 2]
#   Room C (kitchen)  x[ 2, 6] y[ 0, 4]
#   Room D (office)   x[ 2, 6] y[-4, 0]
wall_with_doors(4, -6, 6, [], vertical=False)       # north outer
wall_with_doors(-4, -6, 6, [], vertical=False)      # south outer
wall_with_doors(-6, -4, 4, [], vertical=True)       # west outer
wall_with_doors(6, -4, 4, [], vertical=True)        # east outer
wall_with_doors(-2, -4, 4, [(-1.0, 1.0), (2.5, 1.0)], vertical=True)   # A | B
wall_with_doors(2, -4, 4, [(1.0, 1.0), (-2.0, 1.0)], vertical=True)    # B | C,D
wall_with_doors(0, 2, 6, [(4.0, 1.0)], vertical=False)                 # C / D

C = {  # colours
    'red': (0.8, 0.1, 0.1, 1), 'green': (0.1, 0.6, 0.2, 1), 'blue': (0.1, 0.2, 0.8, 1),
    'yellow': (0.9, 0.8, 0.1, 1), 'brown': (0.45, 0.28, 0.12, 1), 'white': (0.95, 0.95, 0.95, 1),
    'grey': (0.4, 0.4, 0.4, 1), 'black': (0.08, 0.08, 0.08, 1), 'orange': (0.95, 0.5, 0.1, 1),
}

# --- Bedroom (A) ---
models.append(box_model("bed", -4.6, 2.8, 0.25, 2.0, 1.5, 0.5, C['blue']))
models.append(box_model("wardrobe", -5.5, -3.2, 1.0, 0.6, 1.6, 2.0, C['brown']))
models.append(box_model("nightstand", -3.2, 3.5, 0.25, 0.4, 0.4, 0.5, C['brown']))
models.append(cyl_model("plant_bedroom", -2.6, -3.3, 0.2, 0.8, C['green']))
# --- Living room (B) ---
models.append(box_model("sofa", 0.0, 3.3, 0.35, 2.0, 0.8, 0.7, C['red']))
models.append(box_model("coffee_table", 0.0, 1.8, 0.2, 1.0, 0.6, 0.4, C['brown']))
models.append(box_model("tv_stand", 0.0, -3.6, 0.3, 1.4, 0.4, 0.6, C['black']))
models.append(cyl_model("plant_living", 1.5, -3.3, 0.25, 1.0, C['green']))
models.append(sphere_model("ball", -0.8, -0.5, 0.15, C['orange']))
# --- Kitchen (C) ---
models.append(box_model("fridge", 5.5, 3.4, 0.9, 0.7, 0.7, 1.8, C['white']))
models.append(box_model("kitchen_counter", 4.0, 3.5, 0.45, 2.4, 0.6, 0.9, C['grey']))
models.append(box_model("dining_table", 3.9, 1.6, 0.375, 1.4, 0.9, 0.75, C['brown']))
models.append(cyl_model("trash_bin", 2.5, 3.5, 0.18, 0.5, C['black']))
# --- Office (D) ---
models.append(box_model("desk", 5.4, -2.0, 0.375, 0.8, 1.6, 0.75, C['brown']))
models.append(box_model("office_chair", 4.5, -2.0, 0.25, 0.5, 0.5, 0.5, C['black']))
models.append(box_model("bookshelf", 3.9, -3.6, 0.9, 1.6, 0.35, 1.8, C['yellow']))
models.append(box_model("box_cardboard", 2.7, -0.8, 0.2, 0.4, 0.4, 0.4, C['orange']))

print(f"""<?xml version="1.0"?>
<sdf version="1.6">
  <world name="indoor_house">
    <include><uri>model://sun</uri></include>
    <include><uri>model://ground_plane</uri></include>
    <physics type="ode">
      <max_step_size>0.004</max_step_size>
      <real_time_update_rate>250</real_time_update_rate>
    </physics>
    <scene><ambient>0.5 0.5 0.5 1</ambient><shadows>false</shadows></scene>
    <gravity>0 0 -9.8</gravity>
    <!-- ceiling-less so the sun lights the rooms -->
{chr(10).join(models)}
  </world>
</sdf>""")
