from tiberius.control.control import Control
from tiberius.navigation.path_planning.a_star_algorithms import Astar
import sys

control = Control()
a = Astar(control)

destination = []
destination[0] = sys.argv[1]
destination[1] = sys.argv[2]

a.run_astar(destination)
