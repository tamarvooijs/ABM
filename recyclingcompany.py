from mesa import Agent
import math

class Contract():
    def __init__(self, Company, Municipality):
        self.company = Company
        self.municipality = Municipality

class RecyclingCompany(Agent):
    def __init__(self, unique_id, name, model, technology, contract, percentage_filtered):
        super().__init__(unique_id, model)
        self.agent = "Company"
        self.name = name
        self.technology = technology
        self.contract = contract
        self.percentage_filtered = percentage_filtered
        self.collected = 0
        self.max_throughput = math.inf

    def step(self):
        print("Hi, I am company " + str(self.unique_id) + ".")
        return 0
