<h3>
  Katayoun Borojerdi
<h3>

<h1 align="center">
  Homework 11 - OpenAI
  <img src="https://gym.openai.com/assets/dist/home/header/home-icon-54c30e2345.svg" alt="Gym" width="50">
  Gym
</h1>

<h4 align="center">
  Training a Lunar Lander to properly land using a Jetson TX2.
</h4>

## Problem Description
There are two python scripts used to run the Lunar Lander Program.
```lunar_lander.py```
containes the OpenAI Gym Lunar Lander enviornment and the configuration of the keras Nueral Network model.

```run_lunar_lander.py```
calls both the the Lunar Lander environment and NN model, and contians the Reinforcement learning algorythm.

## DefaultcReinforcement Learning 
The default RL algorithm  seems to be a monte carlo method. Actions are randomly generated, and we use them to get coresponding states and rewards from the enviornment. We use that information to train our nuearl network. Once the netwrok is trained again we generate random actions, but now we feed those into our NN and estimate the reward. We choose that action withth highest reward and progress through the episode. periodiclly we re-trin the model, and over time the model improves and eventually becomes proficient at predicting r based on a given current state and action.

The problem with this model is that even after it is trained sufficently, it still relies on you feeding in random actions to find the maximum reward. it would be more efficient if our network could output the action. Also we are not including discount reward factor in this model. So there is no weight given to future reward. This may cause the model to spedn more time hoevering and learn to land and complete the espisode.

## About Lunar-Lander
The task is to land the space-ship between the flags smoothly. The ship has 3 throttles in it. One throttle points downward and other 2 points in the left and right direction. With the help of these, you have to control the Ship.

There are 2 different Lunar Lander Environment in OpenAIGym. One has discrete action space and other has continuous action space. For this problem we are useing the contiuous action sapce.

## LunarLanderContinuous-v2 (Continuous)
Landing pad is always at coordinates (0,0). Action is two real values vector from -1 to +1. First controls main engine, -1..0 off, 0..+1 throttle from 50% to 100% power. Engine can’t work with less than 50% power. Second value -1.0..-0.5 fire left engine, +0.5..+1.0 fire right engine, -0.5..0.5 off.

## First Model Update
The original RL algorithm generated actions between -1 and 1. However because all actions between -.5 and .5 mean the engins are off. I felt this would bias the actions and waste processing time. So I changed to generate numbers from .4 to 1 for the main enginer and +/- that same range for the side engines.

I also update the script to run by episode instead of just number of steps, so that I could better understand the total reward per episode. I added a max memory size for the input list to make sure I did not run out of memory. 

```
from collections import deque
self.memory = deque(maxlen=2000)
```

This also acts as a way to remove old training steps that are not as good for newer ones based on more accurate NN model. With this I was able to train the model for more total steps. I kept the NN the same for comparison to the basleine RL algorythm and ran it for about 3 times the total number of steps.

## Training Visualization
Here are my 2 best episodes out of 10 test episodes I ran once the training was complete.

<div align="center">
<img src="Lunar_lander_run3.gif">
<p>Successfull episode after 3rd training conifgurartion.</p>
</div>

<div align="center">
<img src="Lunar_lander_run3.gif">
<p>Successfull episode after 3rd training conifgurartion.</p>
</div>

Following is the plot showing rewards per episode. I was able to solve the task in around 350 episodes.

Plot of the training vs 

Reward vs Episode Plot (continuous)

