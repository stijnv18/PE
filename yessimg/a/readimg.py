import PIL.Image
import numpy as np
from matplotlib import pyplot as plt
from imageio import imread

img = imread('test.png')
height, width, channels = img.shape
plt.imshow(img)
white = (img[:, :, :3] >= 150).all(2)

coords = np.array(np.where(white))[::-1].T

#Backtoimg = coords.reshape((height , width))

# Get the maximum value in the first row of pixels
#max_value = np.amax(Backtoimg[0])

# Get the index of the pixel with the maximum x-coordinate (rightmost pixel)


# Find all the pixels with the lowest y-value

lowest_y = np.min(coords[:, 1])
lowest_y_pixels = coords[coords[:, 1] == lowest_y]
lowest_y_x_values = lowest_y_pixels[:, 0]
Topcorner = lowest_y_pixels[np.argmax(lowest_y_pixels[:, 0])]

biggest_y = np.max(coords[:, 1])
biggest_y_pixels = coords[coords[:, 1] == biggest_y]
biggest_y_x_values = biggest_y_pixels[:, 0]
Bottemcorner = biggest_y_pixels[np.argmax(biggest_y_pixels[:, 0])]



plt.plot(Topcorner[0], Topcorner[1], 'ro')
plt.plot(Bottemcorner[0], Bottemcorner[1], 'ro')

plt.show()




