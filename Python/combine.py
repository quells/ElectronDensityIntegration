#!/usr/bin/python

import sys, os
import re

rootFolder = '/path/to/csv/files'

sphereFiles = []
linearFiles = []

for root, subFolders, files in os.walk(rootFolder):
	for filename in files:
		filepath = os.path.join(root, filename)
		if filepath.endswith('0_s.csv'):
			if not filepath in sphereFiles:
				sphereFiles.append(filepath)
		elif filepath.endswith('0_z.csv'):
			if not filepath in linearFiles:
				linearFiles.append(filepath)

def match(regex, string):
	return re.search(re.compile(regex), string)

def readTime(filename):
	return filename.split('density')[1].split('_')[0]

spherePoints = []
linearPoints = []
linearRef = []

sphereT, sphereR = [], []
linearT, linearZ = [], []

for dataType in ['sphere', 'linear']:
	for filepath in (sphereFiles if dataType == 'sphere' else linearFiles):
		with open(filepath, 'r') as dataFile:
			time = readTime(filepath)
			(sphereT if dataType == 'sphere' else linearT).append(time)
			px, py, pz = 0, 0, 0
			i = 0
			for line in dataFile.read().split('\n'):
				line = line.split(',')
				pos, esum, cells = 0, 0, 0
				if match('\d\.\d{8}', line[0]):
					(px, py, pz) = line
				elif match('\d\.\d{5}e', line[0]):
					(pos, esum, cells) = line
					if not pos in (sphereR if dataType == 'sphere' else linearZ):
						(sphereR if dataType == 'sphere' else linearZ).append(pos)
					if dataType == 'linear':
						if time == '0000':
							linearRef.append(float(esum))
						linearPoints.append({
							'time': time,
							'px': px, 'py': py, 'pz': pz,
							'pos': pos, 'sum': esum
							# '%.5e'%(float(esum)-linearRef[i])
						})
					else:
						spherePoints.append({
							'time': time,
							'px': px, 'py': py, 'pz': pz,
							'pos': pos, 'sum': esum
						})
					i += 1

for dataType in ['sphere', 'linear']:
	text = dataType
	for r in (sphereR if dataType == 'sphere' else linearZ):
		text += ',%s'%(r)
	for t in (sphereT if dataType == 'sphere' else linearT):
		text += '\n%s'%(t)
		for r in (sphereR if dataType == 'sphere' else linearZ):
			for p in (spherePoints if dataType == 'sphere' else linearPoints):
				if p['time'] == t and p['pos'] == r:
					text += ',%s'%(p['sum'])
	text += '\n'
	print text
