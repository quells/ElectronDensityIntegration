#!/usr/bin/python

import optparse
import sys
import os

from reusable import parseFile, distanceBetween

'''Parse command line arguments'''
int_desc = 'Integrate electron density simulation results with respect to distance. Specialized options exist for handling projectiles and aluminum sheets.'
int_usage = 'usage: %prog [options] filename'
parser = optparse.OptionParser(description=int_desc, usage=int_usage)
parser.add_option('-r', '--radius', dest='maxRange', type=int, default=None, help='maximum radius for spherical integration in Bohr radii')

intType = optparse.OptionGroup(parser, 'Integration Type')
intType.add_option('-s', '--spherical', action='store_true', help='Integrate spherically around a hydrogen projectile. Only suitable for simulations with such a projectile.')
intType.add_option('-l', '--linear', action='store_true', help='Integrate linearly along the entire supercell. Requires a direction input. z is typically the most useful.')

linIntDir = optparse.OptionGroup(parser, 'Linear Integration Direction')
linIntDir.add_option('-x', action='store_true')
linIntDir.add_option('-y', action='store_true')
linIntDir.add_option('-z', action='store_true')

parser.add_option_group(intType)
parser.add_option_group(linIntDir)
(options, args) = parser.parse_args()

'''Fail if command line arguments are invalid, see `README.md`'''
try:
	filename = args[0]
except IndexError:
	print 'error - No file selected.'
	sys.exit()
args = options

if args.spherical == None and args.linear == None:
	print 'error - No integration method selected.'
	sys.exit()

if args.linear == True:
	if args.spherical == True:
		print 'error - Select only one integration method.'
		sys.exit()
	num_linear_options = sum([1 if not d == None else 0 for d in [args.x, args.y, args.z]])
	if num_linear_options == 0:
		print 'error - Select a linear integration direction.'
		sys.exit()
	elif num_linear_options > 1:
		print 'error - Select only one linear integration direction.'
		sys.exit()

'''Read data from file using `reusable.py`'''
(numAtoms, dimensions, resolution, dV, data, protonPosition, alPositions) = parseFile(filename)

'''Output will be a CSV table'''
outputString = 'hydrogen position (Bohr radii),,\n'
outputString += 'x,y,z\n'
outputString += ','.join(['%.8f'%(i) for i in protonPosition]) + '\n'
outputString += ',,\n'

if args.spherical:
	outputFilename = os.path.splitext(filename)[0] + '_s.csv'

	effectiveRes = resolution[dimensions.index(min(dimensions))]
	maxRange = min(dimensions)/2
	# If a maximum range is given, use that.
	if not args.maxRange == None:
		# Convert args.maxRange from 'real space' to 'index space'
		maxRange = int(args.maxRange/effectiveRes)
	# If there are aluminum atoms close to the projectile, do not integrate into the aluminum
	for al in alPositions:
		# Convert a from 'real space' to 'index space'
		a = int(distanceBetween(protonPosition, al)/effectiveRes)
		maxRange = min(maxRange, a)

	px, py, pz = protonPosition
	sums = []
	# Convert protonPosition from 'real space' to 'index space'
	px = int(px/resolution[0]); py = int(py/resolution[1]); pz = int(pz/resolution[2]);

	outputString += 'radius,sum,cells\n'

	for r in range(1, maxRange+1):
		eSum = 0
		numCells = 0.0
		outputString += '%.5e,'%(r*effectiveRes)
		dx = [px-r-1, px+r+1]; dy = [py-r-1, py+r+1]; dz = [pz-r-1, pz+r+1];

		for x in range(dx[0], dx[1]):
			if x >= dimensions[0]:
				x -= dimensions[0]
			for y in range(dy[0], dy[1]):
				if y >= dimensions[1]:
					y -= dimensions[1]
				for z in range(dz[0], dz[1]):
					if z >= dimensions[2]:
						z -= dimensions[2]
					distance = distanceBetween(protonPosition, [x*resolution[0], y*resolution[1], z*resolution[2]])
					radius = r*effectiveRes
					if distance <= radius:
						try:
							eSum += data[x][y][z]*dV
							numCells += 1
						except IndexError:
							print 'error - index out of range'
							print 'attempting to access [%i, %i, %i] with radius %i-indices when size of supercell is [%i, %i, %i]'%(x, y, z, r, len(data), len(data[x]), len(data[x][y]))
							sys.exit()
		print '%i / %i, %.2e cells summed to %.5e'%(r, maxRange, numCells, eSum)
		outputString += '%.5e,%.5e\n'%(eSum, numCells)

	with open(outputFilename, 'w') as f:
		f.write(outputString)
elif args.linear:
	direction = 'x' if args.x else 'y' if args.y else 'z'
	outputFilename = os.path.splitext(filename)[0] + '_' + direction + '.csv'

	outputString += direction + ',sum,cells\n'

	# Handles integration direction
	ni, nj, nk = 0, 0, 0
	if args.x:
		ni, nj, nk = dimensions[0], dimensions[1], dimensions[2]
	elif args.y:
		ni, nj, nk = dimensions[1], dimensions[2], dimensions[0]
	else:
		ni, nj, nk = dimensions[2], dimensions[1], dimensions[0]
	ni, nj, nk = int(ni), int(nj), int(nk)

	for i in range(0, ni):
		eSum = 0
		numCells = 0.0
		outputString += '%.5e,'%(i*resolution[0 if args.x else 1 if args.y else 2])
		for j in range(0, nj):
			for k in range(0, nk):
				try:
					eSum += data[i if args.x else k if args.y else k][j if args.x else i if args.y else j][k if args.x else j if args.y else i]*dV
				except IndexError:
					print 'error - index out of range'
					print [i, j, k], dimensions
					sys.exit()
				numCells += 1
		print '%i / %i, %.2e cells summed to %.5e'%(i+1, ni, numCells, eSum)
		outputString += '%.5e, %.5e\n'%(eSum, numCells)

	with open(outputFilename, 'w') as f:
		f.write(outputString)
