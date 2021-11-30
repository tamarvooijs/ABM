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

# Required libraries for animation
from matplotlib.animation import FuncAnimation
from matplotlib import animation, rc, collections
from IPython.display import HTML

from household import Household, waste
from municipality import Municipality
from recyclingcompany import RecyclingCompany



class RecyclingModel(Model):
    "Model in which agents recycle"

    def __init__(self, No_HH, No_Mun, No_Comp):
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
