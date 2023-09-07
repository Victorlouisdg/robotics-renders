import json
import os

import bpy
from robotics_renders.assets import load_collection_asset_as_real

bpy.ops.object.delete()

asset_snapshot_path = os.path.join(os.path.dirname(__file__), "../assets/asset_snapshot.json")
with open(asset_snapshot_path, "r") as file:
    assets = json.load(file)["assets"]

zed2i_info = [asset for asset in assets if asset["name"] == "ZED2i"][0]
zed2i = load_collection_asset_as_real(**zed2i_info)
zed2i.location = (0, 0, 1.0)
