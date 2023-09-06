import airo_blender as ab
import bpy
import numpy as np
import urdf_workshop

bpy.ops.object.delete()

_, _, arm_links = ab.import_urdf(urdf_workshop.ur5e)
tool_link = arm_links["wrist_3_link"]

gripper_joints, _, gripper_links = ab.import_urdf(urdf_workshop.robotiq_2f85)

# Parenting the gripper to the robot
gripper_bases = [link for link in gripper_links.values() if link.parent is None]
gripper_base = gripper_bases[0]
gripper_base.parent = tool_link

# Closing the gripper
gripper_joint = gripper_joints["finger_joint"]
gripper_joint.rotation_euler = (0, 0, np.deg2rad(42))
