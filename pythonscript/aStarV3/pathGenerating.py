from operator import ge
import numpy as np
from aStarV3 import geofenceband


class Cell:
    def __init__(self):
        self.position = (0, 0)
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, cell):
        return self.position == cell.position

    def showcell(self):
        print(self.position)


class Gridworld:
    def __init__(self, world_size):
        self.w = np.zeros(world_size)
        self.world_x_limit = world_size[0]
        self.world_y_limit = world_size[1]

    def show(self):
        print(self.w)

    def get_neigbours(self, cell):
        neughbourCord = [(-1, -1),(-1, 0),(-1, 1),(0, -1),(0, 1),(1, -1),(1, 0),(1, 1),]
        currentX = cell.position[0]
        currentY = cell.position[1]
        neighbours = []
        for n in neughbourCord:
            x = currentX + n[0]
            y = currentY + n[1]
            if 0 <= x < self.world_x_limit and 0 <= y < self.world_y_limit:
                c = Cell()
                c.position = (x, y)
                c.parent = cell
                neighbours.append(c)
        return neighbours


def astar(world, start, goal, obstacle, geofence):
    """
    Implementation of a start algorithm
    world : Object of the world object
    start : Object of the cell as  start position
    stop  : Object of the cell as goal position
    >>> p = Gridworld()
    >>> start = Cell()
    >>> start.position = (0,0)
    >>> goal = Cell()
    >>> goal.position = (4,4)
    >>> astar(p, start, goal)
    [(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)]
    """
    _open = []
    _closed = []
    _open.append(start)
    # print(obstacle)
    while _open:
        min_f = np.argmin([n.f for n in _open])
        current = _open[min_f]
        _closed.append(_open.pop(min_f))
        # print(current.position)
        if current == goal:
            break
        for n in world.get_neigbours(current):
            for c in _closed:
                if c == n:
                    continue
            x3, y3 = current.position
            x1, y1 = n.position
            x2, y2 = goal.position
            p3 = (x3,y3)
            p1 = (x1,y1)
            p2 = (x2,y2)
            dist =  geofenceband.displacement(p1,p3)
            n.g = current.g + dist
            n.h = (y2 - y1) ** 2 + (x2 - x1) ** 2

            ######OBSTACLE CONDITION########
            for o in range(len(obstacle)):
                ox = obstacle[o][0]
                oy = obstacle[o][1]                
                radiuscheck = ((ox-x1)**2 + (oy-y1)**2)**0.5
                if radiuscheck <= (obstacle[o][2]+5):
                    n.h = 9999999
                    # print("hit obstacle")
                    break

            ######GEOFENCE CONDITION########
            for g in range(len(geofence)):
                if g+1 == len(geofence):
                    pt1 = geofence[g]
                    pt2 = geofence[0]
                else:
                    pt1 = geofence[g]
                    pt2 = geofence[g+1]
                              
                geocheck = geofenceband.geoband(n.position,pt1,pt2)
                if geocheck == False:
                    n.h = 9999999
                    # print("breach geofence")
                    break

            n.f = n.h + n.g

            for c in _open:
                if c == n and c.f < n.f:
                    continue
            _open.append(n)
    path = []
    while current.parent is not None:
        path.append(current.position)
        current = current.parent
    path.append(current.position)
    return path[::-1]

if __name__ == "__main__":
    world = Gridworld((15,15))
    #   stat position and Goal
    start = Cell()
    start.position = (3, 3)
    goal = Cell()
    goal.position = (10, 10)
    # print(f"path from {start.position} to {goal.position}")
    s = astar(world, start, goal, [(7,7,1)], [(0,0),(0,15),(15,15),(15,0)])
    # print(s)
    #   Just for visual reasons
    for i in s:
        world.w[i] = 1
    # print(world.w)