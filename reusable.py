#!/usr/bin/python

import sys

def findAl(filename):
	"""
	Takes 1 argument, a filename for a `.cub` file.
	Finds just the number of atoms, the positions of non-hydrogen atoms (aluminum in this case), and supercell dimension information.
	Returns: a tuple containing this information.

	Use `parseFile()` instead if information about the projectile is required.
	"""
	numAtoms, dimensions, resolution, alPositions = 0, [], [], []
	print 'Parsing %s'%(filename)
	allValues = []
	with open(filename) as file:
		n = 0
		for line in file.readlines():
			n += 1
			line = line.strip('\n').split(' ')
			if n < 3:
				continue
			elif n < 4:
				numAtoms = int(line[0])
			elif n < 7:
				dimensions.append(int(line[0]))
				resolution.append(float(line[n-3]))
			elif n < 7 + numAtoms:
				if line[0] == '1':
					continue
				else:
					al = []
					for i in [2, 3, 4]:
						al.append(float(line[i]))
					alPositions.append(al)
			else:
				continue
	return (numAtoms, dimensions, resolution, alPositions)

def parseFile(filename):
	"""
	Takes 1 argument, a filename for a `.cub` file.
	Finds the number of atoms, electron density data, hydrogen position, the positions of non-hydrogen atoms (aluminum in this case), and supercell dimension information.
	Returns: a tuple containing this information.

	Use `findAl()` if only information about the aluminum is required, or if there is no projectile.
	"""
	numAtoms, dimensions, resolution, data, protonPosition, alPositions = 0, [], [], [], [], []

	# count the number of atoms, read the dimensions of the supercell and its resolution,
	# read the locations of each atom, and combine electron density information into a single array
	print 'Parsing %s'%(filename)
	allValues = []
	with open(filename) as file:
		n = 0
		for line in file.readlines():
			n += 1
			line = line.strip('\n').split(' ')
			if n < 3:
				continue
			elif n < 4:
				numAtoms = int(line[0])
			elif n < 7:
				dimensions.append(int(line[0]))
				resolution.append(float(line[n-3]))
			elif n < 7 + numAtoms:
				if line[0] == '1':
					for i in [2, 3, 4]:
						protonPosition.append(float(line[i]))
				else:
					al = []
					for i in [2, 3, 4]:
						al.append(float(line[i]))
					alPositions.append(al)
			else:
				allValues += [float(f) for f in line[:-1]]

	# the volume of each cell, since values in the source file are electrons/volume
	dV = resolution[0]*resolution[1]*resolution[2]

	# organize single array into nested arrays
	# serializing and deserializing this data is at least 2x slower than generating it each run
	for x in range(dimensions[0]):
		data.append([])
		for y in range(dimensions[1]):
			data[x].append([])
			for z in range(dimensions[2]):
				data[x][y].append([])
				data[x][y][z] = allValues[x*dimensions[1]*dimensions[2] + y*dimensions[2] + z]

	return (numAtoms, dimensions, resolution, dV, data, protonPosition, alPositions)

def distanceBetween(a, b):
	if not len(a) == len(b):
		print 'error - unequal vector lengths'
		sys.exit()
	d = 0
	for i in range(len(a)):
		d += (a[i]-b[i])**2
	return d**0.5