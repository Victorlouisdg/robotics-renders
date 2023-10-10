Basic scripts :beginner:
=============
Some scripts to get you started with this repo.

### 01 - [UR5e](./01_ur5e.py)

![UR5e](https://i.imgur.com/mNYP60Y.png)

Simply loads a UR5e urdf into Blender of which you can pose the joints by clicking the arrows and pressing `R` to rotate.

### 02 - [UR5e with Robotiq 2F-85](./02_ur5e_robotiq.py)

![UR5e with Robotiq](https://i.imgur.com/htUjVdt.png)

Shows how you can parent a gripper to the tool link of the UR5e.

### 03 - [UR5e animated](./03_ur5e_animated.py)

![UR5e animted](https://i.imgur.com/Vkp5YhO.gif)

To create the animation, render it as a sequence of png files.
Convert the png files to a video using ffmpeg:
```
ffmpeg -framerate 24 -i %04d.png output.mp4
```
To turn that video into a gif, I followed this [guide](http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html#usage).

### 04 - [Reference frames](./04_reference_frames.py)

TODO: finish

### 05 [UR5e and shelves](./05_ur5e_and_shelves.py)

![UR5e and shelves](https://i.imgur.com/LUqLoPv.png)
