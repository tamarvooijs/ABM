from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from main import RecyclingModel
from mesa.visualization.UserParam import UserSettableParameter


def agent_portrayal(agent):
    if agent.agent == "Household":
        if agent.knowledge > 0.7:
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
        if agent.percentage_filtered < 0.1:
            portrayal = {"Shape": "circle",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": "grey",
                         "r": 1}
        else:
            big = agent.percentage_filtered * 5
            portrayal = {"Shape": "circle",
                         "Filled": "true",
                         "Layer": 0,
                         "Color": "grey",
                         "r": big}

    return portrayal

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
        {"Label": "Recycled plastic waste Rotterdam", "Color": "green"},
        {"Label": "Recycled plastic waste Vlaardingen", "Color": "red"},
        {"Label": "Recycled plastic waste Schiedam", "Color": "yellow"},
    ],
    canvas_height= 300,
    data_collector_name="datacollector_waste"
)

chart_percentage_plastic = ChartModule(
    [
        {"Label": "Percentage recycled Rotterdam", "Color": "green"},
        {"Label": "Percentage recycled Vlaardingen", "Color": "red"},
        {"Label": "Percentage recycled Schiedam", "Color": "yellow"},
    ],
    canvas_height= 300,
    data_collector_name="datacollector_waste"
)

# If we want a nice dashboard to play with

model_params = {
    "knowledge_policy": UserSettableParameter("checkbox", "Knowledge policy", value=False),
    "household_num_rotterdam": UserSettableParameter("slider", "Households Rotterdam", 50, 1, 100, 1)
    }


server = ModularServer(RecyclingModel,
                       [grid, chart_percentage_plastic],
                       "Recycling Model",
                       {"policies" :{"Knowledge": True, "Perception": False, "Knowledge + perception": False, "Technology": False}})
server.port = 8521 # The default
server.launch()