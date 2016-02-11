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

    def init_grid(self):
        walls = self.create_walls()

        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if(x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(self.cell(x, y, reachable))
                self.start = self.get_cell(0, 0)
                self.end = self.get_cell(5, 5)

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
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
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

    def find_end(self, destination):
        curlocation = self.gps.getLocation()
        distance = self.gps.getDistance(curlocation, destination)
        bearing = self.gps.getHeading(curlocation, destination)
        if 45 < bearing < 135:
            grid_height = int(distance * math.sin(bearing))  # not right
            grid_width = int(distance * math.cos(bearing))  # not right
        elif -135 < bearing < -45:
            a = 0
        elif -45 < bearing < 45:
            a = 1
        else:
            a = 2

        return [curlocation, distance, bearing, grid_height, grid_width]

    def run_astar(self, destination):
        grid_values = self.find_end(destination)


        return