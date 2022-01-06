from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
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

chart_waste_total = ChartModule(
    [
        {"Label": "Waste Rotterdam", "Color": "green"},
        {"Label": "Waste Vlaardingen", "Color": "red"},
        {"Label": "Waste Schiedam", "Color": "yellow"},
    ],
    canvas_height= 300,
    data_collector_name="datacollector_waste"
)

chart_waste_plastic = ChartModule(
    [
        {"Label": "Plastic waste Rotterdam", "Color": "green"},
        {"Label": "Plastic waste Vlaardingen", "Color": "red"},
        {"Label": "Plastic waste Schiedam", "Color": "yellow"},
    ],
    canvas_height= 300,
    data_collector_name="datacollector_waste"
)

server = ModularServer(RecyclingModel,
                       [grid, chart_waste_total, chart_waste_plastic],
                       "Recycling Model",
                       {})
server.port = 8521 # The default
server.launch()