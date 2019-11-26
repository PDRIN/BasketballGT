import numpy as np

def mixed_strategy(m):
	a00 = (m[0][0] - m[0][2]) - (m[1][0] - m[1][2])
	a01 = (m[0][1] - m[0][2]) - (m[1][1] - m[1][2])
	b0 = (m[1][2] - m[0][2])

	a10 = (m[1][0] - m[1][2]) - (m[2][0] - m[2][2])
	a11 = (m[1][1] - m[1][2]) - (m[2][1] - m[2][2])
	b1 = (m[2][2] - m[1][2])

	a = np.array([[a00, a01], [a10, a11]])
	b = np.array([b0,b1])

	print(np.linalg.solve(a,b))

a = np.array([[1.04, 1.02, 1.08], [0.99, 1.02, 1.01], [1.00, 1.08, 1.05]])

mixed_strategy(a)