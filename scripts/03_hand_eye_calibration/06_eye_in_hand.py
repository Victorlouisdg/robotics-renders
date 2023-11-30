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

ur5e, ur5e_links, gripper_links, ur5e_joints, _ = add_ur5e_with_robotiq()  # type: ignore

ur5e.location = (1.5, 0, 0)
# home_joints = np.deg2rad([-180, -30, 75, -135, -45, 0])
home_joints = np.deg2rad([270, -45, -90, -45, 0, 0])
set_joint_angles(home_joints, ur5e_joints)

zed2i.parent = ur5e_links["wrist_3_link"]

zed2i_mpi = np.identity(4)
X = np.array([0.0, 0.0, 1.0])
Z = np.array([0.0, -1.0, 0.0])
Y = np.cross(Z, X)
orientation = np.column_stack([X, Y, Z])
# orientation = np.linalg.inv(orientation)

zed2i_mpi[:3, :3] = np.column_stack([X, Y, Z])
zed2i_mpi[:3, 3] = np.array([0.0, -0.06, 0.05])

# m = np.linalg.inv(zed2i_mpi)
# m[:3, 3] = np.array([0.0, 0.0, 0.175])

zed2i.matrix_parent_inverse = Matrix(zed2i_mpi)


# Setting up the scene camera
camera = bpy.data.objects["Camera"]

# camera.parent = ur5e_links["wrist_3_link"]


bpy.context.view_layer.update()
ur5e_pose = np.array(ur5e.matrix_world)

zed2i_left = zed2i.children[0]  # type: ignore
zed2i_left_pose = blender_to_airo_camera_pose_convention(zed2i_left.matrix_world)


ur5e_wrist_pose = np.array(ur5e_links["wrist_3_link"].matrix_world)
ur5e_wrist_pose[:3, 3] += ur5e_wrist_pose[:3, :3] @ np.array([0.0, 0.0, 0.175])  # Add tcp offset

add_frame(zed2i_left_pose, 0.2, name="ZED2i Left Pose")
add_frame(ur5e_wrist_pose, 0.2, name="UR5e Wrist Pose")

start = zed2i_left_pose[:3, 3]
end = ur5e_wrist_pose[:3, 3]
print(start, end)
robot_to_camera_path = linear_path(start, end)

soft_yellow = (1.0, 0.8, 0.1)
add_path(robot_to_camera_path, points_per_second=10, color=soft_yellow, radius=0.006)


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

scene.render.resolution_x = 1400
scene.render.resolution_y = 200

camera.data.lens = 100
camera.location = (-1.9371, 6.22239, 2.52928)
camera.rotation_euler = np.deg2rad([75.9594, 0.0, 206.693])
