import airo_blender as ab
import bpy


def load_collection_asset_as_real(name: str, relative_path: str, library: str, type: str, **kwargs) -> bpy.types.ID:
    # This messy code turns the collection instance to a real object and removes the extra empty that was created
    collection = ab.load_asset(name, relative_path, library, type, **kwargs)
    bpy.ops.object.collection_instance_add(collection=collection.name)
    empty = bpy.context.selected_objects[0]
    bpy.ops.object.duplicates_make_real(use_base_parent=False, use_hierarchy=True)
    first_object = bpy.context.selected_objects[0]
    bpy.ops.object.select_all(action="DESELECT")
    empty.select_set(True)
    bpy.ops.object.delete()
    first_object.select_set(True)
    bpy.context.view_layer.objects.active = first_object
    return first_object
