#!/usr/bin/python

import optparse
import sys
import os

from reusable import parseFile
import math

'''Parse command line arguments'''
parser = optparse.OptionParser(description='Search for artifacts in secondary electron emission data.', usage='%prog filename')
(options, args) = parser.parse_args()
try:
	filename = args[0]
except IndexError:
	print 'error - No file selected.'
	sys.exit()
args = options

'''Read data from file using `reusable.py`'''
(numAtoms, dimensions, resolution, dV, data, protonPosition, alPositions) = parseFile(filename)

'''Default to the center of the cube; if a proton is present, center on that.'''
ymin = dimensions[1]/2
ymax = ymin + 1
if len(protonPosition) > 0:
	# Convert protonPosition from 'real space' to 'index space'
	px, py, pz = protonPosition
	px = int(px/resolution[0]); py = int(py/resolution[1]); pz = int(pz/resolution[2]);
	# Center y-slice on the proton
	ymin = py - 1
	ymax = py + 1

# what the output should look like
#  x ->
# y 000000000000000000000000000000
# | 000000333300000000000000000000
# V 000003344330000000000000000000
#   000033444433000000000000000000
#   000334455443300000000000000000
#   000334455443300000000000000000
#   000033444433000000000000000000
#   000003344330000000000000000000
#   000000333300000000000000000000
#   000000000000000000000000000000
#   000000000000000000000000000000

'''Output will be a CSV table'''
outputFilename = os.path.splitext(filename)[0] + '_shadow.csv'

'''Go through `data` and read the sliced data into a new array'''
shadowData = []
for z in range(dimensions[2]):
	line = []
	for x in range(dimensions[0]):
		value = 0
		for y in range(ymin, ymax):
			if z >= dimensions[2]:
				z -= dimensions[2]
			try:
				value += data[x][y][z]*dV/resolution[2]
			except IndexError:
				print 'Index Error'
				print x, y, z
				sys.exit()
		line.append(math.log(value, 10))
	shadowData.append(line)

'''Write to CSV file'''
outputString = 'protonPosition,%.3e,%.3e,%.3e\n'%(protonPosition[0], protonPosition[1], protonPosition[2])
outputString += 'z\\x,' + ','.join(['%.3e'%(x*resolution[0]) for x in range(dimensions[0])])
i = 0
for yData in shadowData:
	outputString += '\n%.3e,'%(i*resolution[2]) + ','.join(['%.3e'%(xDatum) for xDatum in yData])
	i += 1

with open(outputFilename, 'w') as f:
	f.write(outputString)