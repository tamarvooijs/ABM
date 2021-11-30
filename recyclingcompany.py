#library imports:
#mesa
from mesa import Agent
from mesa.datacollection import DataCollector
#load all available schedulers
import mesa.time as time
import math
import random
# matplot lib for plotting, numpy for all sorts of useful math
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#basic python statistics
import statistics as stat

#import pandas
import pandas as pd

# Required libraries for animation
from matplotlib.animation import FuncAnimation
from matplotlib import animation, rc, collections
from IPython.display import HTML


class RecyclingCompany(Agent):
    def __init__(self, unique_id, model, technology, contract, percentage_filtered):
        super().__init__(unique_id, model)
        self.agent = "Company"
        self.technology = technology
        self.contract = contract
        self.percentage_filtered = percentage_filtered
        self.collected = 0

    def step(self):
        print("Hi, I am company " + str(self.unique_id) + ".")
        return 0
