#!/usr/bin/python

import numpy as np

res = 0.2
size = 100
half = res*size/2

def dSquared(x, y, z):
	return np.sqrt((x-half)**2 + (y-half)**2 + (z-pos)**2)

for t in range(10):
	print t
	filename = 'density%04i.cub'%(t*1000)
	pos = half + (t - 5)/10.0*half

	header = '''Qbox wavefunction in VMD CUBE format
  electron density
2 0.00000000 0.00000000 0.00000000
%i %.8f 0.00000000 0.00000000
%i 0.00000000 %.8f 0.00000000
%i 0.00000000 0.00000000 %.8f
13 13.00000000 %.8f %.8f 0.00000000
1 1.00000000 %.8f %.8f %.8f
'''%(size, res, size, res, size, res, half, half, half, half, pos)

	with open(filename, 'w') as file:
		file.write(header)

	i = 0
	sigma = (res*size/50.0)
	for X in range(size):
		for Y in range(size):
			for Z in range(size):
				x = X*res
				y = Y*res
				z = Z*res
				d2 = dSquared(x, y, z)
				f = np.exp(-d2/sigma) + np.exp(-z*z/(sigma*sigma))
				with open(filename, 'a') as file:
					file.write('%.5e '%f)
					if i % 6 == 5:
						file.write('\n')
				i += 1