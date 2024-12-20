from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import Slider
from mesa.visualization.ModularVisualization import ModularServer
from model import MicromobilityModel
from agent import Vehicle, User, ChargingStation

# Visualization
def agent_portrayal(agent):
    portrayal = {}
    if isinstance(agent, Vehicle):
        portrayal = {"Shape": "circle", "r": 0.5, "Filled": True, "Layer": 1}
        if agent.state == "Available":
            portrayal["Color"] = "green"
        elif agent.state == "In Use":
            portrayal["Color"] = "blue"
        elif agent.state == "Needs Recharging" or agent.state == "Going to Recharge":
            portrayal["Color"] = "red"
        elif agent.state == "Recharging":
            portrayal["Color"] = "orange"
    elif isinstance(agent, User):
        portrayal = {"Shape": "circle", "r": 0.3, "Color": "yellow", "Filled": True, "Layer": 2}
    elif isinstance(agent, ChargingStation):
        portrayal = {"Shape": "rect", "w": 0.5, "h": 0.5, "Color": "gray", "Filled": True, "Layer": 0}
    return portrayal


grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

chart_vehicle_availability = ChartModule([{"Label": "Vehicle Availability", "Color": "green"}])
chart_average_wait_time = ChartModule([{"Label": "Average User Wait Time", "Color": "blue"}])
chart_vehicle_utilization = ChartModule([{"Label": "Vehicle Utilization", "Color": "red"}])

server = ModularServer(
    MicromobilityModel,
    [grid, chart_vehicle_availability, chart_average_wait_time, chart_vehicle_utilization],
    "Shared Micromobility Simulation",
    {
        "width": 10,
        "height": 10,
        "num_vehicles": Slider("Number of Vehicles", 7, 1, 20),
        "num_users": Slider("Initial Number of Users", 3, 0, 20),
        "num_charging_stations": Slider("Number of Charging Stations", 5, 1, 10),
        "battery_depletion_rate": Slider("Battery Depletion Rate", 10, 1, 50),
        "recharge_rate": Slider("Recharge Rate", 20, 1, 50),
        "trip_duration": Slider("Trip Duration", 5, 1, 20),
        "user_range": Slider("User Range", 2, 1, 5),
        "low_battery_threshold": Slider("Low Battery Threshold", 35, 1, 50),
        "user_demand_probability": Slider("User Demand Probability", 0, 0, 1, 0.05),
        "high_demand_center_x": Slider("High Demand Center X", 3, 0, 10, 1),
        "high_demand_center_y": Slider("High Demand Center Y", 2, 0, 10, 1),
        "high_demand_radius": Slider("High Demand Radius", 1, 1, 5, 1),
        "high_demand_probability": Slider("High Demand Probability", 0.1, 0, 1, 0.05),
    },
)


if __name__ == "__main__":
    server.port = 8521
    server.launch() 
