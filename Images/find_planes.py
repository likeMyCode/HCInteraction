from skimage import data, io, filters, morphology, feature, exposure, measure
from skimage.morphology import square, dilation
from skimage.filter import gaussian_filter
from matplotlib import pyplot as plt
import numpy as np

images = ["samolot%02d.jpg" % x for x in range(20)] 


def to_gray(img_name):
	gray_img = data.imread(img_name, as_grey=True)
	gray_img = np.asarray(gray_img)
    
	parameter = (1 - np.mean(gray_img)) * 0.64 
	size = np.shape(gray_img) 
    
	for i in range(size[0]):
		for j in range(size[1]):
			gray_img[i,j] = 1 - gray_img[i,j]
			gray_img[i,j] = gray_img[i,j] ** 5

			if (gray_img[i,j] > parameter):
				gray_img[i,j] = 1 
			else:
				gray_img[i,j] = 0 
    
	gray_img = morphology.closing(gray_img, morphology.square(25))
	gray_img = morphology.dilation(gray_img, morphology.disk(16))

	return gray_img


def to_gray2(img_name, th_value, off, erosion, closing, dilation):
	gray_img = data.imread(img_name, as_grey=True)
	gray_img = filters.threshold_adaptive(gray_img, th_value, offset=off)
	size = np.shape(gray_img) 

	for i in range(size[0]):
		for j in range(size[1]):
			if (gray_img[i,j] == 1):
				gray_img[i,j] = 0
			else:
				gray_img[i,j] = 1

	gray_img = morphology.erosion(gray_img, morphology.square(erosion))
	gray_img = morphology.closing(gray_img, morphology.square(closing))
	gray_img = morphology.dilation(gray_img, morphology.square(dilation))

	return gray_img


def find_centroid(points):
	x = [p[1] for p in points]
	y = [p[0] for p in points]
	centr = (sum(x) / len(points), sum(y) / len(points))
	return centr


def find_contours(gray_img,limit_cont):
	conts = measure.find_contours(gray_img, 0.8)
	conts = [cont for cont in conts if len(cont) > limit_cont]
	return conts  


def just_do_it(limit_cont):
	fig = plt.figure(facecolor='black')
	plt.gray()
	print("Rozpoczynam przetwarzanie obrazow...")
    
	for i in range(20):
		img = data.imread(images[i])

		gray_img = to_gray(images[i])				# samoloty1.pdf
		#gray_img = to_gray2(images[i],  1001, 0.2, 5, 9, 12) 	# samoloty2.pdf
		#gray_img = to_gray2(images[i],  641, 0.2, 5, 20, 5)	# samoloty3.pdf
		conts = find_contours(gray_img, limit_cont)
		centrs = [find_centroid(cont) for cont in conts]

		ax = fig.add_subplot(4,5,i)
		ax.set_yticks([])
		ax.set_xticks([])
		io.imshow(img)
		print("Przetworzono: " + images[i])
        
		for n, cont in enumerate(conts):
			ax.plot(cont[:, 1], cont[:, 0], linewidth=2)
            
		for centr in centrs:
			ax.add_artist(plt.Circle(centr, 5, color='white'))
            
	fig.tight_layout()
	#plt.show()
	plt.savefig('samoloty3.pdf')
    

if __name__ == '__main__':
    just_do_it(limit_cont=350)
