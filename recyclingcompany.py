from mesa import Agent
import math
from technology import Technology
from scipy.stats import bernoulli
import random

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
        self.contracts = []
        self.percentage_filtered = 0
        self.average_percentage = []
        self.collected_over_years = []
        self.profit = 0.0
        self.budget = random.uniform(200, 800)


    def step(self):
        if bool(self.contracts):
            if self.model.schedule.time % 12 != 0:

                self.technology.last_renewed += 1
                # In this case, technologies have a constant price


                for i in self.contracts:

                    costs_technology = self.technology.costs
                    if i.municipality.policies["Technology"] == True:
                        costs_technology = self.technology.costs / 2

                if self.budget > costs_technology:
                    if self.technology.last_renewed/10 < 1:
                        p = self.technology.last_renewed/10
                    else:
                        p=1
                    if bernoulli.rvs(size=1, p= p):

                        self.technology.version += 1
                        self.technology.throughput = self.technology.throughput * 1.1
                        self.technology.percentage = 0.5 + (self.technology.percentage/(math.sqrt((self.technology.percentage * self.technology.percentage)+1)))/2
                        self.technology.last_renewed = 0


                        self.budget -= costs_technology

            if self.model.schedule.time % 12 == 0 and self.model.schedule.time != 0:
                self.calculate_profits()
                self.percentage_filtered = self.average_percentage[-1] * self.technology.percentage
                for i in self.contracts:
                    i.municipality.factor_company = self.percentage_filtered
                self.budget += self.profit
            #print("Hi, I am company " + str(self.unique_id) + " and my contracts are" + str(self.contracts))
            return 0

    def calculate_profits(self):
        total_amount = 0

        for i in self.contracts:
            total_amount += i.municipality.mun_waste_per_year[-1]

        if total_amount > self.technology.throughput:
            average_percentage = self.technology.throughput/total_amount
            total_amount = self.technology.throughput
        else:
            average_percentage = 1
        self.average_percentage.append(average_percentage)
        self.profit = total_amount * self.model.exogenous_price
        # use number in decision to invest in technologies.

