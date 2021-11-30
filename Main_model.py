class RecyclingModel(Model):
    "Model in which agents recycle"

    def __init__(self, No_HH, No_Mun, No_Comp, width, height):
        self.schedule = time.RandomActivation(self)
        self.No_Mun = No_Mun
        self.grid = MultiGrid(width, height, True)



        for i in range(No_HH):
            household = Household(i, self,"single", "yes", "Rotterdam", produced_volume=2, knowledge=0.5, perception=0.5)
            self.schedule.add(household)

        for i in range(No_Mun):
            municipality = Municipality(i+No_HH, self, 1, 100, 1, 3)
            self.schedule.add(municipality)
            # Create municipalities
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(municipality, (x, y))
            add(agent:household)

        for i in range(No_Comp):
            company = RecyclingCompany(i+No_Mun+No_HH, self, "technology 1", "contract 2", 50)
            self.schedule.add(company)

    def step(self):
        self.schedule.step()