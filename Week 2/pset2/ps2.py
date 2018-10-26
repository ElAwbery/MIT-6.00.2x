# 6.00.2x Problem Set 2: Simulating robots


import random

# import ps2_visualize
import pylab

##################
## Comment/uncomment the relevant lines, depending on which version of Python you have
##################

# For Python 3.5:
#from ps2_verify_movement35 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.5 
#import platform
#print("Python version =")
#print(platform.python_version())
# For Python 3.6:
# from ps2_verify_movement36 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.6
import math
import time

import tkinter

class RobotVisualization(object):
    def __init__(self, num_robots, width, height, delay = 0.2):
        "Initializes a visualization with the specified parameters."
        # Number of seconds to pause after each frame
        self.delay = delay

        self.max_dim = max(width, height)
        self.width = width
        self.height = height
        self.num_robots = num_robots

        # Initialize a drawing surface
        self.master = tkinter.Tk()
        self.w = tkinter.Canvas(self.master, width=500, height=500)
        self.w.pack()
        self.master.update()

        # Draw a backing and lines
        x1, y1 = self._map_coords(0, 0)
        x2, y2 = self._map_coords(width, height)
        self.w.create_rectangle(x1, y1, x2, y2, fill = "white")

        # Draw gray squares for dirty tiles
        self.tiles = {}
        for i in range(width):
            for j in range(height):
                x1, y1 = self._map_coords(i, j)
                x2, y2 = self._map_coords(i + 1, j + 1)
                self.tiles[(i, j)] = self.w.create_rectangle(x1, y1, x2, y2,
                                                             fill = "gray")

        # Draw gridlines
        for i in range(width + 1):
            x1, y1 = self._map_coords(i, 0)
            x2, y2 = self._map_coords(i, height)
            self.w.create_line(x1, y1, x2, y2)
        for i in range(height + 1):
            x1, y1 = self._map_coords(0, i)
            x2, y2 = self._map_coords(width, i)
            self.w.create_line(x1, y1, x2, y2)

        # Draw some status text
        self.robots = None
        self.text = self.w.create_text(25, 0, anchor=tkinter.NW,
                                       text=self._status_string(0, 0))
        self.time = 0
        self.master.update()

    def _status_string(self, time, num_clean_tiles):
        "Returns an appropriate status string to print."
        percent_clean = round(100 * num_clean_tiles / (self.width * self.height))
        return "Time: %04d; %d tiles (%d%%) cleaned" % \
            (time, num_clean_tiles, percent_clean)

    def _map_coords(self, x, y):
        "Maps grid positions to window positions (in pixels)."
        return (250 + 450 * ((x - self.width / 2.0) / self.max_dim),
                250 + 450 * ((self.height / 2.0 - y) / self.max_dim))

    def _draw_robot(self, position, direction):
        "Returns a polygon representing a robot with the specified parameters."
        x, y = position.getX(), position.getY()
        d1 = direction + 165
        d2 = direction - 165
        x1, y1 = self._map_coords(x, y)
        x2, y2 = self._map_coords(x + 0.6 * math.sin(math.radians(d1)),
                                  y + 0.6 * math.cos(math.radians(d1)))
        x3, y3 = self._map_coords(x + 0.6 * math.sin(math.radians(d2)),
                                  y + 0.6 * math.cos(math.radians(d2)))
        return self.w.create_polygon([x1, y1, x2, y2, x3, y3], fill="red")

    def update(self, room, robots):
        "Redraws the visualization with the specified room and robot state."
        # Removes a gray square for any tiles have been cleaned.
        for i in range(self.width):
            for j in range(self.height):
                if room.isTileCleaned(i, j):
                    self.w.delete(self.tiles[(i, j)])
        # Delete all existing robots.
        if self.robots:
            for robot in self.robots:
                self.w.delete(robot)
                self.master.update_idletasks()
        # Draw new robots
        self.robots = []
        for robot in robots:
            pos = robot.getRobotPosition()
            x, y = pos.getX(), pos.getY()
            x1, y1 = self._map_coords(x - 0.08, y - 0.08)
            x2, y2 = self._map_coords(x + 0.08, y + 0.08)
            self.robots.append(self.w.create_oval(x1, y1, x2, y2,
                                                  fill = "black"))
            self.robots.append(
                self._draw_robot(robot.getRobotPosition(), robot.getRobotDirection()))
        # Update text
        self.w.delete(self.text)
        self.time += 1
        self.text = self.w.create_text(
            25, 0, anchor=tkinter.NW,
            text=self._status_string(self.time, room.getNumCleanedTiles()))
        self.master.update()
        time.sleep(self.delay)

    def done(self):
        "Indicate that the animation is done so that we allow the user to close the window."
        tkinter.mainloop()

# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y
        
    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)

# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = width
        self.height = height
        # Dictionary keeps track of cleaned tiles. Tiles are keys. If value is True, tile is cleaned. Otherwise, False.
        self.tiles = {}
        
        for horizontal_loc in range(self.width):
            for vertical_loc in range(self.height):
                self.tiles[(horizontal_loc, vertical_loc)] = False
                               
    
    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        horizontal = int(pos.getX())
        vertical = int(pos.getY())
        
        self.tiles[(horizontal, vertical)] = True # Tile has been cleaned, dic value changed.
        
        
    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.tiles[(m, n)] == True
    
    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        clean_tiles = 0
        for tile in self.tiles:
            if self.tiles[tile] == True:
                clean_tiles += 1
        return clean_tiles

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        x = random.uniform(0, self.width)
        y = random.uniform(0, self.height)
        return Position(x, y)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        horizontal_position = math.floor(pos.getX())
        vertical_position = math.floor(pos.getY()) #int function truncates in wrong direction for negatives
        return (horizontal_position, vertical_position) in self.tiles       

# === Problem 2
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        self.speed = speed
        self.position = room.getRandomPosition() # sets initial position, a position object 
        self.direction = random.uniform(0, 360) # sets initial direction, a random angle, a float
        
        room.cleanTileAtPosition(self.position)      

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.position
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.position = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!

# === Problem 3

class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
      
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # assumes robot starts in room
        # sets tile in new position as cleaned
        
        new_position = self.position.getNewPosition(self.direction, self.speed)
        
        if self.room.isPositionInRoom(new_position):
            self.position = new_position
            self.room.cleanTileAtPosition(self.position)
        else:
            self.direction = random.uniform(0, 360)                
    
Roomy = RectangularRoom(5, 7)
Stan = StandardRobot(Roomy, 1.4)
Stan.updatePositionAndClean()
Stan.updatePositionAndClean()
Stan.updatePositionAndClean()
Stan.updatePositionAndClean()
Stan.updatePositionAndClean()
Stan.updatePositionAndClean()
Stan.updatePositionAndClean()
Stan.updatePositionAndClean()
Stan.updatePositionAndClean()

# Uncomment this line to see your implementation of StandardRobot in action!
#testRobotMovement(StandardRobot, RectangularRoom)

# === Problem 4
   
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type):
    """
    Runs num_trials (an int) trials and returns the mean number of
    time_steps needed to clean the fraction min_coverage/room.
    
    The simulation is run with num_robots robots of type robot_type, each with
    speed speed, in a room of dimensions width * height.
    
    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float representing percentage of room to be cleaned
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated, eg: StandardRobot
    """   
   
    results = []
    for trial in range(num_trials):
        # anim = RobotVisualization(num_robots, width, height)
        time_steps = 0
        
        # Instantiate a new room
        room = RectangularRoom(width, height)
        
        # Instantiate the robots
        robots = [robot_type(room, speed) for number in range(num_robots)]
        
        while (room.getNumCleanedTiles()/room.getNumTiles()) < min_coverage:
            time_steps += 1
            # anim.update(room, robots)

            for bot in robots:
                bot.updatePositionAndClean()
            if (room.getNumCleanedTiles()/room.getNumTiles()) >= min_coverage:
                results.append(time_steps)
                
            else:
                continue
        # anim.done()
    # return mean
    return sum(results)/len(results)   
    
