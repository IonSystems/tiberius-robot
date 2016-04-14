'''
TODO
add ability to input start and end cells
add sensor data to grid
create a gui for the website

'''

import heapq

import math

from tiberius.navigation.path_planning.cell import Cell
from tiberius.navigation.gps.algorithms import Algorithms
from tiberius.database.decorators import database_grid_update


class Astar(object):
    def __init__(self):
        self.cell = Cell()
        self.gps = Algorithms()
        self.opened = []
        heapq.heapfiy(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = 6  # size of the y-axis
        self.grid_width = 6  # size of the x-axis

    def create_walls(self):
        walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3),  # This is a test array should be filled from sensor data
                 (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))
        '''
        this should be filled with database requests for all information about the grid area.
        then any obstacles should be added the the walls array
        '''
        return walls

    def init_grid(self, startlocation, endlocation):
        walls = self.create_walls()

        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(self.cell(x, y, reachable))
                self.start = self.get_cell(startlocation)
                self.end = self.get_cell(endlocation)

    def get_heuristic(self, cell):
        '''
        compute the heuristic value H for a cell
        distance between this cell anf the end cell multiplied by 10

        :param cell:
        :return heuristic value:
        '''
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        '''
        returns a cell by using the x and y coordinates to find it in the array cells
        :param x:
        :param y:
        :return:
        '''
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        '''
        Returns adjacent cells to a cell. Clockwise starting
        from the one on the right.

        @param cell get adjacent cells for this cell
        @returns adjacent cells list
        '''
        cells = []
        if cell.x < self.grid_width - 1:
            cells.append(self.get_cell(cell.x + 1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y - 1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x - 1, cell.y))
        if cell.y < self.grid_height - 1:
            cells.append(self.get_cell(cell.x, cell.y + 1))
        return cells

    def display_path(self):
        cell = self.end
        while cell.parent is not self.start:
            cell = cell.parent
            print 'path: cell: %d,%d' % (cell.x, cell.y)

    def update_cell(self, adj, cell):
        """
        Update adjacent cell

        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def get_path(self):
        cell = self.end
        path = []
        while cell.parent is not self.start:
            path.append(cell)
            cell = cell.parent
            print 'path: cell: %d, %d' % (cell.x,cell.y)
        return path

    def solve(self):
        """Solve maze, find path to ending cell.
        @returns path or None if not found.
        """
        # add starting cell to open heap queue
        heapq.heappush(self.opened, (self.start.f, self.start))
        while len(self.opened):
            # pop cell from heap queue
            f, cell = heapq.heappop(self.opened)
            # add cell to closed list so we don't process it twice
            self.closed.add(cell)
            # if ending cell, return found path
            if cell is self.end:
                return self.get_path()
            # get adjacent cells for cell
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        # if adj cell in open list, check if current path is
                        # better than the one previously found
                        # for this adj cell.
                        if adj_cell.g > cell.g + 10:
                            self.update_cell(adj_cell, cell)
                    else:
                        self.update_cell(adj_cell, cell)
                        # add adj cell to open list
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))

    def get_grid_data(self, destination):
        curlocation = self.gps.getLocation()

        distance = self.gps.getDistance(curlocation, destination)
        bearing = self.gps.getHeading(curlocation, destination)

        grid_height = int(distance * math.sin(bearing))
        grid_width = int(distance * math.cos(bearing))

        grid_height = abs(grid_height)
        grid_width = abs(grid_width)

        startlocation = (0, 0)
        endlocation = (grid_width, grid_height)

        if 0 < bearing < 180:
            if bearing < 90:  # less than 90 so between 0 and 90
                startlocation = (0, 0)
                endlocation = (grid_width, grid_height)
            else:  # more than 90 so between 90 and 180
                startlocation = (0, grid_height)
                endlocation = (grid_width, 0)
        elif -180 < bearing < 0:
            if bearing > -90:  # more than -90 so between 0 and -90
                startlocation = (grid_width, 0)
                endlocation = (0, grid_height)
            else:  # between -90 and -180
                startlocation = (grid_width, grid_height)
                endlocation = (0, 0)

        return [curlocation, distance, bearing, grid_width, grid_height, startlocation, endlocation]

    @database_grid_update
    def run_astar(self, destination):
        # 0 - curlocation, 1 - distance, 2 - bearing, 3 - grid_width, 4 - grid_height, 5 - startlocation, 6 - endlocation
        grid_values = self.get_grid_data(destination)

        curlocation = grid_values[0]
        distance = grid_values[1]
        bearing = grid_values[2]

        self.grid_width = grid_values[3]
        self.grid_height = grid_values[4]
        startlocation = grid_values[5]
        endlocation = grid_values[6]

        # this is where data is read from the database to fill the grid with non reachable locations
        self.create_walls()

        # build the grid using including the walls created by the database data
        self.init_grid(startlocation, endlocation)

        # find a path through the current grid
        self.solve()
        path = self.get_path()

        self.gps.pointToPoint()
        # need loop to update and get to end
        return
