import json

import airo_blender as ab

all_assets = ab.available_assets()
asset_snapshot = {"assets": all_assets}

with open("asset_snapshot.json", "w") as file:
    json.dump(asset_snapshot, file, indent=4)
