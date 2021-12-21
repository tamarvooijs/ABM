
class Technology:
    "Type of technology that is used by recycling company"

    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        self.model = model
        self.version = 0
        self.last_renewed = 0
        self.percentage = 1
        self.throughput = 1000
        self.new = False
        self.costs = 500

    def update_technology(self):
        self.version += 1
        self.throughput = (self.throughput * 1.1)/self.throughput
        self.percentage = self.percentage * 1.1
        self.last_renewed = 0



