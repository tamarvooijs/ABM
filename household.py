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

    def __init__(self, unique_id, model, type, access, municipality, produced_volume_base):
        super().__init__(unique_id, model)
        self.agent = "Household"
        self.type = type
        self.access = access
        self.municipality = municipality
        self.produced_volume_base = produced_volume_base
        self.produced_volume_updated = 0
        Household.calculate_knowledge(self)
        Household.calculate_perception(self)

    def step(self):
        self.produced_volume_base = waste(self.model.schedule.time, self.type)
        self.produced_volume_updated = self.produced_volume_base * self.knowledge * self.perception

        print("Hi, I am household " + str(self.unique_id) + " and I produced this amount of waste:",
              str(round(self.produced_volume_updated, 2)) + "and knowledge", self.knowledge )
        return 0

    def calculate_perception(self):
        if self.type == "Individual":
            self.perception = random.uniform(0.4, 0.6)
        if self.type == "Retired":
            self.perception = random.uniform(0.2, 0.5)
        if self.type == "Couple":
            self.perception = random.uniform(0.5, 0.7)
        if self.type == "Family":
            self.perception = random.uniform(0.3, 0.6)


    def calculate_knowledge(self):
        if self.type == "Individual":
            self.knowledge = random.uniform(0.4, 0.6)
        if self.type == "Retired":
            self.knowledge = random.uniform(0.2, 0.5)
        if self.type == "Couple":
            self.knowledge = random.uniform(0.5, 0.7)
        if self.type == "Family":
            self.knowledge = random.uniform(0.3, 0.6)






