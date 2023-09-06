import airo_blender as ab
import urdf_workshop
import bpy

bpy.ops.object.delete()

ab.import_urdf(urdf_workshop.ur5e)
