import json
import os

import airo_blender as ab
import bpy
import numpy as np
from linen.blender.frame import add_frame
from linen.blender.points import add_points

bpy.data.objects.remove(bpy.data.objects["Cube"], do_unlink=True)
bpy.data.objects.remove(bpy.data.objects["Light"], do_unlink=True)

asset_snapshot_path = os.path.join(os.path.dirname(__file__), "../assets/asset_snapshot.json")
with open(asset_snapshot_path, "r") as file:
    assets = json.load(file)["assets"]

A = np.identity(4)
B = np.identity(4)
B[1, 3] = 3.0

add_frame(A, 1.0, name="A")
add_frame(B, 1.0, name="B")

point = np.array([0.0, 2.0, 0.0])
soft_yellow = (1.0, 0.8, 0.1)
add_points([point], 0.1, soft_yellow)

camera = bpy.data.objects["Camera"]
camera.location = (6.3, 4.8, 3.3)
camera.rotation_euler = np.deg2rad([66.0, 0.0, 115.0])  # type: ignore

# TODO finish

scene = bpy.context.scene
hdri_infos = [asset for asset in assets if asset["name"] == "photo_studio_01"]

if len(hdri_infos) > 0:
    hdri = ab.load_asset(**hdri_infos[0])
    scene.world = hdri

scene.render.engine = "CYCLES"
scene.cycles.samples = 64
scene.view_settings.look = "High Contrast"
