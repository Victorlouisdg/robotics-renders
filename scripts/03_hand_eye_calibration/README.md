# Hand-eye calibration

### 01 - [ZED2i](./01_zed2i.py)

![ZED2i](https://i.imgur.com/nA7acw2.png)

Simply loads a ZED2i camera into Blender.

### 02 - [Hand-to-eye calibration](./hand_to_eye.py)

![Hand-to_eye](https://i.imgur.com/f0BQUiS.png)

Shows the transform that is searched in hand-to-eye calibration.

### 03 - Charuco board creation
Script to load an image of a charuco board into Blender.

### 04 - [Charuco board detection](./04_charuco_detection.py)
![Charuco detection](https://i.imgur.com/BvIhjoe.gif)

Shows that a single camera can detect the pose of a charuco board relative to itself.

### 05 - [Missing transform](./05_missing_transform.py)
![Missing transform](https://i.imgur.com/y2x5oGs.png)

Shows the missing, but constant, transform between the end-effector frame and the board.