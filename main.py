# Libraries
from municipality import Municipality
from household import Household
from recyclingcompany import RecyclingCompany
from mesa import Agent, Model
import mesa.time as time
import random
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.datacollection import DataCollector

#import space mesa
from mesa.space import MultiGrid

# Required libraries for animation
from matplotlib.animation import FuncAnimation
from matplotlib import animation, rc, collections
from IPython.display import HTML

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

    def __init__(self, No_HH, No_Mun, No_Comp):
        self.height = 10
        self.width = 10
        self.grid = MultiGrid(self.width, self.height, True)
        self.schedule = RandomActivationPerType(self)
        self.waste_per_year = []
        self.waste_this_year = 0
        self.forced_step = 0

        RecyclingModel.generate_households(self, No_HH)


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
                total_waste += i.produced_waste_volume_updated
        # Municipalities keeping track of yearly produced waste in order to calculate a new contract
        for i in self.schedule.agents:
            if i.agent == "Municipality" and self.forced_step % 12 != 0:
                self.waste_this_year += total_waste
            elif i.agent == "Municipality" and self.forced_step % 12 == 0 and self.forced_step != 0:
                self.waste_per_year.append(self.waste_this_year)
                self.waste_this_year = 0
                print("List of waste collected every year: ", self.waste_per_year)

        for i in self.schedule.agents:
            # This only works if there is one recyclingcompany
            # TO DO: aggregate to more companies
            if i.agent == "Company":
                i.collected += total_waste
                waste_collected = i.collected
        print("Total waste this round equals ", total_waste)
        print("Total collected", waste_collected)
        self.forced_step += 1       # Quick fix to the step counting problem

    def generate_households(self, number_of_households):
        types_of_households = ["Individual", "Couple", "Family", "Retired_couple", "Retired_single"]

        # households are generated based on literature about the distribution of households in The Netherlands
        distribution_households = [0.35, 0.27, 0.33, 0.02, 0.04]
        list_hh = []

        for i in range(number_of_households):

            type_hh = random.choices(types_of_households, distribution_households)[0]
            household = Household(i, self, type_hh, "yes", "Rotterdam")
            self.schedule.add(household)
            list_hh.append(type_hh)
        print("list", list_hh)
        return


model = RecyclingModel(100, 2, 1)

number_of_steps = 40
for i in range(number_of_steps):
   print("Step:", i)
   model.step()





