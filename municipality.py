#library imports:
#mesa
from mesa import Agent
from recyclingcompany import Contract
import numpy as np
import random


class Municipality(Agent):
    """ Municipalities collect the waste from the households, can use different policies and have contract with the recycling companies """
    def __init__(self, unique_id, model, number_of_households):
        super().__init__(unique_id, model)
        self.agent = "Municipality"
        self.name = unique_id
        self.number_of_households = number_of_households
        self.contract = None
        self.infrastructure = True
        self.mun_waste_this_year = 0
        self.mun_waste_per_year = []
        self.policies = self.model.policies
        self.factor_company = 0.4

    def step(self):

        # Store waste for every year in mun_waste_per_year
        if self.model.schedule.time % 12 == 0 and self.model.schedule.time != 0:
            self.mun_waste_per_year.append(self.mun_waste_this_year)
            self.mun_waste_this_year = 0

        # New contract every 3 years
        if self.model.schedule.time % 36 == 1 and self.model.schedule.time != 1:
            self.search_contract()

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



