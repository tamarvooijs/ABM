#library imports:
#mesa
from mesa import Agent
from recyclingcompany import Contract
import numpy as np
import random


class Municipality(Agent):
    def __init__(self, unique_id, name, model, number_of_households, budget, contract, infrastructure):
        super().__init__(unique_id, model)
        self.agent = "Municipality"
        self.name = name
        self.number_of_households = number_of_households
        self.budget = budget
        self.contract = contract
        self.infrastructure = infrastructure
        self.mun_waste_this_year = 0
        self.mun_waste_per_year = []


    # Maybe a function that is needed later
    # def renew_contract(self):
    #     expected_waste_next_year = np.mean(self.model.waste_per_year)


    def step(self):
        print("Hi, I am municipality " + str(self.unique_id) + ".")

        # New contract every 3 years
        if self.model.schedule.time % 36 == 1 and self.model.schedule.time != 1:
            self.search_contract()
            print("I want a new contract for this amount of waste ", np.mean(self.model.waste_per_year[-3:]))
        return 0

    def search_contract(self):

        list_of_companies = []
        largest_throughput = 0
        comp_largest_throughput = None

        for i in self.model.schedule.agents:
            if i.agent == "Company":
                # TODO: change model.waste_per_year to municipality average
                if i.max_throughput > np.mean(self.mun_waste_per_year[-3:]):
                    list_of_companies.append(i)
                if i.max_throughput > largest_throughput:
                    largest_throughput = i.max_throughput
                    comp_largest_throughput = i
        if not list_of_companies:
            company = comp_largest_throughput
        else:
            company = random.choice(list_of_companies)
        #TODO: look at percentage that a municipality want to recycle
        
        self.contract = Contract(company, self)

