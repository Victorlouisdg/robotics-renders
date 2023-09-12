from typing import Dict

import bpy
import numpy as np


def set_joint_angles(joint_angles: np.ndarray, arm_joints: Dict[str, bpy.types.Object]) -> None:
    for joint, joint_angle in zip(arm_joints.values(), joint_angles):
        joint.rotation_euler = (0, 0, joint_angle)
