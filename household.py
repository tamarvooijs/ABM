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
        number_of_persons = 1
    elif type == "Couple" or "Retired":
        number_of_persons = 2
    elif type == "Family":
        number_of_persons = 4
    else:
        print("error")
        return 1

    waste = 40 - 0.04 * x - math.exp(-0.01 * x) * math.sin(0.3 * x) * number_of_persons

    return waste


class Household(Agent):
    "Households that recycle a certain amount of plastic each year"

    def __init__(self, unique_id, model, type, access, municipality):
        super().__init__(unique_id, model)
        self.agent = "Household"
        self.type = type
        self.access = access
        self.municipality = municipality
        self.produced_volume_base = waste(self.model.schedule.time, self.type)
        self.produced_volume_updated = 0
        Household.initial_knowledge(self)
        Household.initial_perception(self)

    def step(self):

        self.produced_volume_updated = waste(self.model.schedule.time, self.type) * self.knowledge * self.perception

        print("Hi, I am household " + str(self.unique_id) + " and I produced this amount of waste:",
              str(round(self.produced_volume_updated, 2)) + " and knowledge", self.knowledge )
        return 0

    def initial_perception(self):
        perception_range = (0, 0)

        if self.type == "Individual":
            perception_range = (0.4, 0.6)
        if self.type == "Retired":
            perception_range = (0.2, 0.5)
        if self.type == "Couple":
            perception_range = (0.5, 0.7)
        if self.type == "Family":
            perception_range = (0.3, 0.6)

        self.perception = random.uniform(perception_range[0], perception_range[1])

    def initial_knowledge(self):
        knowledge_range = (0, 0)

        if self.type == "Individual":
            knowledge_range = (0.4, 0.6)
        if self.type == "Retired":
            knowledge_range = (0.2, 0.5)
        if self.type == "Couple":
            knowledge_range = (0.5, 0.7)
        if self.type == "Family":
            knowledge_range = (0.3, 0.6)

        self.knowledge = random.uniform(knowledge_range[0], knowledge_range[1])




