from typing import Dict, Tuple

import airo_blender as ab
import bpy
import numpy as np
import urdf_workshop


def add_ur5e_with_robotiq() -> (
    Tuple[
        bpy.types.Object,
        Dict[str, bpy.types.Object],
        Dict[str, bpy.types.Object],
        Dict[str, bpy.types.Object],
        bpy.types.Object,
    ]
):
    arm_joints, _, arm_links = ab.import_urdf(urdf_workshop.ur5e)
    tool_link = arm_links["wrist_3_link"]

    gripper_joints, _, gripper_links = ab.import_urdf(urdf_workshop.robotiq_2f85)

    # Parenting the gripper to the robot
    gripper_bases = [link for link in gripper_links.values() if link.parent is None]
    gripper_base = gripper_bases[0]
    gripper_base.parent = tool_link

    # Closing the gripper
    gripper_joint = gripper_joints["finger_joint"]
    gripper_joint.rotation_euler = (0, 0, np.deg2rad(42))

    links = {**arm_links, **gripper_links}

    base_links = [link for link in links.values() if link.parent is None]
    base_link = base_links[0]

    return base_link, arm_links, gripper_links, arm_joints, gripper_joint
