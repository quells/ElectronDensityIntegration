#!/usr/bin/python
# -*- coding: utf-8 -*-

import optparse
from matplotlib import pyplot as plt
import numpy as np
import sys

parser = optparse.OptionParser(description='Graph combined electron data')
(options, args) = parser.parse_args()

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
				times.append(float(line[0])/1000)
				values.append(line[1:])
		else:
			if line.startswith('spherical'):
				continue
			elif line.startswith('linear'):
				modeIsLinear = True
				distances = [float(i) for i in line.split(',')[1:]]
				# distances *0.529 for Å

corrected_values = []
for i in range(len(values)):
	temp = []
	for j in range(len(ref)):
		temp.append(values[i][j] - ref[j])
	corrected_values.append(temp)

colors = ['#ff0000', '#ff8000', '#ffff00', '#80ff00', '#00ff00', '#00ff80', '#00ffff', '#0080ff', '#0000ff', '#8000ff', '#ff00ff', '#ff0080']
# colors += ['#800000', '#804000', '#808000', '#408000', '#008000', '#008040', '#008080', '#004080', '#000080', '#400080', '#800080', '#800040']
# colors = ['#ff0000', '#ff4000', '#ff8000', '#ffc000', '#ffff00', '#c0ff00', '#80ff00', '#40ff00', '#00ff00', '#00ff40', '#00ff80', '#00ffc0', '#00ffff', '#00c0ff', '#0080ff', '#0040ff', '#0000ff', '#4000ff', '#8000ff', '#c000ff', '#ff00ff', '#ff00c0', '#ff0080', '#ff0040']

def polyfit(x, y, degree):
	results = {}
	coeffs = np.polyfit(x, y, degree)
	results['polynomial'] = coeffs.tolist()
	formula = np.poly1d(coeffs)
	results['formula'] = formula
	correlation = np.corrcoef(x, y)[0,1]
	results['correlation'] = correlation
	results['determination'] = correlation**2
	return results

def parsePolynomial(f, y = u'y', x = u'x'):
	coeffs = f['polynomial']
	formula = y + u' = '
	for c in coeffs:
		i = coeffs.index(c)
		n = len(coeffs) - i - 1
		if i > 0 and c > 0:
			formula += u' + '
		else:
			formula += u' '
		if n > 1:
			formula += u'%.2e %s^%i'%(c, x, n)
		elif n == 1:
			formula += u'%.2e %s'%(c, x)
		else:
			formula += u'%.2e'%(c)
	formula += u'\nR² = %.4f'%(f['determination'])
	return formula

# print len(corrected_values[0])
# for i in range(len(times)):
# 	print times[i], sum(corrected_values[i])
# sys.exit()

print '%i electrons in cell'%sum(ref)

drift = polyfit(times, [sum(i) for i in corrected_values], 2)
x = np.linspace(min(times), max(times))
plt.scatter(times, [sum(i) for i in corrected_values])
plt.plot(x, drift['formula'](x))

# lindrift = polyfit(times[0:2], [sum(i) for i in corrected_values[0:2]], 1)
# plt.plot(x, lindrift['formula'](x), linestyle='--', color='#000000')

plt.text(3000, drift['formula'](2000), parsePolynomial(drift, u'∆e', 't'))
plt.xlabel('time (atomic units)')
plt.ylabel('increase in total # electrons')
plt.title('Drift in electron number over time')
# plt.title('Drift in electron number in ' + filename.split('.')[0] + '\n')
plt.show()
plt.clf()
# sys.exit()

distances = [d*0.529 for d in distances]
for v in corrected_values:
	i = corrected_values.index(v)
	plt.plot(distances, v, color=colors[i], label='t = %.1f'%(times[i]))
plt.plot(distances, [i/max(ref)*max(corrected_values[4])/2 for i in ref], color='#000000', linestyle='--', label='Reference')
plt.xlabel(u'z (Å)')
plt.ylabel('Change in # Electrons (Relative to Reference)')
plt.title('Distribution of Integration Error')
# plt.title('Distribution of electron drift in ' + filename.split('.')[0] + '\n')
plt.legend()
# plt.axis([40, 46, -0.002, 0.01])
plt.show()
plt.clf()

# i = 0
# for n in corrected_values[-1]:
# 	plt.scatter(distances[i], corrected_values[-1][i]/ref[i])
# 	i += 1
# plt.show()
# plt.clf()