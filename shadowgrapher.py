#!/usr/bin/python

import optparse
import sys
import os

import math

import matplotlib.pyplot as plt
from matplotlib import cm, axes
import numpy as np

parser = optparse.OptionParser(description='Search for artifacts in secondary electron emission data.')
(options, args) = parser.parse_args()
filename = args[0]
args = options

x, y = [], []
data = []
with open(filename) as f:
	n = 0
	for line in f.readlines():
		if n < 1:
			n += 1
			continue
		elif n == 1:
			x = [float(x) for x in line.split(',')[1:]]
		else:
			line = line.split(',')
			y.append(float(line[0]))
			data.append([math.log(float(d), 10) for d in line[1:]])
		n += 1
time = filename.split('y')[-1].split('_')[0]

scale = 50.0
fig = plt.figure(figsize=(len(x)/scale*1.25, len(y)/scale), dpi=100)
# print len(x)/scale
# spacing = 3.6/20
# plt.subplots_adjust(left=spacing, right=(1-spacing))
CS = plt.contour(x, y, data, levels=np.linspace(-2, -7, 26), cmap=cm.jet)
plt.xlabel('x (a_B)')
plt.ylabel('z (a_B)')
plt.title('Electron distribution at t=%s'%(time))
CB = plt.colorbar(CS, extend='both')
CB.ax.set_ylabel('log (# electrons)')
plt.savefig(filename.split('.')[0] + '.png')
# plt.show()