import json
import os

import airo_blender as ab
import bpy
import numpy as np
from linen.blender.frame import add_frame
from robotics_renders.assets import load_collection_asset_as_real
from robotics_renders.robots.posing import set_joint_angles
from robotics_renders.robots.ur5e_with_robotiq import add_ur5e_with_robotiq

bpy.data.objects.remove(bpy.data.objects["Cube"], do_unlink=True)
bpy.data.objects.remove(bpy.data.objects["Light"], do_unlink=True)

asset_snapshot_path = os.path.join(os.path.dirname(__file__), "../assets/asset_snapshot.json")
with open(asset_snapshot_path, "r") as file:
    assets = json.load(file)["assets"]

# Setting up the shelves
shelves_info = [asset for asset in assets if asset["name"] == "steel_frame_shelves_01"][0]
shelves = load_collection_asset_as_real(**shelves_info)

y_shift = 0.3
shelves.rotation_euler = (0, 0, np.deg2rad(90))
shelves.location = (0.15, -0.324 + y_shift, 0)
shelves.scale = (0.6, 0.6, 0.6)

shelves_fake_pose = np.identity(4)
shelves_fake_pose[1, 3] = y_shift
add_frame(shelves_fake_pose, 0.3, name="Shelves Pose")

# Setting up the spray
spray_info = [asset for asset in assets if asset["name"] == "lubricant_spray"][0]
spray = load_collection_asset_as_real(**spray_info)
spray_location = (0.2, 0.04, 0.69)

# Quick fix
spray_tin = bpy.data.objects["lubricant_spray_tin.001"]
spray_tape = bpy.data.objects["lubricant_spray_tape.001"]

spray.location = spray_location
spray_tin.location = spray_location
spray_tape.location = spray_location

ur5e, ur5e_links, _, ur5e_joints, _ = add_ur5e_with_robotiq()  # type: ignore

ur5e.location = (1.5, 0, 0)
home_joints = np.deg2rad([270, -45, -90, -45, 0, 180])
set_joint_angles(home_joints, ur5e_joints)

# Setting up the scene camera
camera = bpy.data.objects["Camera"]
camera.location = (2.25, 3, 1.7)
camera.rotation_euler = np.deg2rad([69.0, 0.0, 155.0])  # type: ignore

bpy.context.view_layer.update()
ur5e_pose = np.array(ur5e.matrix_world)
tool_pose = np.array(ur5e_links["wrist_3_link"].matrix_world)

spray_pose = np.array(spray.matrix_world)

tcp_offset = np.array([0.0, 0.0, 0.172])
tcp_transform = np.identity(4)
tcp_transform[:3, 3] = tcp_offset

tcp_pose = tool_pose @ tcp_transform

add_frame(ur5e_pose, 0.3, name="UR5e Pose")
add_frame(tcp_pose, 0.15, name="TCP Pose")
add_frame(spray_pose, 0.2, name="Spray Pose")

# Add a large ground plane
bpy.ops.mesh.primitive_plane_add(size=20)

# Then to complete the scene, I like to add the photo_studio_01 HDRI from polyhaven
scene = bpy.context.scene
hdri_infos = [asset for asset in assets if asset["name"] == "photo_studio_01"]

if len(hdri_infos) > 0:
    hdri = ab.load_asset(**hdri_infos[0])
    scene.world = hdri

scene.render.engine = "CYCLES"
scene.cycles.samples = 64
scene.view_settings.look = "High Contrast"
