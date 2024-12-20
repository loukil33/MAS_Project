from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np
from agent import Vehicle, User, ChargingStation


class MicromobilityModel(Model):
    def __init__(self, width, height, num_vehicles, num_users, num_charging_stations,
                 battery_depletion_rate, recharge_rate, trip_duration, user_range, 
                 low_battery_threshold, user_demand_probability,
                 high_demand_center_x, high_demand_center_y, high_demand_radius, high_demand_probability):
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = RandomActivation(self)
        self.num_vehicles = num_vehicles
        self.num_users = num_users
        self.num_charging_stations = num_charging_stations
        self.battery_depletion_rate = battery_depletion_rate
        self.recharge_rate = recharge_rate
        self.trip_duration = trip_duration
        self.user_range = user_range
        self.low_battery_threshold = low_battery_threshold
        self.user_demand_probability = user_demand_probability

        # Construct high demand zone dynamically
        self.high_demand_zone = {
            "center": (high_demand_center_x, high_demand_center_y),
            "radius": high_demand_radius,
            "probability": high_demand_probability,
        }
        self.running = True

        self.datacollector = DataCollector(
            {
                "Vehicle Availability": lambda m: sum(1 for v in m.schedule.agents if isinstance(v, Vehicle) and v.state == "Available") / m.num_vehicles * 100,
                "Average User Wait Time": lambda m: np.mean([u.wait_time for u in m.schedule.agents if isinstance(u, User)]) if any(isinstance(u, User) for u in m.schedule.agents) else 0,
                "Vehicle Utilization": lambda m: sum(1 for v in m.schedule.agents if isinstance(v, Vehicle) and v.state == "In Use") / m.num_vehicles * 100,
            }
        )

        # Add vehicles
        for i in range(self.num_vehicles):
            vehicle = Vehicle(i, self)
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(vehicle, (x, y))
            self.schedule.add(vehicle)

        # Add users
        for i in range(self.num_users):
            self.generate_user()

        # Add charging stations
        for i in range(self.num_charging_stations):
            station = ChargingStation(self.num_vehicles + self.num_users + i, self)
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(station, (x, y))
            self.schedule.add(station)

    def generate_user(self):
        center = self.high_demand_zone["center"]
        radius = self.high_demand_zone["radius"]
        high_demand_probability = self.high_demand_zone["probability"]

        if self.random.random() < high_demand_probability:
            x = self.random.randint(max(center[0] - radius, 0), min(center[0] + radius, self.grid.width - 1))
            y = self.random.randint(max(center[1] - radius, 0), min(center[1] + radius, self.grid.height - 1))
        else:
            x, y = self.random.randrange(self.grid.width), self.random.randrange(self.grid.height)

        user = User(self.num_vehicles + len([a for a in self.schedule.agents if isinstance(a, User)]), self)
        self.grid.place_agent(user, (x, y))
        self.schedule.add(user)

    def step(self):
        self.schedule.step()
        
        # Generate new users based on user demand probability
        if self.random.random() < self.user_demand_probability:
            self.generate_user()
        
        self.datacollector.collect(self)
