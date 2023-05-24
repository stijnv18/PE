import PIL.Image
import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
from scipy.ndimage import label
from imageio import imread
import time

starttime = time.time()




img = imread('test.png')
height, width, channels = img.shape
plt.imshow(img)

# Convert the image to binary (white pixels have a value of 1, black pixels have a value of 0)
white = (img[:, :, :3] >= 150).all(2).astype(int)

# Label the connected components in the binary image
labels, num_labels = label(white)

# Find the largest connected component (excluding the background label 0)
largest_label = np.argmax(np.bincount(labels.flat)[1:]) + 1

# Extract the coordinates of the largest connected component
coords = np.array(np.where(labels == largest_label))[::-1].T

# Interpolate the y-coordinates of the pixels
f = interp1d(coords[:, 0], coords[:, 1], kind='linear', fill_value=(coords[0, 1], coords[-1, 1]), bounds_error=False)

# Generate a new set of x-coordinates to interpolate to
x_new = np.linspace(coords[0, 0], coords[-1, 0], num=len(coords))

# Evaluate the interpolation function at the new x-coordinates
coords_new = np.column_stack((x_new, f(x_new)))

stoptime = time.time()
print(stoptime - starttime)

# Plot the original and smoothed coordinates
plt.plot(coords[:, 0], coords[:, 1], 'bo', markersize=2)
#plt.plot(coords_new[:, 0], coords_new[:, 1], 'r-', linewidth=2)
plt.show()