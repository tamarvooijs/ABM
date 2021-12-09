from mesa import Agent

class RecyclingCompany(Agent):
    def __init__(self, unique_id, model, technology, contract, percentage_filtered):
        super().__init__(unique_id, model)
        self.agent = "Company"
        self.technology = technology
        self.contract = contract
        self.percentage_filtered = percentage_filtered
        self.collected = 0

    def step(self):
        print("Hi, I am company " + str(self.unique_id) + ".")
        return 0
