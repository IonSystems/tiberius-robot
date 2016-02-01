from tiberius.navigation.gps.algorithms import Algorithms
import sys

g = Algorithms()
long = sys.argv[1]
lat = sys.argv[2]
g.pointToPoint([long, lat], 4, 50)
