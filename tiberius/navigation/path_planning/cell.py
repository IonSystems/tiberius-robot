'''
cell object that is used to create the grid for the A* algorithm.

'''
class Cell(object):
    def __init__(self, x, y, reachable, lat, lon):
        '''
        Initialize new cell

        @param x cell x coordinate
        @param y cell y coordinate
        @param reachable is cell reachable? not a wall?
        '''
        self.reachable = reachable  # is the cell reachable - True or False
        self.x = x  # cell x-axis value
        self.y = y  # cell y-axis value
        self.parent = None  # the cell before this one in the path
        self.g = 0  # cost of moving from the starting cell
        self.h = 0  # the heuristic value of the cell
        self.f = 0  # the final cost of the cell
        self.lat = lat  # the latitude position of the cell
        self.long = lon  # the longitude position of the cell
