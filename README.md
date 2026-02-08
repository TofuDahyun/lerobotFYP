# This is my guide NOW

***

## On Launch
```
conda activate lerobot4
cd C:\School Stuff\Year 4 Sem 2\FYP\lerobotFYP
```

***

## Check for GPU availability
```
nvidia-smi
```

***

## Extra pip stuff to do for proper cuda usage and huggingface upload during training
```
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install hf_xet
pip install torchcodec, so that dont need pyav, but this caused problems
```

***

### Installation of torchcodec caused problems, claimed to have fasting video decoding but had python.exe path issue
```
pip install torchcodec
```
Solution is to fall back to pyav by uninstalling it and ignoring errors
```
pip uninstall torchcodec
```

***

### Tried cu116 for cuda 11.6 but torch version is not compatible
Found existing installation: torch 2.7.1
Uninstalling torch-2.7.1:
  Successfully uninstalled torch-2.7.1
Found existing installation: torchvision 0.22.1
Uninstalling torchvision-0.22.1:
  Successfully uninstalled torchvision-0.22.1
WARNING: Skipping torchaudio as it is not installed.

accelerate 1.12.0 requires torch>=2.0.0, but you have torch 1.13.1+cu116 which is incompatible.
lerobot 0.4.4 requires torch<2.8.0,>=2.2.1, but you have torch 1.13.1+cu116 which is incompatible.
lerobot 0.4.4 requires torchvision<0.23.0,>=0.21.0, but you have torchvision 0.14.1+cu116 which is incompatible.

solution: try cu118, though might not be compatible with 11.6

according to nvidia-smi, cuda is 11.6

***

## To open visual studio code
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

**Records 1 episode for the picking up of toy car but does not upload it to hub**
```
lerobot-record --robot.type=so101_follower --robot.port=COM4 --robot.id=follower_arm --robot.cameras="{ front: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}}" --teleop.type=so101_leader --teleop.port=COM3 --teleop.id=leader_arm --dataset.repo_id=TofuDahyun/toy_car_test --dataset.num_episodes=1 --dataset.episode_time_s=60 --dataset.single_task="Pick up the toy car and place it in the box" --dataset.push_to_hub=false
```

**Replays the recorded episode 0 from test3 folder**
```
lerobot-replay --robot.type=so101_follower --robot.port=COM4 --robot.id=follower_arm --dataset.repo_id=TofuDahyun/toy_car_test3 --dataset.episode=0
```

**Replays the recorded episode 6 from train_010226 folder**
```
lerobot-replay --robot.type=so101_follower --robot.port=COM4 --robot.id=follower_arm --dataset.repo_id=TofuDahyun/toy_car_train_010226 --dataset.episode=6
```

**Actual recording command ran to record 10 episodes for the picking up of toy car**
```
lerobot-record --robot.type=so101_follower --robot.port=COM4 --robot.id=follower_arm --robot.cameras="{ front: {type: opencv, index_or_path: 1, width: 640, height: 480, fps: 30}}" --teleop.type=so101_leader --teleop.port=COM3 --teleop.id=leader_arm --dataset.repo_id=TofuDahyun/toy_car_train_010226 --dataset.num_episodes=10 --dataset.episode_time_s=60 --dataset.single_task="Pick up the toy car and place it in the box"
```

box is 9.5cm horizontally away from the table, 6cm vertically
robot is 15cm vertically away from table and in the center of no line and got line

**Trains a model based on recording data and uploads the policy to huggingface and makes it private**
```
lerobot-train --dataset.repo_id=TofuDahyun/toy_car_train_010226 --policy.path=lerobot/smolvla_base --batch_size=8 --steps=5000 --output_dir=outputs/train/policy_output_toy_car_train_010226 --job_name=policy_output_toy_car_train_010226 --policy.device=cuda --wandb.enable=true --policy.repo_id=TofuDahyun/policy_output_toy_car_train_010226 --policy.private=true
```

**Trains a model based on recording data and uploads the policy to huggingface and makes it private, and renames the camera1 from smolvla_base to match my dataset camera name and declare 2 empty cameras and declares batch_size and steps**
```
lerobot-train --dataset.repo_id=TofuDahyun/toy_car_train_010226 --policy.path=lerobot/smolvla_base --batch_size=8 --steps=5000 --output_dir=outputs/train/policy_output_toy_car_train_010226 --job_name=policy_output_toy_car_train_010226 --policy.device=cuda --wandb.enable=true --policy.repo_id=TofuDahyun/policy_output_toy_car_train_010226 --rename_map="{"observation.images.front": "observation.images.camera1"}" --policy.empty_cameras=2 --policy.private=true
```

**Trains a model based on recording data and uploads the policy to huggingface and makes it private, and renames the camera1 from smolvla_base to match my dataset camera name and declare 2 empty cameras and declares batch_size and steps and reduced the amount of memory that the previous commands took. This worked**

In the future remmeber to run Anaconda Prompt with `Administrator mode`

```
lerobot-train --dataset.repo_id=TofuDahyun/toy_car_train_010226 --policy.path=lerobot/smolvla_base --batch_size=2 --steps=5000 --output_dir=outputs/train/policy_output_toy_car_train_010226 --job_name=policy_output_toy_car_train_010226 --policy.device=cuda --wandb.enable=true --policy.repo_id=TofuDahyun/policy_output_toy_car_train_010226 --rename_map="{"observation.images.front": "observation.images.camera1"}" --policy.empty_cameras=2 --num_workers=0 --policy.use_amp=true --policy.resize_imgs_with_padding="[256,256]" --policy.private=true
```

**Trains without taking reference to smolvla_base, not really optimal**
```
lerobot-train --dataset.repo_id=TofuDahyun/toy_car_train_010226 --policy.type=act --batch_size=8 --steps=5000 --output_dir=outputs/train/act_policy_output_toy_car_train_010226 --job_name=act_policy_output_toy_car_train_010226 --policy.device=cuda --wandb.enable=true --policy.repo_id=TofuDahyun/act_policy_output_toy_car_train_010226 --policy.private=true
```

**To run the testing script with camera, made by my own**
```
python -m lerobot_teleoperate_testing --robot.type=so101_follower --robot.port=COM4 --robot.id=follower_arm --teleop.type=so101_leader --teleop.port=COM3 --teleop.id=leader_arm
```
***