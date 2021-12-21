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

Comp_Names = ["Perpetual"]
model = RecyclingModel()


number_of_steps = 240
for i in range(number_of_steps):
   print("Step:", i)
   model.step()