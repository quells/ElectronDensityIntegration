#!/usr/bin/python

import optparse
from matplotlib import pyplot as plt
import numpy as np
import sys
import math

parser = optparse.OptionParser(description='Graph combined electron data', usage='usage: %prog filename')
(options, args) = parser.parse_args()

'''Fail if command line arguments are invalid, see `README.md`'''
try:
	filename = args[0]
except IndexError:
	print 'No file specified.'
	sys.exit()

ref = []
times = []
distances = []
values = []
modeIsLinear = False
with open(filename) as file:
	for line in file.readlines():
		if modeIsLinear:
			if line.startswith('0000'):
				ref = [float(i) for i in line.split(',')[1:]]
			else:
				try:
					line = [float(i) for i in line.split(',')]
				except ValueError:
					break
				times.append(line[0])
				values.append(line[1:])
		else:
			if line.startswith('spherical'):
				continue
			elif line.startswith('linear'):
				modeIsLinear = True
				distances = [float(i) for i in line.split(',')[1:]]

# values looks like
# [    z: 0.217, 0.434, ...
#   ...
# 	4000: [... ,],
# 	4200: [... ,],
# 	...
# ]

# figure out where the Al sheet ends
i = 0
al = []
for v in ref:
	if v/max(ref) > 0.95:
		al.append(i)
	i += 1
firstAl = min(al)
lastAl = max(al)

res = []
for z in distances:
	if distances.index(z) > 0:
		res.append(z - distances[distances.index(z)-1])
res = sum(res)/len(res)

# arbitrarily avoid integrating within n a_B of the Al sheet
n = 10
startIndex = firstAl-int(n/res)
endIndex = lastAl+int(n/res)
print filename
print distances[startIndex], distances[endIndex]

seeBack = [sum(ref[:startIndex])]
seeForward = [sum(ref[endIndex:])]
seeCombined = [seeBack[0] + seeForward[0]]
for v in values:
	seeBack.append(sum(v[:startIndex]))
	seeForward.append(sum(v[endIndex:]))
	seeCombined.append(sum(v[:startIndex]) + sum(v[endIndex:]))

times = [0]+times

# plt.scatter(times, seeBack, color='#0000ff')
# plt.scatter(times, seeForward, color='#ff0000')
plt.scatter(times, seeCombined, color='#a000a0')
# plt.plot(times, seeBack, label='before sheet', color='#0000ff')
# plt.plot(times, seeForward, label='after sheet', color='#ff0000')
# plt.plot(times, seeCombined, label='combined', color='#a000a0')
plt.plot(times, seeCombined, color='#a000a0', label='max: %.2e'%(max(seeCombined)))
plt.axis([0, max(times), 0, 4.0]) # max(seeCombined)*1.1
plt.xlabel('time')
plt.ylabel('total electrons %i a_B outside the Al sheet'%(n))
plt.title(filename.split('.')[0])
# plt.title('Secondary Electron Emission')
plt.legend(loc='best')
# plt.show()
plt.savefig(filename.split('.')[0]+'.png')
plt.clf()