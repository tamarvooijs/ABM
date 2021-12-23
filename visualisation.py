from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from main import RecyclingModel

def agent_portrayal(agent):
    if agent.agent == "Household":
        if agent.type == "Individual":
            portrayal = {"Shape": "circle",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": "red",
                         "r": 0.5}
        else:
            portrayal = {"Shape": "circle",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": "purple",
                         "r": 0.5}
    elif agent.agent == "Municipality":
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "blue",
                     "w":1,
                     "h":1}
    elif agent.agent == "Company":
        portrayal = {"Shape": "circle",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "grey",
                     "r": 2}
    return portrayal


Mun_Names = ["Rotterdam", "Den Haag"]
Comp_Names = ["Perpetual"]


grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)
server = ModularServer(RecyclingModel,
                       [grid],
                       "Recycling Model",
                       {})
server.port = 8521 # The default
server.launch()