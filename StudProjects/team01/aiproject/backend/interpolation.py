import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy import interpolate

n = 8
img1 = np.zeros((n, n))
img2 = np.zeros((n, n))

img1[2:4, 2:4] = 1
img2[4:6, 4:6] = 1

plt.figure()
plt.imshow(img1, cmap=cm.Greys)

plt.figure()
plt.imshow(img2, cmap=cm.Greys)

points = (np.r_[0, 2], np.arange(n), np.arange(n))
values = np.stack((img1, img2))
xi = np.rollaxis(np.mgrid[:n, :n], 0, 3).reshape((n**2, 2))
xi = np.c_[np.ones(n**2), xi]

values_x = interpolate.interpn(points, values, xi, method='linear')
values_x = values_x.reshape((n, n))
print(values_x)

plt.figure()
plt.imshow(values_x, cmap=cm.Greys)
plt.clim((0, 1))

plt.show()