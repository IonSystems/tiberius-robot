from tiberius.navigation.gps.algorithms import Algorithms
import sys

g = Algorithms()

algo = sys.argv[1]
latitude = []
longitude = []

check = 1
speedpercent = 50

points = []
j = 0

'''
latitude = sys.argv[1]
longitude = sys.argv[2]
g.pointToPoint([latitude,longitude], check, speedpercent)
'''
# try:
for i in range(2, sys.argv.__len__()-3, 2):
	latitude.append(sys.argv[i])
	longitude.append(sys.argv[i+1])
	points.append([latitude[j], longitude[j]])
	j += 1

check = int(sys.argv[sys.argv.__len__()-2])
speedpercent = int(sys.argv[sys.argv.__len__()-1])

print 'Check: ' + str(check)
print 'Speed: ' + str(speedpercent)
print 'lat: ' + str(latitude)
print 'long: ' + str(longitude)
print 'Points: ' + str(points)

if algo is '0':
	g.pointToPoint([latitude[0], longitude[0]], check, speedpercent)
elif algo is '1':
	g.followPath(points, check, speedpercent)
'''except:
    print "Well that didn't quite go to plan!!!"
    print 'Did you run this script correctly?'
    print 'Hmmm maybe I can help you out with that, being a supreme being and all!'
    print 'Try using this format:'
    print 'python test_gps_algorithms.py algo lat1 long1 lat2 long2 ... check speedpercent'
    print '\n'
    print 'The algo argument is used to select which algorithm is being tested:'
    print '0 - pointToPoint, 1 - followPath'
    print 'The number of lat and long values is up to you but they must have the same number of values and'
    print 'If you select pointToPoint then the code will only consider the first values'
    print 'The check argument is the number of meters between each check on if tiberius is going to the right place'
    print 'And finally speedpercent is the speed percentage of tiberius, hint its a percentage so between 0 and 100 :)'
    print 'I hope you found this to be helpful but if not then there is no hope for you :('
'''