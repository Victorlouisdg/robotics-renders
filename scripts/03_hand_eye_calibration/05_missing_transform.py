import json
import os

import airo_blender as ab
import bpy
import numpy as np
from linen.blender.frame import add_frame
from linen.blender.path import add_path
from linen.path.linear import linear_path
from mathutils import Matrix
from robotics_renders.assets import load_collection_asset_as_real
from robotics_renders.coordinate_conventions import blender_to_airo_camera_pose_convention
from robotics_renders.robots.posing import set_joint_angles
from robotics_renders.robots.ur5e_with_robotiq import add_ur5e_with_robotiq

bpy.data.objects.remove(bpy.data.objects["Cube"], do_unlink=True)
bpy.data.objects.remove(bpy.data.objects["Light"], do_unlink=True)

asset_snapshot_path = os.path.join(os.path.dirname(__file__), "../assets/asset_snapshot.json")
with open(asset_snapshot_path, "r") as file:
    assets = json.load(file)["assets"]

zed2i_info = [asset for asset in assets if asset["name"] == "ZED2i"][0]
zed2i = load_collection_asset_as_real(**zed2i_info)
zed2i.location = (0, 0, 1.0)
zed2i.rotation_euler = (0, np.deg2rad(15), 0)

ur5e, ur5e_links, _, ur5e_joints, _ = add_ur5e_with_robotiq()  # type: ignore

ur5e.location = (1.5, 0, 0)
home_joints = np.deg2rad([270, -45, -90, -45, 0, 120])
set_joint_angles(home_joints, ur5e_joints)

# Setting up the scene camera
camera = bpy.data.objects["Camera"]
camera.location = (2.25, 3, 1.7)
camera.rotation_euler = np.deg2rad([69.0, 0.0, 155.0])  # type: ignore

zed2i_left = zed2i.children[0]  # type: ignore
zed2i_left_pose = blender_to_airo_camera_pose_convention(zed2i_left.matrix_world)

charuco_info = [asset for asset in assets if asset["name"] == "airo_charuco"][0]
charuco = ab.load_asset(**charuco_info)
bpy.context.scene.collection.objects.link(charuco)

board_offset = np.array([0.0, 0.06, 0.48])
orientation = Matrix.Rotation(-np.pi / 2, 3, "Y")
local_Z = orientation.col[2]  # type: ignore
orientation = Matrix.Rotation(-np.pi / 2 - np.pi / 4, 3, local_Z) @ orientation  # type: ignore
board_transform = np.identity(4)
board_transform[:3, :3] = orientation  # .to_numpy()
board_transform[:3, 3] = board_offset

charuco.parent = ur5e_links["wrist_3_link"]
charuco.matrix_parent_inverse = Matrix(board_transform)

bpy.context.view_layer.update()
ur5e_pose = np.array(ur5e.matrix_world)
board_pose = np.array(charuco.matrix_world)
tool_pose = np.array(ur5e_links["wrist_3_link"].matrix_world)

add_frame(zed2i_left_pose, 0.2, name="ZED2i Left Pose")
add_frame(ur5e_pose, 0.3, name="UR5e Pose")
add_frame(board_pose, 0.15, name="Charuco Board Pose")
add_frame(tool_pose, 0.15, name="Tool Pose")


robot_to_tool_path = linear_path(ur5e_pose[:3, 3], tool_pose[:3, 3])
camera_to_board_path = linear_path(zed2i_left_pose[:3, 3], board_pose[:3, 3])

soft_yellow = (1.0, 0.8, 0.1)
add_path(robot_to_tool_path, points_per_second=60, color=soft_yellow, radius=0.006)
add_path(camera_to_board_path, points_per_second=60, color=soft_yellow, radius=0.006)


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
