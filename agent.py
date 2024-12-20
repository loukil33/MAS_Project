from mesa import Agent



class User(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wait_time = 0

    def step(self):
        self.wait_time += 1

class Vehicle(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.state = "Available"
        self.battery = 100
        self.destination = None

    def step(self):
        if self.state == "In Use":
            if self.destination:
                self.move_toward(self.destination)
                self.battery -= self.model.battery_depletion_rate / self.model.trip_duration
                if self.pos == self.destination:
                    self.state = "Needs Recharging" if self.battery <= 0 else "Available"
                    self.destination = None
        elif self.state == "Available":
            if self.battery <= self.model.low_battery_threshold:
                self.state = "Going to Recharge"
                self.destination = self.closest_charging_station()
            else:
                nearby_users = self.model.grid.get_neighbors(self.pos, moore=True, radius=self.model.user_range)
                users = [u for u in nearby_users if isinstance(u, User)]
                if users:
                    user = users[0]  
                    self.destination = user.pos
                    if self.pos != self.destination:
                        self.move_toward(self.destination)
                    if self.pos == user.pos:
                        self.state = "In Use"
                        self.destination = (self.model.random.randrange(self.model.grid.width),
                                            self.model.random.randrange(self.model.grid.height))
                        self.model.grid.remove_agent(user)
                        self.model.schedule.remove(user)
                        self.model.generate_user()
                else:
                    self.random_move()
        elif self.state == "Going to Recharge":
            if self.destination:
                self.move_toward(self.destination)
                if self.pos == self.destination:
                    self.state = "Recharging"
        elif self.state == "Recharging":
            if self.battery < 100:
                self.battery += self.model.recharge_rate
            if self.battery >= 100:
                self.battery = 100
                self.state = "Available"
        elif self.battery <= self.model.low_battery_threshold and self.state != "Recharging":
            self.state = "Going to Recharge"

    def move_toward(self, destination):
        x, y = self.pos
        dest_x, dest_y = destination
        new_x = x + (1 if dest_x > x else -1 if dest_x < x else 0)
        new_y = y + (1 if dest_y > y else -1 if dest_y < y else 0)
        self.model.grid.move_agent(self, (new_x, new_y))

    def random_move(self):
        possible_steps = self.model.grid.get_neighborhood(self.pos, moore=True, include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def closest_charging_station(self):
        charging_stations = [a for a in self.model.schedule.agents if isinstance(a, ChargingStation)]
        return min(charging_stations, key=lambda cs: self.euclidean_distance(self.pos, cs.pos)).pos

    def euclidean_distance(self, pos1, pos2):
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5


class ChargingStation(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
