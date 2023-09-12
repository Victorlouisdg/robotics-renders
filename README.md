# robotics-renders

![Banner](https://i.imgur.com/y2x5oGs.png)

Illustrations and animations of robotics concepts using Blender.
We build the Blender scenes using Python scripts as much of possible.

## Getting started :rocket:

After completing the installation, see the [scripts](./scripts/) folder for the available scripts.
Run them with Blender like so:

```
blender -P scripts/01_basics/01_ur5e.py
```


## Installation :cd:

First install [airo-blender](https://github.com/airo-ugent/airo-blender) and then the [urdf-workshop](https://github.com/Victorlouisdg/urdf-workshop) and [linen](https://github.com/Victorlouisdg/linen).
Then clone the repo and run:
```bash
git clone git@github.com:Victorlouisdg/robotics-renders.git
cd robotics-renders
pip install -e robotics-renders
```