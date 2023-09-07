import json
import os

import airo_blender as ab
import bpy
import numpy as np
from airo_typing import HomogeneousMatrixType
from linen.blender.frame import add_frame
from linen.blender.path import add_path
from linen.path.linear import linear_path
from robotics_renders.assets import load_collection_asset_as_real
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

# ur5e = ab.import_urdf(urdf_workshop.ur5e)
# ur5e.location = (1.0, 0, 0)

ur5e, _, _, ur5e_joints, _ = add_ur5e_with_robotiq()

ur5e.location = (1.5, 0, 0)
# home_joints = np.deg2rad([-180, -30, 75, -135, -45, 0])
home_joints = np.deg2rad([270, -45, -90, -45, 0, 0])
set_joint_angles(home_joints, ur5e_joints)

# Setting up the scene camera
camera = bpy.data.objects["Camera"]
camera.location = (2.25, 3, 1.7)
camera.rotation_euler = np.deg2rad([69.0, 0.0, 155.0])


def blender_to_airo_camera_pose_convention(blender_pose: HomogeneousMatrixType) -> HomogeneousMatrixType:
    pose = np.array(blender_pose)
    pose[:, [1, 2]] *= -1  # Flip y and z axes
    return pose


zed2i_left = zed2i.children[0]
zed2i_left_pose = blender_to_airo_camera_pose_convention(zed2i_left.matrix_world)

bpy.context.view_layer.update()
ur5e_pose = np.array(ur5e.matrix_world)

add_frame(zed2i_left_pose, 0.2, name="ZED2i Left Pose")
add_frame(ur5e_pose, 0.3, name="UR5e Pose")

start = zed2i_left_pose[:3, 3]
end = ur5e_pose[:3, 3]
print(start, end)
robot_to_camera_path = linear_path(start, end)

soft_yellow = (1.0, 0.8, 0.1)
add_path(robot_to_camera_path, points_per_second=100, color=soft_yellow, radius=0.006)


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
