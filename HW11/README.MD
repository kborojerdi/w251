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

## Key Features

* LivePreview - Make changes, See changes
  - Instantly see what your Markdown documents look like in HTML as you create them.
* Sync Scrolling
  - While you type, Li
  
## Reinforcement Learning | Brief Intro
Reinforcement learning is an interesting area of Machine learning. The rough Idea is that you have an agent and an environment. The agent takes actions and environment gives reward based on those actions, The goal is to teach the agent optimal behaviour in order to maximize the reward received by the environment.

Reinforcement Learning Diagram
For example, have a look at the diagram. This maze represents our environment. Our purpose would be to teach the agent an optimal policy so that it can solve this maze. The maze will provide a reward to the agent based on the goodness of each action it takes. Also, each action taken by agent leads it to the new state in the environment.

## About Lunar-Lander
As you can see in the picture below, there is one space-ship. The task is to land the space-ship between the flags smoothly. The ship has 3 throttles in it. One throttle points downward and other 2 points in the left and right direction. With the help of these, you have to control the Ship.

There are 2 different Lunar Lander Environment in OpenAIGym. One has discrete action space and other has continuous action space. Let’s solve both one by one. Please read this doc to know how to use Gym environments.

## LunarLanderContinuous-v2 (Continuous)
Landing pad is always at coordinates (0,0). Coordinates are the first two numbers in state vector. Reward for moving from the top of the screen to landing pad and zero speed is about 100..140 points. If lander moves away from landing pad it loses reward back. Episode finishes if the lander crashes or comes to rest, receiving additional -100 or +100 points. Each leg ground contact is +10. Firing main engine is -0.3 points each frame. Solved is 200 points. Landing outside landing pad is possible. Fuel is infinite, so an agent can learn to fly and then land on its first attempt. Action is two real values vector from -1 to +1. First controls main engine, -1..0 off, 0..+1 throttle from 50% to 100% power. Engine can’t work with less than 50% power. Second value -1.0..-0.5 fire left engine, +0.5..+1.0 fire right engine, -0.5..0.5 off.
  
  
## Training Visualization
* Following gifs shows the learning progress. In starting the agent is behaving very poorly. It does not know how to control the throttles.

<div align="center">
<img src="Lunar_lander_run3.gif">
<p>Successfull episode after 3rd training conifgurartion.</p>
</div>

Following is the plot showing rewards per episode. I was able to solve the task in around 350 episodes.

Plot of the training vs 

Reward vs Episode Plot (continuous)

