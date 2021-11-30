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


def waste(x, type):
    if type == "Individual":
        waste = 40 - 0.04 * x - math.exp(-0.01 * x) * math.sin(0.3 * x)

    elif type == "Couple" or "Retired":
        waste = (40 - 0.04 * x - math.exp(-0.01 * x) * math.sin(0.3 * x)) * 2

    elif type == "Family":
        waste = 40 - 0.04 * x - math.exp(-0.01 * x) * math.sin(0.3 * x) * 4

    else:
        print("error")
        return 1

    return waste


class Household(Agent):
    "Households that recycle a certain amount of plastic each year"

    def __init__(self, unique_id, model, type, access, municipality, produced_volume, knowledge, perception):
        super().__init__(unique_id, model)
        self.agent = "Household"
        self.type = type
        self.access = access
        self.municipality = municipality
        self.produced_volume = produced_volume
        self.knowledge = knowledge
        self.perception = perception

    def step(self):
        self.produced_volume = waste(self.model.schedule.time, self.type)

        print("Hi, I am household " + str(self.unique_id) + " and I produced this amount of waste:",
              round(self.produced_volume, 2))
        return 0
