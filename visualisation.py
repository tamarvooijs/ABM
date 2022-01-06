from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from main import RecyclingModel


def agent_portrayal(agent):
    if agent.agent == "Household":
        if agent.knowledge > 0.8:
            portrayal = {"Shape": "circle",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": "red",
                         "r": 0.5}
        elif agent.knowledge > 0.5:
            portrayal = {"Shape": "circle",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": "orange",
                         "r": 0.5}
        else:
            portrayal = {"Shape": "circle",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": "yellow",
                         "r": 0.5}
    elif agent.agent == "Municipality":
        portrayal = {"Shape": "rect",
                     "Filled": "true",
                     "Layer": 0,
                     "Color": "black",
                     "w":1,
                     "h":1}
    elif agent.agent == "Company":
        if agent.technology.throughput < 1000:
            portrayal = {"Shape": "circle",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": "grey",
                         "r": 1}
        else:
            big = agent.technology.throughput / 1000
            portrayal = {"Shape": "circle",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": "grey",
                         "r": big}

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