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

    def __init__(self, knowledge_policy, household_num_rotterdam):
        self.height = 50
        self.width = 50
        self.grid = MultiGrid(self.width, self.height, False)
        self.schedule = RandomActivationPerType(self)
        self.waste_per_year = []
        self.waste_this_year = 0
        self.num_agents = 0
        self.exogenous_price = 0.25
        self.running = True
        self.citycells = {}
        self.knowledge_policy = knowledge_policy
        self.household_num_rotterdam = household_num_rotterdam
        self.generate_municipalities()

        self.generate_companies()

        self.datacollector_waste = DataCollector({
            "Waste Rotterdam": lambda self: self.waste_count_municipality("Rotterdam"),
            "Waste Vlaardingen": lambda self: self.waste_count_municipality("Vlaardingen"),
            "Waste Schiedam": lambda self: self.waste_count_municipality("Schiedam"),
            "Recycled plastic waste Rotterdam": lambda self: self.recycled_plastic_waste_municipality("Rotterdam"),
            "Recycled plastic waste Vlaardingen": lambda self: self.recycled_plastic_waste_municipality("Vlaardingen"),
            "Recycled plastic waste Schiedam": lambda self: self.recycled_plastic_waste_municipality("Schiedam"),
            "Percentage recycled Rotterdam": lambda self: self.recycled_plastic_waste_municipality(
                "Rotterdam") / self.waste_count_municipality("Rotterdam") if self.recycled_plastic_waste_municipality(
                "Rotterdam") != 0 else 0,
            "Percentage recycled Vlaardingen": lambda self: self.recycled_plastic_waste_municipality(
                "Vlaardingen") / self.waste_count_municipality("Vlaardingen") if self.recycled_plastic_waste_municipality(
                "Vlaardingen") != 0 else 0,
            "Percentage recycled Schiedam": lambda self: self.recycled_plastic_waste_municipality(
                "Schiedam")/ self.waste_count_municipality("Schiedam") if self.recycled_plastic_waste_municipality(
                "Schiedam") != 0 else 0
        })

        self.datacollector_waste.collect((self))

    def step(self):
        self.schedule.step()
        self.datacollector_waste.collect(self)
        total_waste = 0
        for i in self.schedule.agents:
            if i.agent == "Household":
                total_waste += i.recycled_plastic

                # Add waste of household to corresponding municipality
                for j in self.schedule.agents:
                    if j.agent == "Municipality" and i.municipality.name == j.unique_id:
                        # Add waste for this step to municipality
                        j.mun_waste_this_year += i.recycled_plastic


        # Municipalities keeping track of yearly produced waste in order to calculate a new contract
        for i in self.schedule.agents:
            if i.agent == "Municipality" and self.schedule.time % 12 != 0:
                self.waste_this_year += total_waste



            elif i.agent == "Municipality" and self.schedule.time % 12 == 0 and self.schedule.time != 0:
                self.waste_per_year.append(self.waste_this_year)
                try:
                    i.contract.company.collected_over_years[self.schedule.time] += self.waste_this_year
                except IndexError:
                    i.contract.company.collected_over_years.append(self.waste_this_year)

                self.waste_this_year = 0


    def generate_companies(self):
        Company_Names = ["alfa", "beta"]
        for i in range(len(Company_Names)):
            company = RecyclingCompany(Company_Names[i], self, 50)
            self.schedule.add(company)
            o = self.grid.find_empty()
            self.grid.place_agent(company, o)
            self.num_agents += 1


    def generate_municipalities(self):

        Mun_Names = {"Rotterdam": 10, "Vlaardingen": 5, "Schiedam": 7}

        for i in Mun_Names.keys():

            municipality = Municipality( i, self, Mun_Names[i])
            self.schedule.add(municipality)
            self.num_agents += 1


            z = self.grid.find_empty()
            self.grid.place_agent(municipality, z)

            self.citycells[municipality.name] = []
            self.citycells[municipality.name].append(z)

            for j in range(int(municipality.number_of_households)-1):
                neighbors = []
                while not neighbors:
                    u = random.randrange(0, len(self.citycells[municipality.name]))
                    neighbors = self.grid.get_neighborhood(self.citycells[municipality.name][u], False)

                    for k in neighbors:
                        if k in self.citycells[municipality.name]:
                            neighbors.remove(k)

                else:
                    y = random.choice(neighbors)
                    self.citycells[municipality.name].append(y)
                    self.grid.place_agent(municipality, y)

            RecyclingModel.generate_households(self, municipality.number_of_households, i, municipality)




    def generate_households(self, number_of_households, municipality_name, municipality):
        types_of_households = ["Individual", "Couple", "Family", "Retired_couple", "Retired_single"]

        # households are generated based on literature about the distribution of households in The Netherlands
        distribution_households_Rotterdam = [42, 8, 20, 1, 29]
        distribution_households_Schiedam = [36, 7, 15, 24, 18]
        distribution_households_Vlaardingen = [30, 9, 42, 7, 12]
        list_hh = []

        for i in range(number_of_households):
            random.seed(10)
            if municipality.name == "Rotterdam":
                type_hh = random.choices(types_of_households, distribution_households_Rotterdam)[0]
            elif municipality.name == "Schiedam":
                type_hh = random.choices(types_of_households, distribution_households_Schiedam)[0]
            elif municipality.name == "Vlaardingen":
                type_hh = random.choices(types_of_households, distribution_households_Vlaardingen)[0]
            household = Household((municipality, i), self, type_hh, "yes", municipality)
            self.num_agents += 1
            self.schedule.add(household)

            MyCells = []

            for j in self.citycells.keys():
                if household.municipality.name == j:
                    MyCells.append(self.citycells[j])
                    cell = random.choice(random.choice(MyCells))
                    self.grid.place_agent(household, cell)
                    self.citycells[j].remove(cell)


            list_hh.append(type_hh)
        print("list", list_hh)
        return

    def waste_count_municipality(model, municipality):
        municipality_waste = sum([agent.produced_waste_volume_updated for agent in model.schedule.agents if agent.agent=="Household" and agent.municipality.name == municipality])
        return municipality_waste

    def total_plastic_waste_municipality(model, municipality):
        municipality_plastic_waste = sum([agent.recycled_plastic for agent in model.schedule.agents if
                                          agent.agent == "Household" and agent.municipality.name == municipality])
        return municipality_plastic_waste

    def recycled_plastic_waste_municipality(model, municipality):
        recycled_municipality_plastic_waste = sum([agent.recycled_plastic * agent.municipality.factor_company for agent in model.schedule.agents if agent.agent == "Household" and agent.municipality.name == municipality])
        return recycled_municipality_plastic_waste











