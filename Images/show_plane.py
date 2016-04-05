from skimage import data, io, filters, morphology, feature, exposure, measure
from skimage.morphology import square, dilation
from skimage.filter import gaussian_filter
from matplotlib import pyplot as plt
import numpy as np

images = ["samolot00.jpg", "samolot01.jpg", "samolot08.jpg", "samolot10.jpg", "samolot12.jpg", "samolot09.jpg"] 

def main():
	plt.figure(facecolor='black')
	plt.gray()
	
	for i in range(6):
		img = io.imread(images[i], as_grey=True)
		img = filters.canny(img)
		img = morphology.erosion(img, morphology.square(1))
		
		plt.subplot(2,3,i)
		plt.axis('off')
		io.imshow(img)
	plt.show()
	

if __name__ == '__main__':
	main()
