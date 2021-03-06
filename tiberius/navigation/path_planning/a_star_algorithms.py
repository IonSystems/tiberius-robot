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


class Astar:
    def __init__(self, control):
        self.control = control
        self.gps = Algorithms(self.control)
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.walls = []
        self.grid_height = 9  # size of the y-axis
        self.grid_width = 9  # size of the x-axis

    def create_walls(self):
        '''
        walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3),  # This is a test array should be filled from sensor data
                 (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))

        this should be filled with database requests for all information about the grid area.
        then any obstacles should be added the the walls array
        '''

        self.walls = [Wall(0, 5, 5), Wall(1, 0, 5), Wall(1, 1, 5), Wall(1, 5, 5), Wall(2, 3, 5), Wall(3, 1, 5),
                 Wall(3, 2, 5), Wall(3, 5, 5), Wall(4, 1, 5), Wall(4, 4, 5), Wall(5, 1, 5)]

        return self.walls

    # need to give the grids there lat and long positions.
    def init_grid(self, startlocation, endlocation):
        walls = self.create_walls()
        # mkae a variable so it relates to the size of the
        bottom_left_location_lat = math.floor(self.grid_height / 2) * 0.00001
        bottom_left_location_lon = math.floor(self.grid_width / 2) * 0.00001
        lat = startlocation[0] - bottom_left_location_lat  # one more than the actual distance as it gets inc'ed first
        lon = startlocation[1] - bottom_left_location_lon  # one more than the actual distance as it gets inc'ed first
        for x in range(self.grid_width):
            lon += 0.00001
            for y in range(self.grid_height):
                wall = self.find_wall(x, y)
                if isinstance(wall, Wall):
                    reachable = wall.accessibility
                else:
                    reachable = 1
                lat += 0.00001

                self.cells.append(Cell(x, y, reachable, lat, lon))

        self.start = self.get_cell(startlocation[0], startlocation[1])
        self.end = self.get_cell(endlocation[0], endlocation[1])

    def get_heuristic(self, cell):
        '''
        compute the heuristic value H for a cell
        distance between this cell anf the end cell multiplied by 10

        :param cell:
        :return heuristic value:
        '''
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def find_wall(self, x, y):
        for wall in self.walls:
            if wall.x == x and wall.y == y:
                return wall
        return False

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
        adj.g = (cell.g + 10) + (cell.reachable * 10)  # better but needs to be tested
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def get_path(self):
        cell = self.end
        path = []
        while cell.parent is not self.start:
            path.append(cell)
            cell = cell.parent
            print 'path: cell: %d, %d, %d. %d' % (cell.x, cell.y, cell.lat, cell.lon)
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
                if adj_cell.reachable < 4 and adj_cell not in self.closed:
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

        grid_height = abs(self.grid_height)
        grid_width = abs(self.grid_width)

        calc_width = 0
        calc_height = 0

        centre_width = math.floor(self.grid_width / 2)
        centre_height = math.floor(self.grid_height / 2)
        startlocation = [centre_width, centre_height]

        if distance < centre_height:
            if 0 < bearing < 180:
                if bearing < 90:
                    calc_width = centre_width + math.floor(distance * math.sin(bearing))
                    calc_height = centre_height + math.floor(distance * math.cos(bearing))
                else:
                    calc_width = centre_width + math.floor(distance * math.sin(180 - bearing))
                    calc_height = centre_height - math.floor(distance * math.cos(180 - bearing))
            else:
                if bearing > -90:
                    calc_width = centre_width - math.floor(distance * math.cos(math.fabs(bearing)))
                    calc_height = centre_height + math.floor(distance * math.cos(math.fabs(bearing)))
                else:
                    calc_width = centre_width - math.floor(distance * math.cos(math.fabs((-180) - bearing)))
                    calc_height = centre_height - math.floor(distance * math.cos(math.fabs((-180) - bearing)))

        else:
            if 0 < bearing < 180:
                if 0 < bearing < 90:
                    if bearing < 45:
                        calc_width = centre_width + math.floor(centre_height * math.tan(math.fabs(bearing)))
                        calc_height = grid_height
                    else:
                        calc_width = grid_width
                        calc_height = centre_height + math.floor(centre_width / math.tan(math.fabs(bearing)))
                else:
                    if bearing < 135:
                        calc_width = grid_width
                        calc_height = centre_height - math.floor(centre_width * math.tan(math.fabs(bearing - 90)))
                    else:
                        calc_width = centre_width + math.floor(centre_height / math.tan(math.fabs(bearing - 90)))
                        calc_height = 0
            else:
                if -90 < bearing < 0:
                    if bearing > -45:
                        calc_width = centre_width - math.floor(centre_height * math.tan(math.fabs(bearing)))
                        calc_height = grid_height
                    else:
                        calc_width = 0
                        calc_height = centre_height + math.floor(centre_width / math.tan(math.fabs(bearing)))
                else:
                    if bearing > -135:
                        calc_width = 0
                        calc_height = centre_height - math.floor(centre_width * math.tan(math.fabs(bearing + 90)))
                    else:
                        calc_width = centre_width - math.floor(centre_height / math.tan(math.fabs(bearing + 90)))
                        calc_height = 0
        endlocation = [calc_width, calc_height]

        return [curlocation, distance, bearing, grid_width, grid_height, startlocation, endlocation]

    @database_grid_update
    def run_astar(self, destination):
        # 0 - curlocation, 1 - distance, 2 - bearing, 3 - grid_width,
        # 4 - grid_height, 5 - startlocation, 6 - endlocation

        destination = format(destination, '.5f')
        grid_values = self.get_grid_data(destination)

        curlocation = grid_values[0]
        distance = grid_values[1]
        bearing = grid_values[2]

        self.grid_width = grid_values[3]
        self.grid_height = grid_values[4]
        startlocation = grid_values[5]
        endlocation = grid_values[6]

        startlocation = format(startlocation, '.5f')
        endlocation = format(endlocation, '.5f')

        # this is where data is read from the database to fill the grid with non reachable locations
        self.create_walls()

        # build the grid using including the walls created by the database data
        self.init_grid(startlocation, endlocation)

        # find a path through the current grid
        self.solve()
        path = self.get_path()
        points = []

        # build points
        for i in range(0, len(path), 1):
            points.append([path[i].lat, path[i].lon])

        self.gps.followPath(points, 50)

        # get the new current location after following the path
        curlocation = format(self.gps.getLocation(), '.5f')

        # check if the destination has been reached.
        if curlocation != destination:
            print 'Current location is : {0}.\nRe-running A-Star to get to Destination : {1}'.format(str(curlocation),
                                                                                                  str(destination))
            self.run_astar(destination)

        print 'A-Star complete, with current location : {0}.\nThe given destination was : {1}'.format(str(curlocation),
                                                                                                  str(destination))

        return


# object that is used to give a wall an accessibility value
class Wall(object):
    def __init__(self, x, y, accessibility):
        self.x = x
        self.y = y
        self.accessibility = accessibility
