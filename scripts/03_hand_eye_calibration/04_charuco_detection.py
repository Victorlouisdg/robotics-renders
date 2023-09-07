import json
import os

import airo_blender as ab
import bpy
import numpy as np
from linen.blender.frame import add_frame
from robotics_renders.assets import load_collection_asset_as_real
from robotics_renders.coordinate_conventions import blender_to_airo_camera_pose_convention

bpy.ops.object.delete()

asset_snapshot_path = os.path.join(os.path.dirname(__file__), "../assets/asset_snapshot.json")
with open(asset_snapshot_path, "r") as file:
    assets = json.load(file)["assets"]

charuco_info = [asset for asset in assets if asset["name"] == "airo_charuco"][0]
charuco = ab.load_asset(**charuco_info)
bpy.context.scene.collection.objects.link(charuco)

location0 = (1, 0.15, 0.8)
rotation_euler0 = np.deg2rad([270, 0, -90])
pose0 = (location0, rotation_euler0)

location1 = (0.75, -0.1, 0.95)
rotation_euler1 = np.deg2rad([250, -23, -138])
pose1 = (location1, rotation_euler1)

location2 = (0.65, 0.25, 0.6)
rotation_euler2 = np.deg2rad([200, 0, -70])
pose2 = (location2, rotation_euler2)

keyposes = [pose0, pose1, pose2, pose0]
frames_between_poses = 50

for i, (location, rotation_euler) in enumerate(keyposes):
    charuco.location = location
    charuco.rotation_euler = rotation_euler
    frame = i * frames_between_poses + 1
    charuco.keyframe_insert(data_path="location", frame=frame)
    charuco.keyframe_insert(data_path="rotation_euler", frame=frame)

bpy.context.scene.frame_end = frame

charuco_pose = add_frame(np.identity(4), 0.1, name="Charuco Pose")
charuco_pose.parent = charuco


zed2i_info = [asset for asset in assets if asset["name"] == "ZED2i"][0]
zed2i = load_collection_asset_as_real(**zed2i_info)
zed2i.location = (0, 0, 1.0)
zed2i.rotation_euler = (0, np.deg2rad(15), 0)
zed2i_left = zed2i.children[0]

bpy.context.view_layer.update()
zed2i_left_pose = blender_to_airo_camera_pose_convention(zed2i_left.matrix_world)
add_frame(zed2i_left_pose, 0.2, name="ZED2i Left Pose", radius_height_ratio=0.025)

# Setting up the scene camera
camera = bpy.data.objects["Camera"]
camera.location = (-0.45, 1.5, 1.55)
camera.rotation_euler = np.deg2rad([66.8, 0.0, 212.0])


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
