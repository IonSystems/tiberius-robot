from tiberius.navigation.gps.algorithms import Algorithms
import sys

g = Algorithms()
long = sys.argv[0]
lat = sys.argv[1]
g.pointToPoint([long, lat])
