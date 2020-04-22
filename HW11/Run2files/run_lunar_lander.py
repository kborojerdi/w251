import sys, math
import numpy as np
import random

import Box2D
from Box2D.b2 import (edgeShape, circleShape, fixtureDef, polygonShape, revoluteJointDef, contactListener)

#Created by https://github.com/shivaverma

import gym
from gym import spaces
from gym.utils import seeding
import skvideo.io
from keras.models import Sequential
from keras.layers import Dense
from lunar_lander import *

from collections import deque

#import pickle

# Initialize training data
# X_train, y_train = [],[]
frames = []

X_train = deque(maxlen=10000)
y_train = deque(maxlen=10000)


if __name__=="__main__":
    # Initialize lunar lander environment
    env = LunarLanderContinuous()
    prev_s = env.reset()
    #total_reward = 0
    steps = 0
    total_steps = 0
    #a = np.array([0.0,0.0])
    a = env.action_space.sample()
    modelTrained = False
    model = nnmodel(10)
    tr = 0
#    prev_r = 0
    #track total number of completed episodes
    episode = 0
#    training_thr = 3000
    training_episodes = 20
#    total_itrs = 50000
    max_steps = 500
    # Run total episodes instead of iterations
    total_episodes = 300
    #successful_steps = []
    successful_landings = []

    reward_list = []


#    while steps <= total_itrs:
    while episode < total_episodes:
        new_s, r, done, info = env.step(a)
        
        X_train.append(list(prev_s)+list(a))
        y_train.append(r)

        #ran a new env, iterate step
        steps += 1

        # This 'if' statement determines how often your model is re-trained

#        if steps > training_thr and steps %1000 ==0:
        if episode > training_episodes and episode %10 == 0 and steps == 1:
            # re-train a model
            #print("training model model")
            print("training the model")
            modelTrained = True
            model.fit(np.array(X_train),np.array(y_train).reshape(len(y_train),1), epochs = 10, batch_size=20)

        if modelTrained:
            maxr = -1000
            maxa = None
            for i in range(100):
#                a1 = np.random.randint(-1000,1000)/1000
#                a2 = np.random.randint(-1000,1000)/1000
                a1 = np.random.randint(400,1000)/1000
                a2 = (np.random.randint(400,1000)/1000) * random.randrange(-1, 2, 2)
                testa = [a1,a2]
                r_pred = model.predict(np.array(list(new_s)+list(testa)).reshape(1,len(list(new_s)+list(testa))))
                if r_pred > maxr:
                    maxr = r_pred
                    maxa = testa
            a = np.array(maxa)

        else:
#            a = np.array([np.random.randint(-1000,1000)/1000,\
#                 np.random.randint(-1000,1000)/1000])
            a = np.array([np.random.randint(400,1000)/1000,\
                  ((np.random.randint(400,1000)/1000) * random.randrange(-1, 2, 2))])

#        if steps %100 == 0:
#            print("At step ", steps)
#            print("reward: ", r)
#            print("total rewards ", tr)
        
        prev_s = new_s
#        prev_r = r

        tr = tr + r #move this to better track successes

#        if (steps >= training_thr and tr < -500) or done:
        if steps >= max_steps or tr < -500 or done:
            #print(prev_s, tr) #add tr to print
            if done and tr >= 200: # was prev_r <= 200
                #successful_steps.append(steps) 
                #print("Successful Landing!!! ",steps)
                #print("Total successes are: ", len(successful_steps))
                successful_landings.append(tr) 
                print("Successful Landing!!! ", episode, steps, tr)
                print("Total successes are: ", len(successful_landings))
            
            else:
                print("Crashed!!! ", episode, steps, tr)
                print("Total successes are: ", len(successful_landings))

            reward_list.append(tr)
            #reset all variables and the enviornment
            prev_s = env.reset()
            tr = 0
            steps = 0
            a = env.action_space.sample()
            episode += 1

    with open('/tmp/videos/LL_reward_list_2_1.txt', 'w') as file:
        for reward in reward_list:
            file.write("%i\n" % reward)

