from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from main import RecyclingModel

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 2}
    return portrayal

grid = CanvasGrid(agent_portrayal, 5, 5, 500, 500)
server = ModularServer(RecyclingModel,
                       [grid],
                       "Recycling Model",
                       {"No_HH":5, "No_Mun":1, "No_Comp":2})
server.port = 8521 # The default
server.launch()
