from mesa import Agent
from mesa.datacollection import DataCollector
#load all available schedulers
import mesa.time as time
import math
import random
import numpy as np


def waste(x, type):
    """ To calculate the base waste of one type of a household"""
    if type == "Individual" or "Retired_single":
        number_of_persons = 1
    elif type == "Couple" or "Retired_couple":
        number_of_persons = 2
    elif type == "Family":
        number_of_persons = 4
    else:
        print("error")
        return 1

    waste_function = 40 - 0.04 * x - math.exp(-0.01 * x) * math.sin(0.3 * x) * number_of_persons
    waste = waste_function * random.uniform(0.95, 1.05)
    return waste


class Household(Agent):
    "Households that recycle a certain amount of plastic each year"

    def __init__(self, unique_id, model, type, access, municipality):
        super().__init__(unique_id, model)
        self.agent = "Household"
        self.type = type
        self.access = access
        self.municipality = municipality
        self.produced_waste_volume_base = waste(self.model.schedule.time, self.type)
        self.produced_waste_volume_updated = 0
        self.factor_plastic = 0.3
        self.produced_plastic = 0
        self.recycled_plastic = 0
        Household.initial_knowledge(self)
        Household.initial_perception(self)

    def step(self):

        self.produced_waste_volume_updated = waste(self.model.schedule.time, self.type)
        # perception influences the plastic that is separated
        self.produced_plastic = self.produced_waste_volume_updated * self.factor_plastic
        # knowledge influences the plastic that is valuable
        self.recycled_plastic = self.produced_plastic  * self.knowledge * self.perception

        if self.municipality.policies["Perception"] == True or self.municipality.policies["Knowledge + perception"] == True:

                self.perception += random.uniform(0, 0.2)

    def initial_perception(self):
        perception_range = (0, 0)

        if self.type == "Individual":
            perception_range = (0.4, 0.6)
            perception_time = np.round(np.random.beta(2,2) * 24, 0)
            perception_change = random.uniform(0.1, 0.2)
        elif self.type == "Retired_couple":
            perception_range = (0.2, 0.5)
            perception_time = np.round(np.random.beta(2,3) * 24, 0)
            perception_change = random.uniform(0.05, 0.15)
        elif self.type == "Retired_single":
            perception_range = (0.2, 0.5)
            perception_time = np.round(np.random.beta(2,4) * 24, 0)
            perception_change = random.uniform(0, 0.15)
        elif self.type == "Couple":
            perception_range = (0.5, 0.7)
            perception_time = np.round(np.random.beta(4,2) * 24, 0)
            perception_change = random.uniform(0.15, 0.2)
        elif self.type == "Family":
            perception_range = (0.4, 0.7)
            perception_time = np.round(np.random.beta(3,2) * 24, 0)
            perception_change = random.uniform(0.05, 0.1)

        self.perception = random.uniform(perception_range[0], perception_range[1])
        self.perception_time = perception_time
        self.perception_change = perception_change
        # if self.municipality.policies["Perception"] == True or self.municipality.policies["Knowledge + perception"] == True:
        #     self.perception += random.uniform(0.05, 0.2)

    def initial_knowledge(self):
        knowledge_range = (0, 0)

        if self.type == "Individual":
            knowledge_range = (0.4, 0.6)
        elif self.type == "Retired_couple" or "Retired_single":
            knowledge_range = (0.2, 0.5)
        elif self.type == "Couple":
            knowledge_range = (0.5, 0.7)
        elif self.type == "Family":
            knowledge_range = (0.3, 0.6)

        self.knowledge = random.uniform(knowledge_range[0], knowledge_range[1])
        if self.municipality.policies["Knowledge"] == True or self.municipality.policies["Knowledge + perception"] == True:
            self.knowledge += random.uniform(0, 0.2)



