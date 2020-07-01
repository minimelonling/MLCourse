# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:46:24 2020

@author: Dining
"""

import pickle
import os
import numpy as np
from sklearn.tree import DecisionTreeRegressor  
from sklearn.neural_network import MLPClassifier
from sklearn import tree
from sklearn import metrics
from sklearn.model_selection import train_test_split

path = os.getcwd()
path = os.path.join(path,"games","RacingCar","log")

allFile = os.listdir(path) # load log file
data_set = []

for file in allFile:
    with open(os.path.join(path,file),"rb") as f:
        data_set.append(pickle.load(f)) # load data in data_set

x = np.array([1,2,3,4,5,6,7,8,9])  # feature of nine grid information
y = np.array([0]) # label

#        9 grid relative position
#        |    |    |    |
#        |  1 |  2 |  3 |
#        |    |  5 |    |
#        |  4 |  c |  6 |
#        |    |    |    |
#        |  7 |  8 |  9 |
#        |    |    |    |   

for data in data_set: 
    lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]
    PlayerCar_x = []  
    PlayerCar_y = []
    Activity = [] # the label which we give it
    ComputerCar_lane = [] # feature : to record the computer car x
    for scene_info in data["scene_info"][1::]: # start from the frame 1 
        grid = set()     
        ComputerCarDif_x = []
        ComputerCarDif_y = []
        ComputerCar_x = []
        ComputerCar_y = []
        speed_ahead = []
        for car in scene_info["cars_info"]:
            if car["id"] == 0:  # the player's car information          
                PlayerCar_x.append(car["pos"][0])
                PlayerCar_y.append(car["pos"][1])
                p_x = car["pos"][0]
                p_y = car["pos"][1]
                p_v = car["velocity"]
                self_lane = car["pos"][0]//70
                if p_x <= 65:
                    grid.add(1)
                    grid.add(4)
                    grid.add(7)
                elif p_x >= 565:
                    grid.add(3)
                    grid.add(6)
                    grid.add(9)
            else:
                ComputerCar_x.append(car["pos"][0])
                ComputerCar_y.append(car["pos"][1])
                ComputerCarDif_x.append(car["pos"][0]-p_x)
                ComputerCarDif_y.append(car["pos"][1]-p_y)
                speed_ahead.append(car["velocity"])
        
        for i in range(len(ComputerCarDif_x)):          
            if ComputerCarDif_x[i] <= 40 and ComputerCarDif_x[i] >= -40 :      
                if ComputerCarDif_y[i] > 0 and ComputerCarDif_y[i] < 300:
                    grid.add(2)

                    if ComputerCarDif_y[i] < 200:
                        speed_aheadcar = speed_ahead[i] 
                        grid.add(5)

                elif ComputerCarDif_y[i] < 0 and ComputerCarDif_y[i] > -200:
                    grid.add(8)

            if ComputerCarDif_x[i] > -100 and ComputerCarDif_x[i] < -40 :
                if ComputerCarDif_y[i] > 80 and ComputerCarDif_y[i] < 250:
                    grid.add(3)

                elif ComputerCarDif_y[i] < -80 and ComputerCarDif_y[i] > -200:
                    grid.add(9)

                elif ComputerCarDif_y[i] < 80 and ComputerCarDif_y[i] > -80:
                    grid.add(6)

            if ComputerCarDif_x[i] < 100 and ComputerCarDif_x[i] > 40:
                if ComputerCarDif_y[i] > 80 and ComputerCarDif_y[i] < 250:
                    grid.add(1)

                elif ComputerCarDif_y[i] < -80 and ComputerCarDif_y[i] > -200:
                    grid.add(7)

                elif ComputerCarDif_y[i] < 80 and ComputerCarDif_y[i] > -80:
                    grid.add(4)

        if len(grid) == 0:
                Activity.append(0)  # return ["SPEED"]
        else:
            if (2 not in grid): # Check forward 
                # Back to lane center
                if p_x > lanes[self_lane]:
                    Activity.append(1)  # return ["SPEED", "LEFT"]
                elif p_x < lanes[self_lane]:
                    Activity.append(2)  # return ["SPEED", "MOVE_RIGHT"]
                else :
                    Activity.append(0)  # return ["SPEED"]
            else:

                if (p_x < 60 ):
                    Activity.append(2)  # return ["SPEED", "MOVE_RIGHT"]
                elif (1 not in grid) and (4 not in grid) and (7 not in grid): # turn left 
                    Activity.append(1)  # return ["SPEED", "LEFT"]
                elif (3 not in grid) and (6 not in grid) and (9 not in grid): # turn right
                    Activity.append(2)  # return ["SPEED", "MOVE_RIGHT"]
                elif (1 not in grid) and (4 not in grid): # turn left 
                    Activity.append(1)  # return ["SPEED", "LEFT"]
                elif (3 not in grid) and (6 not in grid): # turn right
                    Activity.append(2)  # return ["SPEED", "MOVE_RIGHT"]
                elif (4 not in grid) and (7 not in grid): # turn left 
                    Activity.append(6)   # return [LEFT"]
                elif (6 not in grid) and (9 not in grid): # turn right
                    Activity.append(7)  # return ["RIGHT"]
                elif (5 in grid):  # NEED to BRAKE
                    if (4 not in grid) and (7 not in grid): # turn left 
                        if p_v < speed_aheadcar:
                            Activity.append(1)  # return ["SPEED", "LEFT"]
                        else:
                            Activity.append(4)  # return ["BRAKE", "LEFT"]
                    elif (6 not in grid) and (9 not in grid): # turn right
                        if p_v < speed_aheadcar:
                            Activity.append(2)  # return ["SPEED", "MOVE_RIGHT"]
                        else:
                            Activity.append(5)  # return ["BRAKE", "RIGHT"]
                    else : 
                        if p_v < speed_aheadcar:  # BRAKE
                            Activity.append(0)  # return ["SPEED"]
                        else: 
                            Activity.append(3)  # return ["BRAKE"]
            
        grid_data = [0,0,0,0,0,0,0,0,0]
        grid_tolist = list(grid)
        for i in grid_tolist:
            grid_data[i-1] = 1  # change grid set into feature's data shape
        grid_data = np.array(grid_data).reshape(1,9)

        x = np.vstack((x.reshape(-1,9), np.hstack(grid_data)))
    y = np.hstack((y, np.array(Activity)))
    # stack the feature and label


x = x[1::] #remove [1, 2, 3, 4, 5, 6, 7, 8, 9]
y = y[1::] #remove [0]

x_train , x_test,y_train,y_test = train_test_split(x,y,test_size=0.2)

model = tree.DecisionTreeClassifier() 
model.fit(x_train, y_train)    

y_predict = model.predict(x_test)
print(y_predict)
accuracy = metrics.accuracy_score(y_test, y_predict)
print("Accuracy(正確率) ={:8.3f}%".format(accuracy*100))        
    
with open('games/RacingCar/ml/save/decisiontreemodel.pickle', 'wb') as f:
    pickle.dump(model, f)             
    