#library imports:
#mesa
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
    "Households that recylcle a certain amount of plastic each year"

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
        self.produced_volume = waste(model.schedule.time, self.type)

        print("Hi, I am household " + str(self.unique_id) + " and I produced this amount of waste:",
              round(self.produced_volume, 2))
        return 0


class Municipality(Agent):
    def __init__(self, unique_id, model, number_of_households, budget, contract, infrastructure):
        super().__init__(unique_id, model)
        self.agent = "Municipality"
        self.number_of_households = number_of_households
        self.budget = budget
        self.contract = contract
        self.infrastructure = infrastructure

    def step(self):
        print("Hi, I am municipality " + str(self.unique_id) + ".")
        return 0

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

class RecyclingModel(Model):
    "Model in which agents recycle"

    def __init__(self, No_HH, No_Mun, No_Comp, width, height):
        self.grid = MultiGrid(width, height, True)
        self.schedule = time.RandomActivation(self)

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


#model = RecyclingModel(2, 1, 1)

#number_of_steps = 3
#for i in range(number_of_steps):
 #   print("Step:", i)
 #   model.step()

def agent_portrayal(agent: Municipality):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 2}
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(RecyclingModel,
                       [grid],
                       "Recycling Model",
                       {"No_HH": 5, "No_Mun": 1, "No_Comp": 2, "width": 10, "height": 10})
server.port = 8521  # The default
server.launch()



