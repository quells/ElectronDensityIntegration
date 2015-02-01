#!/usr/bin/python

import optparse
import sys
import os

from reusable import parseFile, distanceFromProton
import math


parser = optparse.OptionParser(description='Search for artifacts in secondary electron emission data.', usage='%prog filename')
(options, args) = parser.parse_args()
filename = args[0]
args = options

(numAtoms, dimensions, resolution, dV, data, protonPosition, alPositions) = parseFile(filename)

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

outputFilename = os.path.splitext(filename)[0] + '_shadow.csv'

zmin = 0
zmax = dimensions[2]

shadowData = []
# for y in range(dimensions[1]):
for z in range(zmin, zmax):
	line = []
	for x in range(dimensions[0]):
		value = 0
		# for z in range(zmin, zmax):
		for y in range(ymin, ymax):
			if z >= dimensions[2]:
				z -= dimensions[2]
			try:
				value += data[x][y][z]*dV/resolution[2]
			except IndexError:
				print x, y, z
				sys.exit()
		line.append(math.log(value, 10))
	shadowData.append(line)

outputString = 'protonPosition,%.3e,%.3e,%.3e\n'%(protonPosition[0], protonPosition[1], protonPosition[2])
outputString += 'z\\x,' + ','.join(['%.3e'%(x*resolution[0]) for x in range(dimensions[0])])
i = 0
for yData in shadowData:
	outputString += '\n%.3e,'%(i*resolution[2]) + ','.join(['%.3e'%(xDatum) for xDatum in yData])
	i += 1

with open(outputFilename, 'w') as f:
	f.write(outputString)