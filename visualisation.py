from main import RecyclingModel

def agent_portrayal(agent: Municipality):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 2}
    return portrayal

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(RecyclingModel,
                       [grid],
                       "Recycling Model",
                       {"No_HH":5, "No_Mun":1, "No_Comp":2, "width":10, "height":10})
server.port = 8521 # The default
server.launch()