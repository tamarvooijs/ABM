#library imports:
#mesa
from collections import OrderedDict

from municipality import Municipality
from household import Household
from recyclingcompany import RecyclingCompany
from mesa import Agent, Model
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

#import visualisation mesa
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

#import space mesa
from mesa.space import MultiGrid

# Required libraries for animation
from matplotlib.animation import FuncAnimation
from matplotlib import animation, rc, collections
from IPython.display import HTML
# class RandomActivationPerType(time.BaseScheduler):
#     """ A scheduler which activates each agent once per step, in random order,
#     with the order reshuffled every step.
#
#     This is equivalent to the NetLogo 'ask agents...' and is generally the
#     default behavior for an ABM.
#
#     Assumes that all agents have a step(model) method.
#
#     """
#     def __init__(self, modelx, sequence):
#         self.model = modelx
#         self.sequence = sequence
#         self._agents = OrderedDict()
#         self.steps = 0
#
#     def step(self) -> None:
#         """ Executes the step of all agents, one at a time, in
#         random order.
#
#         """
#         for i in self.sequence:
#
#             for agent in self.agent_buffer(shuffled=True):
#                 if agent.agent == i:
#                     agent.step()
#                 self.steps += 1
#                 self.time += 1

class RandomActivationPerType(time.BaseScheduler):
    """ A scheduler which activates each agent once per step, in random order,
    with the order reshuffled every step.

    This is equivalent to the NetLogo 'ask agents...' and is generally the
    default behavior for an ABM.

    Assumes that all agents have a step(model) method.

    """

    def step(self) -> None:
        """ Executes the step of all agents, one at a time, in
        random order.

        """
        sequence = ["Municipality", "Household", "Company"]
        for agent in self.agent_buffer(shuffled=True):
            if agent.agent == "Municipality":
                agent.step()
        for agent in self.agent_buffer(shuffled=True):
            if agent.agent == "Household":
                agent.step()
        for agent in self.agent_buffer(shuffled=True):
            if agent.agent == "Company":
                agent.step()
        self.steps += 1
        self.time += 1


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



class RecyclingModel(Model):
    "Model in which agents recycle"

    def __init__(self, No_HH, No_Mun, No_Comp):
        self.height = 10
        self.width = 10
        self.grid = MultiGrid(self.width, self.height, True)
        sequence = ["Municipality", "Household", "Company"]
        self.schedule = RandomActivationPerType(self)


        types_of_households = ["Individual", "Couple", "Family", "Retired"]

        for i in range(No_HH):
            type = random.choice(types_of_households)
            if type == "Individual":
                household = Household(i, self, "Individual", "yes", "Rotterdam", produced_volume=2, knowledge=0.5, perception=0.5)
            elif type =="Couple":
                household = Household(i, self, "Couple", "yes", "Rotterdam", produced_volume=2, knowledge=0.5, perception=0.5)
            elif type == "Family":
                household = Household(i, self, "Family", "yes", "Rotterdam", produced_volume=2, knowledge=0.5, perception=0.5)
            elif type == "Retired":
                household = Household(i, self, "Family", "yes", "Rotterdam", produced_volume=2, knowledge=0.5, perception=0.5)

            self.schedule.add(household)

        for i in range(No_Mun):
            municipality = Municipality(i+No_HH, self, 1, 100, 1, 3)
            self.schedule.add(municipality)

            # Create municipalities on a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(municipality, (x, y))

        for i in range(No_Comp):
            company = RecyclingCompany(i+No_Mun+No_HH, self, "technology 1", "contract 2", 50)
            self.schedule.add(company)

    def step(self):
        self.schedule.step()
        total_waste = 0
        for i in self.schedule.agents:
            if i.agent == "Household":
                total_waste += i.produced_volume
        for i in self.schedule.agents:
            # This only works if there is one recyclingcompany
            # TO DO: aggregate to more companies
            if i.agent == "Company":
                i.collected += total_waste
                waste_collected = i.collected
        print("Total waste this round equals ", total_waste)
        print("Total collected", waste_collected)


model = RecyclingModel(2, 1, 1)

number_of_steps = 3
for i in range(number_of_steps):
   print("Step:", i)
   model.step()





