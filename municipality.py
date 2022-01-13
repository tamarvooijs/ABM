#library imports:
#mesa
from mesa import Agent
from recyclingcompany import Contract
import numpy as np
import random


class Municipality(Agent):
    def __init__(self, unique_id, model, number_of_households):
        super().__init__(unique_id, model)
        self.agent = "Municipality"
        self.name = unique_id
        self.number_of_households = number_of_households
        self.budget = 0
        self.contract = None
        self.infrastructure = True
        self.mun_waste_this_year = 0
        self.mun_waste_per_year = []
        # TODO: implement policies as numbers/names that are either True or False
        self.policies = {"Knowledge": False, "Perception": False, "Knowledge + perception": False, "Technology": False}

    def step(self):
        print("Hi, I am municipality " + str(self.unique_id) + ".")

        # Store waste for every year in mun_waste_per_year
        if self.model.schedule.time % 12 == 0 and self.model.schedule.time != 0:
            self.mun_waste_per_year.append(self.mun_waste_this_year)
            self.mun_waste_this_year = 0

        # New contract every 3 years
        if self.model.schedule.time % 36 == 1 and self.model.schedule.time != 1:
            self.search_contract()
            print("I want a new contract for this amount of waste ", np.mean(self.mun_waste_per_year[-3:]))

        elif self.model.schedule.time == 0:
            list_companies = []
            for i in self.model.schedule.agents:
                if i.agent == "Company":
                    list_companies.append(i)

            company = random.choice(list_companies)
            self.contract = Contract(company, self)
            company.contracts.append(self.contract)
        return 0

    def search_contract(self):

        list_of_companies = []
        largest_throughput = 0
        comp_largest_throughput = None

        for i in self.model.schedule.agents:
            if i.agent == "Company":
                if i.technology.throughput > np.mean(self.mun_waste_per_year[-3:]):
                    list_of_companies.append(i)
                if i.technology.throughput > largest_throughput:
                    largest_throughput = i.technology.throughput
                    comp_largest_throughput = i
        if not list_of_companies:
            company = comp_largest_throughput
        else:
            company = random.choice(list_of_companies)


        self.contract = Contract(company, self)
        company.contracts.append(self.contract)



