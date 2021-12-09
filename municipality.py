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


class Municipality(Agent):
    def __init__(self, unique_id, model, number_of_households, budget, contract, infrastructure):
        super().__init__(unique_id, model)
        self.agent = "Municipality"
        self.number_of_households = number_of_households
        self.budget = budget
        self.contract = contract
        self.infrastructure = infrastructure

    # Maybe a function that is needed later
    # def renew_contract(self):
    #     expected_waste_next_year = np.mean(self.model.waste_per_year)


    def step(self):
        print("Hi, I am municipality " + str(self.unique_id) + ".")

        # New contract every 3 years
        if self.model.schedule.time % 36 == 1 and self.model.schedule.time != 0:
            print("I want a new contract for this amount of waste ", np.mean(self.model.waste_per_year[-3:]))
        return 0
