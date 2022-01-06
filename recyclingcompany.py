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
        self.contracts = []
        self.percentage_filtered = percentage_filtered
        self.average_percentage = []
        self.collected_over_years = []
        self.profit = 0.0
        self.budget = 0.0

    def step(self):

        if self.model.schedule.time % 12 != 0:

            self.technology.last_renewed += 1
            # In this case, technologies have a constant price
            if self.budget > self.technology.costs:
                if self.technology.last_renewed/10 < 1:
                    p = self.technology.last_renewed/10
                else:
                    p=1
                if bernoulli.rvs(size=1, p= p):
                    print("update")
                    self.technology.version += 1
                    self.technology.throughput = self.technology.throughput * 1.1
                    self.technology.percentage = 0.5+ (self.technology.percentage/(math.sqrt((self.technology.percentage * self.technology.percentage)+1)))/2
                    self.technology.last_renewed = 0


                    self.budget -= self.technology.costs

        if self.model.schedule.time % 12 == 0 and self.model.schedule.time != 0:
            self.calculate_profits()
            self.budget += self.profit
            print("my budget is ", self.unique_id, self.budget)



        print("Hi, I am company " + str(self.unique_id) + " and my contracts are" + str(self.contracts))
        return 0

    def calculate_profits(self):
        total_amount = 0

        for i in self.contracts:
            total_amount += i.municipality.mun_waste_per_year[-1]
        print("Amount:", total_amount)
        if total_amount > self.technology.throughput:
            total_amount = self.technology.throughput
        self.average_percentage = total_amount
        self.profit = total_amount * self.model.exogenous_price
        print("Amount",  total_amount)
        print("Percentage", self.unique_id, self.technology.percentage)

        # use number in decision to invest in technologies.

