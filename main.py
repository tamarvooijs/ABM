#library imports:
#mesa
from mesa import Agent, Model
from mesa.datacollection import DataCollector
#load all available schedulers
import mesa.time as time

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

class Household(Agent):
    "Households that recylcle a certain amount of plastic each year"

    def __init__(self, unique_id, model, type, access, municipality, produced_volume, knowledge, perception):
        super().__init__(unique_id, model)
        self.type = type
        self.access = access
        self.municipality = municipality
        self.produced_volume = produced_volume
        self.knowledge = knowledge
        self.perception = perception

    def step(self):
        self.produced_volume += 40/12
        print("Hi, I am household " + str(self.unique_id) + " and I produced this amount of waste:",
              round(self.produced_volume, 2))
        return 0


class Municipality(Agent):
    def __init__(self, unique_id, model, number_of_households, budget, contract, infrastructure):
        super().__init__(unique_id, model)
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
        self.technology = technology
        self.contract = contract
        self.percentage_filtered = percentage_filtered

    def step(self):
        print("Hi, I am company " + str(self.unique_id) + ".")
        return 0

class RecyclingModel(Model):
    "Model in which agents recycle"

    def __init__(self, No_HH, No_Mun, No_Comp):
        self.schedule = time.RandomActivation(self)

        for i in range(No_HH):
            household = Household(i, self,"single", "yes", "Rotterdam", produced_volume=2, knowledge=0.5, perception=0.5)
            self.schedule.add(household)

        for i in range(No_Mun):
            municipality = Municipality(i+No_HH, self, 1, 100, 1, 3)
            self.schedule.add(municipality)

        for i in range(No_Comp):
            company = RecyclingCompany(i+No_Mun+No_HH, self, "technology 1", "contract 2", 50)
            self.schedule.add(company)

    def step(self):
        self.schedule.step()


model = RecyclingModel(2, 1, 1)

number_of_steps = 3
for i in range(number_of_steps):
    print("Step:", i)
    model.step()






