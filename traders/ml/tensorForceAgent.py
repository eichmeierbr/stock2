from tensorforce import Agent
from Classifier import *

import numpy as np


class TensorForceClass(Classifier):

    def __init__(self, ticker, inputSize = 10, load=None):
        self.type = 'DQN RL'
        self.inputSize = inputSize
        self.ticker = ticker
        self.days = inputSize
        self.binary= True
        self.agent = self.createRLagent()
        self.binary = False
        self.lastReturn = 0
        self.canAct = True
        self.needsTrain = True


    def createRLagent(self, load=None):
        states_dict = {'type': 'float', 'shape': self.inputSize}

        if self.binary: outType = 'bool'
        else: outType = 'float'

        actions_dict = {'type': 'bool', 'shape': 1}

        agent = Agent.create(
            agent='ppo',
            states = states_dict,
            actions = actions_dict,
            max_episode_timesteps=1,
            batch_size=10,
            exploration = 0.05,
            memory=10000)

        if not load ==None:
            agent.restore(directory=load)

        return agent


    def fit(self, input, labels):
        if not self.needsTrain: return
        totalReward = 1
        for data, label in zip(input,labels):
            action = self.agent.act(states=data)
            reward = action[0]*1*label
            self.agent.observe(reward=reward,terminal=1)
            totalReward *= (1 + reward/100)
        # print(totalReward)
        self.needsTrain = False
        return


    def predict(self, inputArray):
        actions = []

        for array in inputArray:
            if not self.canAct: 
                self.agent.observe(reward=array[-1],terminal=1)
            actions.append(self.agent.act(states=array)[0]*1)
            self.canAct = False

        return actions