#        tr = tr + r

#        steps += 1
#        total_steps += 1
#        frame = env.render(mode='rgb_array')
#        frames.append(frame)
#        if steps >= training_thr and steps %1000 == 0:
#            fname = "/tmp/videos/frame"+str(steps)+".mp4"
#            skvideo.io.vwrite(fname, np.array(frames))
#            del frames
#            frames = []


if __name__=="__main__":

    # Initialize lunar lander environment
    env = LunarLanderContinuous()
    prev_s = env.reset()
    #total_reward = 0
    steps = 0
    total_steps = 0
    #a = np.array([0.0,0.0])
    a = env.action_space.sample()
    modelTrained = True
    tr = 0
#    prev_r = 0
    #track total number of completed episodes
    episode = 0
#    training_thr = 3000
#    training_episodes = 30
#    total_itrs = 50000
#    max_steps = 500
    # Run total episodes instead of iterations
    total_episodes = 10
    #successful_steps = []
    successful_landings = []

    reward_list = []

    while episode < total_episodes:
        new_s, r, done, info = env.step(a)
        #X_train.append(list(prev_s)+list(a))
        #y_train.append(r)

        #ran a new env, iterate step
        steps += 1

        if modelTrained:
            maxr = -1000
            maxa = None
            for i in range(50):
#                a1 = np.random.randint(-1000,1000)/1000
#                a2 = np.random.randint(-1000,1000)/1000
                a1 = np.random.randint(400,1000)/1000
                a2 = (np.random.randint(400,1000)/1000) * random.randrange(-1, 2, 2)
                testa = [a1,a2]
                r_pred = model.predict(np.array(list(new_s)+list(testa)).reshape(1,len(list(new_s)+list(testa))))
                if r_pred > maxr:
                    maxr = r_pred
                    maxa = testa
            a = np.array(maxa)

        else:
#            a = np.array([np.random.randint(-1000,1000)/1000,\
#                 np.random.randint(-1000,1000)/1000])
            a = np.array([np.random.randint(400,1000)/1000,\
                  ((np.random.randint(400,1000)/1000) * random.randrange(-1, 2, 2))])

#        if steps %100 == 0:
#            print("At step ", steps)
#            print("reward: ", r)
#            print("total rewards ", tr)
        
        prev_s = new_s
#        prev_r = r

        tr = tr + r #move this to better track successes

#        if (steps >= training_thr and tr < -500) or done:
        if steps >= max_steps or tr < -500 or done:
            #print(prev_s, tr) #add tr to print
            frame = env.render(mode='rgb_array')
            frames.append(frame)
            print("is this running")
            fname = "/tmp/videos/episode_2_"+str(episode)+".mp4"
            skvideo.io.vwrite(fname, np.array(frames))
            del frames
            frames = []

            if done and tr >= 200: # was prev_r <= 200
                #successful_steps.append(steps) 
                #print("Successful Landing!!! ",steps)
                #print("Total successes are: ", len(successful_steps))
                successful_landings.append(tr) 
                print("Successful Landing!!! ", episode, steps, tr)
                print("Total successes are: ", len(successful_landings))
            
            else:
                print("Crashed!!! ", episode, steps, tr)
                print("Total successes are: ", len(successful_landings))

            reward_list.append(tr)
            #reset all variables and the enviornment
            prev_s = env.reset()
            tr = 0
            steps = 0
            a = env.action_space.sample()
            episode += 1

 #       env.render(mode='human')
        frame = env.render(mode='rgb_array')
        frames.append(frame)
#        if done:
#            print("is this running")
#            fname = "/tmp/videos/episode_2_"+str(episode)+".mp4"
#            skvideo.io.vwrite(fname, np.array(frames))
#            del frames
#            frames = []

    with open('/tmp/videos/LL_reward_list_2_2.txt', 'w') as file:
        for reward in reward_list:
            file.write("%i\n" % reward)