# tests   
# num_robots, speed, width, height, min_coverage, num_trials,robot_type
pylab.show()
    
#runSimulation(1, 1.5, 15, 20, 1.0, 1, StandardRobot)  # 150

'''
print(runSimulation(1, 1.0, 10, 10, 0.75, 30, StandardRobot))  # 190
print(runSimulation(1, 1.0, 10, 10, 0.9, 30, StandardRobot))  # 310
print(runSimulation(1, 1.0, 20, 20, 1.0, 70, StandardRobot))  # 3322

print(runSimulation(3, 1.0, 20, 20, 1.0, 70, StandardRobot))   # 1105

print(runSimulation(3, 2.0, 20, 20, 1.0, 70, StandardRobot)) 

print(runSimulation(3, 5.0, 20, 20, 1.0, 70, StandardRobot))    

# tests   
# num_robots, speed, width, height, min_coverage, num_trials,robot_type    
'''    

# === Problem 5
'''
iRobot is testing out a new robot design. The proposed new robots differ in that they change 
direction randomly after every time step, rather than just when they run into walls. 
You have been asked to design a simulation to determine what effect, if any, this change has on 
room cleaning times.

Write a new class RandomWalkRobot that inherits from Robot (like StandardRobot) but implements 
the new movement strategy. RandomWalkRobot should have the same interface as StandardRobot.

Test out your new class. Perform a single trial with the StandardRobot implementation and watch the 
visualization to make sure it is doing the right thing. Once you are satisfied, you can call 
runSimulation again, passing RandomWalkRobot instead of StandardRobot.

'''
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
          
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # assumes robot starts in room
        # sets tile in new position as cleaned
        # chooses random direction
        
        
        new_position = self.position.getNewPosition(self.direction, self.speed)
        
        if self.room.isPositionInRoom(new_position):
            self.position = new_position
            self.room.cleanTileAtPosition(self.position)
            self.direction = random.uniform(0, 360)
        else:
            self.direction = random.uniform(0, 360)
            
# test
runSimulation(1, 1.5, 15, 20, 1.0, 1, StandardRobot)  
# 2399 time-ticks, 299 tiles cleaned, 100% clean
            
print(runSimulation(1, 1.5, 5, 10, 1.0, 1, StandardRobot))
# 304 ticks, code only
# with visuals, 410 ticks
print(runSimulation(1, 1.5, 5, 10, 1.0, 1, RandomWalkRobot))  
# 472 ticks, code only
# with visuals, 537 ticks. Stays local to one area for longer than standard robot. 

print(runSimulation(1, 1.5, 5, 10, 0.9, 1, StandardRobot))
# 222 ticks 
print(runSimulation(1, 1.5, 5, 10, 0.9, 1, RandomWalkRobot))
# 436 ticks 
            
print(runSimulation(1, 1.5, 5, 10, 0.5, 1, StandardRobot))
# 54 ticks, seemed
print(runSimulation(1, 1.5, 5, 10, 0.5, 1, RandomWalkRobot))
# 86 ticks. 

# As the proportion of tiles to be cleaned gets smaller, the standard robot performs relatively quicker.
# The tiles cleaned by randomwalkrobot have more connected edges and are local to each other, whereas
# the tiles cleaned by standard robot are more dispersed. 

# === Problem 6
# NOTE: If you are running the simulation, you will have to close it 
# before the plot will show up.

#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#

def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    
# showPlot1('standard vs. random', 'number of robots', 'time to complete')
        
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()    

showPlot2('standard vs. random', 'aspect ratios', 'time to complete')

