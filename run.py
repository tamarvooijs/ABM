# library imports:
# mesa
from mesa import Agent, Model
from mesa.datacollection import DataCollector
# load all available schedulers
import mesa.time as time
import math
import random
# matplot lib for plotting, numpy for all sorts of useful math
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
# basic python statistics
import statistics as stat

# import pandas
import pandas as pd

# Required libraries for animation
from matplotlib.animation import FuncAnimation
from matplotlib import animation, rc, collections
from IPython.display import HTML

from model import RecyclingModel

from main import RecyclingModel

No_Mun = 1
No_Comp = 1
No_HH = 100

#Comp_Names = ["Perpetual"]
#model = RecyclingModel()

# def run_model():
#    model = RecyclingModel(policies = {"Knowledge": False, "Perception": True, "Knowledge + perception": False, "Technology": False})
#    number_of_steps = 240
#    for i in range(number_of_steps):
#       model.step()
#    return model.datacollector_waste.get_model_vars_dataframe()

# dataframe = run_model()
# print(dataframe)
# iterations = 100
# averages = []
# for i in range(iterations):
#     dataframe = run_model()
#     dataframe = dataframe[1:241]
#     dataframe["average_cities"] = (dataframe["Percentage recycled Rotterdam"] + dataframe["Percentage recycled Vlaardingen"] + dataframe["Percentage recycled Schiedam"])/3
#     averages.append(dataframe['average_cities'].mean())



model = RecyclingModel("knowledge_policy"== False, "perception_policy"== True, "perceptionknowledge_policy"== False, "technology_policy"== False)
model.run_model()
dataframe=model.datacollector_waste.get_model_vars_dataframe()

print("AVERAGE", dataframe["Percentage recycled Vlaardingen"][1:241].mean())
print(dataframe)

