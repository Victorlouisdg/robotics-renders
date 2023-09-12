import bpy
import numpy as np
from robotics_renders.robots.posing import set_joint_angles
from robotics_renders.robots.ur5e_with_robotiq import add_ur5e_with_robotiq

bpy.ops.object.delete()

# not sure what the type problem is here
_, _, _, arm_joints, _ = add_ur5e_with_robotiq()  # type: ignore
# home_joints = np.deg2rad([-180, -30, 75, -135, -45, 0])
initial_joints = np.zeros(6)
home_joints = np.deg2rad([180, -45, -90, -45, 0, 0])

fps = 24
n_frames_animated = 4 * fps
n_frames_still = 2 * fps

bpy.context.scene.frame_end = n_frames_animated + n_frames_still

t_values = np.linspace(0, 1, n_frames_animated)

for i, t in enumerate(t_values):
    joints = (1 - t) * initial_joints + t * home_joints
    set_joint_angles(joints, arm_joints)

    # Insert keyframes
    for joint in arm_joints.values():
        joint.keyframe_insert(data_path="rotation_euler", index=2, frame=i + 1)


# Setting up the camera
camera = bpy.data.objects["Camera"]
camera.location = np.array([0.1, 4.2802, 1.63528])  # type: ignore
camera.rotation_euler = np.deg2rad([74.4, 0.0, 180.0])  # type: ignore

scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 64
scene.render.resolution_x = 1400
scene.render.resolution_y = 400
