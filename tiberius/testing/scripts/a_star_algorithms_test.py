from tiberius.navigation.path_planning.a_star_algorithms import Astar
import sys


a = Astar()

destination = []
destination[0] = sys.argv[1]
destination[1] = sys.argv[2]

a.run_astar(destination)
