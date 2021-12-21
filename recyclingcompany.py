from mesa import Agent
import math
from technology import Technology
from scipy.stats import bernoulli

class Contract():
    def __init__(self, Company, Municipality):
        self.company = Company
        self.municipality = Municipality


class RecyclingCompany(Agent):
    def __init__(self, unique_id, model, percentage_filtered):
        super().__init__(unique_id, model)
        self.agent = "Company"
        self.model = model
        self.technology = Technology("T" + unique_id, self.model)
        # make list of contracts here instead of one contract
        self.contracts = []
        self.percentage_filtered = percentage_filtered
        self.collected = 0
        self.max_throughput = math.inf
        self.budget = 1000

    def step(self):

        if self.model.schedule.time % 12 != 0:

            self.technology.last_renewed += 1
            if bernoulli.rvs(size=1, p= self.technology.last_renewed/10):
                self.technology.update_technology()
                self.budget -= self.technology.costs



        print("Hi, I am company " + str(self.unique_id) + " and I have contracts" + str(self.contracts))
        return 0

    def calculate_profits(self):
        for i in self.contracts:
    

        #TODO:
        # calculate the throughput here
        # by looping over contracts
        # and calculating the total waste in all municipalities
        # check whether throughput exceeds the max throughput, throughput = min(max throughput, thhroughput)
        # multiply throughput with factor of earnings
        # use number in decision to invest in technologies.
        self.waste_per_year.append(self.waste_this_year)