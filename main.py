# Libraries
from municipality import Municipality
from household import Household
from recyclingcompany import RecyclingCompany, Contract
from technology import Technology
from mesa import Agent, Model
import mesa.time as time
import random
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.datacollection import DataCollector

#import space mesa
from mesa.space import MultiGrid
from mesa.space import Grid

# Required libraries for animation
from matplotlib.animation import FuncAnimation
from matplotlib import animation, rc, collections
from IPython.display import HTML

import itertools


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
        for i in sequence:
            for agent in self.agent_buffer(shuffled=True):
                if agent.agent == i:
                    agent.step()

        self.steps += 1
        self.time += 1


class RecyclingModel(Model):
    "Model in which agents recycle"


    def __init__(self, No_Comp, Comp_Names):
        self.height = 1000
        self.width = 1000
        self.grid = MultiGrid(self.width, self.height, True)
        self.schedule = RandomActivationPerType(self)
        self.waste_per_year = []
        self.waste_this_year = 0
        self.num_agents = 0


        self.generate_municipalities()

        self.generate_companies()


    def step(self):
        self.schedule.step()
        total_waste = 0
        for i in self.schedule.agents:
            if i.agent == "Household":
                total_waste += i.produced_waste_volume_updated

                # Add waste of household to corresponding municipality
                for j in self.schedule.agents:
                    if j.agent == "Municipality" and i.municipality == j.unique_id:
                        # Add waste for this step to municipality
                        j.mun_waste_this_year += i.produced_waste_volume_updated


        # Municipalities keeping track of yearly produced waste in order to calculate a new contract
        for i in self.schedule.agents:
            if i.agent == "Municipality" and self.schedule.time % 12 != 0:
                self.waste_this_year += total_waste

            elif i.agent == "Municipality" and self.schedule.time % 12 == 0 and self.schedule.time != 0:
                self.waste_per_year.append(self.waste_this_year)
                self.waste_this_year = 0


        for i in self.schedule.agents:
            # This only works if there is one recyclingcompany
            # TO DO: aggregate to more companies
            if i.agent == "Company":
                i.collected += total_waste
                waste_collected = i.collected
        print("Total waste this round equals ", total_waste)
        print("Total collected", waste_collected)


    def generate_companies(self):
        Company_Names = ["alfa", "beta"]
        for i in range(len(Company_Names)):
            company = RecyclingCompany(Company_Names[i], self, 50)
            self.schedule.add(company)
            self.num_agents += 1


    def generate_municipalities(self):

        Mun_Names = {"Rotterdam": 10, "Vlaardingen": 5, "Schiedam": 7}

        for i in Mun_Names.keys():

            municipality = Municipality( i, self, Mun_Names[i])
            self.schedule.add(municipality)
            self.num_agents += 1

            # Create municipalities on a random grid cell
            z = self.grid.find_empty()
            self.grid.place_agent(municipality,z)
            RecyclingModel.generate_households(self, municipality.number_of_households, i)


    def generate_households(self, number_of_households, municipality):
        types_of_households = ["Individual", "Couple", "Family", "Retired_couple", "Retired_single"]

        # households are generated based on literature about the distribution of households in The Netherlands
        distribution_households = [0.35, 0.27, 0.33, 0.02, 0.04]
        list_hh = []

        for i in range(number_of_households):

            type_hh = random.choices(types_of_households, distribution_households)[0]
            household = Household((municipality, i), self, type_hh, "yes", municipality)
            self.num_agents += 1
            self.schedule.add(household)

            # Create households on an empty cell:
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(household, (x, y))


            list_hh.append(type_hh)
        print("list", list_hh)
        return







