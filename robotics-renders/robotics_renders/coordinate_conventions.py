import numpy as np
from airo_typing import HomogeneousMatrixType


def blender_to_airo_camera_pose_convention(blender_pose: HomogeneousMatrixType) -> HomogeneousMatrixType:
    pose = np.array(blender_pose)
    pose[:, [1, 2]] *= -1  # Flip y and z axes
    return pose
