# This is my guide NOW

***

## File Directory Setup
```
conda activate lerobot4
cd ..
cd ..
cd C:\School Stuff\Year 4 Sem 2\FYP\lerobotFYP
```

To open visual studio code, 
```
code
```

***
## Some Useful Commands 
**Teleoperation**
```
lerobot-teleoperate --robot.type=so101_follower --robot.port=COM4 --robot.id=follower_arm --teleop.type=so101_leader --teleop.port=COM3 --teleop.id=leader_arm
```

**Teleoperation with camera display but 1920x1080 seems to not work**
```
lerobot-teleoperate --robot.type=so101_follower --robot.port=COM4 --robot.id=follower_arm --robot.cameras="{ front: {type: opencv, index_or_path: 1, width: 1920, height: 1080, fps: 30}}" --teleop.type=so101_leader --teleop.port=COM3 --teleop.id=leader_arm --display_data=true
```

**Teleoperation with camera display but 640x480 resolution**
```
lerobot-teleoperate --robot.type=so101_follower --robot.port=COM4 --robot.id=follower_arm --robot.cameras="{ front: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}}" --teleop.type=so101_leader --teleop.port=COM3 --teleop.id=leader_arm --display_data=true
```

**Records 1 episode and saves it in test_dataset folder with 5s recording time with command of "Pick up the object"**
```
lerobot-record --robot.type=so101_follower --robot.port=COM4 --robot.id=follower_arm --robot.cameras="{ front: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}}" --teleop.type=so101_leader --teleop.port=COM3 --teleop.id=leader_arm --dataset.repo_id=TofuDahyun/test_dataset --dataset.num_episodes=1 --dataset.episode_time_s=5 --dataset.single_task="Pick up the object"
```

**Records 1 episode and saves it in test_dataset folder with 5s recording time with command of "Pick up the object" and creates new episode indexes each time**
```
lerobot-record --robot.type=so101_follower --robot.port=COM4 --robot.id=follower_arm --robot.cameras="{ front: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}}" --teleop.type=so101_leader --teleop.port=COM3 --teleop.id=leader_arm --dataset.repo_id=TofuDahyun/test_dataset --dataset.num_episodes=1 --dataset.episode_time_s=5 --dataset.single_task="Pick up the object" --resume=True
```

**Records 1 episode and saves it in test6 folder with 10s recording time with command of "Pick up the cube" but don't upload data to huggingface website**
```
lerobot-record --robot.type=so101_follower --robot.port=COM4 --robot.id=follower_arm --robot.cameras="{ front: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}}" --teleop.type=so101_leader --teleop.port=COM3 --teleop.id=leader_arm --dataset.repo_id=TofuDahyun/test6 --dataset.num_episodes=1 --dataset.episode_time_s=10 --dataset.single_task="Pick up the cube" --dataset.push_to_hub=false
```

Video is saved to local directory of: `C:\Users\User\.cache\huggingface\lerobot\TofuDahyun\test6\videos\observation.images.front\chunk-000`


**To run the testing script with camera, made by my own**
```
python -m lerobot_teleoperate_testing --robot.type=so101_follower --robot.port=COM4 --robot.id=follower_arm --teleop.type=so101_leader --teleop.port=COM3 --teleop.id=leader_arm
```
***