import airo_blender as ab
import bpy
import urdf_workshop

bpy.ops.object.delete()

ab.import_urdf(urdf_workshop.ur5e)
