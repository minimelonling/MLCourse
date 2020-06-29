distance = 405
targets = [315, 315, 315, 315]

class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0
        self.car_pos = (0, 0)
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]
        self.lane = 315
        self.target = 315
        pass

    def update(self, scene_info):
        for key in scene_info.keys():
            print(key)
        global flag
        """
        Generate the command according to the received scene information
        """
        self.car_pos = scene_info[self.player]
        for car in scene_info["cars_info"]:
            if car["id"]==self.player_no:
                self.car_vel = car["velocity"]
        if scene_info["status"] != "ALIVE":
            return "RESET"
        if self.encounter_threat(scene_info):
            self.change_lane(scene_info)
        return self.move(scene_info)
        return ["MOVE_LEFT", "MOVE_RIGHT", "SPEED", "BRAKE"]

    def print_scene(self, scene_info):
        for i in scene_info.keys():
            if i == "computer_cars":
                print("computer_cars:")
                for j in scene_info[i]:
                    print("           " + str(j))
            elif i == "cars_info":
                print("cars_info: ")
                for j in scene_info[i]:
                    print(j)
            else:
                print(str(i) + ": " + str(scene_info[i]))

    def encounter_threat(self, scene_info):
        global distance
        global flag
        group = []
        closest = None
        for car in scene_info["cars_info"]:
            if len(self.car_pos) != 0 and car["pos"][0] == self.lane and car["id"] != self.player_no and car["pos"][1] < self.car_pos[1]:
                group.append(car)
        for car in group:
            if closest is None or closest["pos"][1] < car["pos"][1]:
                closest = car
        if closest != None and self.car_pos[1] - closest["pos"][1] < distance:
            return  True
        return False

    def change_lane(self, scene_info):
        print("change")
        group = []
        closest = None
        min_time = 0
        for car in scene_info["cars_info"]:
            if car["pos"][1] < self.car_pos[1]:
                if car["pos"][0] == self.car_pos[0] - 70:
                    group.append(car)
                elif car["pos"][0] == self.car_pos[0] +70:
                    group.append(car)
        for car in group:
            if closest == None or (self.car_pos[1] - car["pos"][1]) / (self.car_vel - car["velocity"]) < (self.car_pos[1] - closest["pos"][1]) / (self.car_vel - closest["velocity"]):
                closest = car
        if closest != None:
            if closest["pos"][0] == self.car_pos[0] - 70:
                if self.lane == 595:
                    self.target = self.lane - 70
                else:
                    self.target = self.lane + 70
            else:
                if self.lane == 35:
                    self.target = self.lane + 70
                else:
                    self.target = self.lane - 70
        else:
            if self.lane <= 315:
                self.target = self.lane + 70
            else:
                self.target = self.lane - 70
        self.lane = self.target
        global targets
        targets[self.player_no] = self.target
            
    def move(self, scene_info):
        global targets
        for car in scene_info["cars_info"]:
            if len(self.car_pos) != 0 and car["pos"][0] == self.target and self.car_pos[1] - car["pos"][1] < 85 and self.car_pos[1] - car["pos"][1] > -85:
                return ["SPEED"]
            elif len(self.car_pos) != 0 and car["pos"][0] - self.car_pos[0] < 45 and car["pos"][0] - self.car_pos[0] > 40 and car["pos"][1] - self.car_pos[1] < 85 and car["pos"][1] - self.car_pos[1] > -85:
                self.lane = self.lane - 70
                return ["SPEED"]
            elif len(self.car_pos) != 0 and car["pos"][0] - self.car_pos[0] > -45 and car["pos"][0] - self.car_pos[0] < -40 and car["pos"][1] - self.car_pos[1] < 85 and car["pos"][1] - self.car_pos[1] > -85:
                self.lane = self.lane + 70
                return ["SPEED"]
        if scene_info["frame"] > 5 and len(self.car_pos) != 0 and self.lane < self.car_pos[0]:
            return ["MOVE_LEFT", "SPEED"]
        elif scene_info["frame"] > 5 and len(self.car_pos) != 0 and self.lane > self.car_pos[0]:
            return ["MOVE_RIGHT", "SPEED"]
        else:
            return ["SPEED"]

    def reset(self):
        """
        Reset the status
        """
        pass
