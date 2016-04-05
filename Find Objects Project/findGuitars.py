#!/usr/bin/python
#-*coding: utf-8 -*-

import numpy as np
import cv2
import sys
import matplotlib.pyplot as plt


'''
	PRZETWARZANIE OBRAZU - 
	WYKRYWANIE I ROZRÓŻNIANIE GITARY ELEKTRYCZNEJ OD AKUSTYCZNEJ

	Autorzy: Katarzyna Boczek, Patryk Gliszczyński


	Program ten ma na celu rozpoznawanie dwóch charakterystycznych
	typów gitar na podstawie otrzymanego obrazu i zaznaczenie ich
	położenia. Ponieważ gitara w odróżnieniu od na przykład tablic
	rejestracyjnych czy kart do gry ma bardzo nieregularny kształt,
	przez co przy różnych ustawieniach gitary bardzo utrudnia weryfikacje
	jej pozycji. Dlatego też mimo wielu prób nie potrafiliśmy napisać,
	jednej metody, która by w każdych warunkach bezbłędnie wykrywała
	położenie gitary. Oczywiście w idealnych warunkach, gdy gitara jest
	do nas skierowana bezpośrednio nie było żadnego problemu w wykryciu
	gitary na obrazie. Natomiast zbyt mocna zmiana perspektywy i położenie
	gitary było prawie niemożliwe do detekcji. Próbowaliśmy porównywać z
	wieloma "zdjęciami podstawowymi" np. sam gryf, sama podstrunnica, czy
	też gitara w całości, natomiast nie znaleźliśmy złotego środka, które
	zdjęcie byłoby najlepsze do porównania go z otrzymanym obrazem. 
'''



#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# FIND GUITARS

def findGuitars(fn1, fn2, fn3, method):
	electricImg = cv2.imread(fn1, 0)
	acousticImg = cv2.imread(fn2, 0)
	mainImg = cv2.imread(fn3, 0)
	electricColorImg = cv2.imread(fn1)
	acousticColorImg = cv2.imread(fn2)    
	mainColorImg = cv2.imread(fn3) 

	if electricImg is None:
		print ('Failed to load fn1:', fn1)
		sys.exit(1)
        
	if acousticImg is None:
		print ('Failed to load fn2:', fn2)
		sys.exit(1)

	if mainImg is None:
		print ('Failed to load fn3:', fn3)
		sys.exit(1)

	kp_pairs1 = match_images(electricImg, mainImg, method)
	kp_pairs2 = match_images(acousticImg, mainImg, method)
    
	if kp_pairs1:
		draw_matches('find_obj', kp_pairs1, kp_pairs2, electricImg, acousticImg,
		mainImg, electricColorImg, acousticColorImg, mainColorImg)   
	else:
		print ("No matches found")
    	

def match_images(img1, img2, method):

	if (method == 'SIFT'):
		detector = cv2.SIFT()
	elif (method == 'SURF'):
		detector = cv2.SURF(300, 5, 5)
	elif (method == 'ORB'):
		detector = cv2.ORB()
	elif (method == 'BRIEF'):
		star = cv2.FeatureDetector_create("STAR")
		brief = cv2.DescriptorExtractor_create("BRIEF")
		matcher = cv2.BFMatcher(cv2.NORM_L2)
		kp1 = star.detect(img1, None)
		kp2 = star.detect(img2, None)
		kp1, desc1 = brief.compute(img1, kp1)
		kp2, desc2 = brief.compute(img2, kp2)

		raw_matches = matcher.knnMatch(desc1, trainDescriptors = desc2, k = 2)
		kp_pairs = filter_matches(kp1, kp2, raw_matches)
		return kp_pairs
	
	else:
		print ("Wrong Method!")
		sys.exit(0)

	matcher = cv2.BFMatcher(cv2.NORM_L2)

	kp1, desc1 = detector.detectAndCompute(img1, None)
	kp2, desc2 = detector.detectAndCompute(img2, None)

	raw_matches = matcher.knnMatch(desc1, trainDescriptors = desc2, k = 2)
	kp_pairs = filter_matches(kp1, kp2, raw_matches)
	return kp_pairs


def filter_matches(kp1, kp2, matches, ratio = 0.75):
	mkp1, mkp2 = [], []
	
	for m in matches:
		if len(m) == 2 and m[0].distance < m[1].distance * ratio:
			m = m[0]
			mkp1.append( kp1[m.queryIdx] )
			mkp2.append( kp2[m.trainIdx] )
	
	kp_pairs = zip(mkp1, mkp2)
	return kp_pairs
    

def explore_match(win, kp_pairs1, kp_pairs2, electricImg, 
		acousticImg, mainImg, electricColorImg, acousticColorImg, 
		mainColorImg, status1=None, H1=None, status2=None, H2=None):
	
	h1, w1 = electricImg.shape[:2]
	h2, w2 = mainImg.shape[:2]
	h3, w3 = acousticImg.shape[:2]
	
	vis = np.zeros((max(h1, h2, h3), w1+w2+w3), np.uint8)
	vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)
	vis[:h1, :w1] = electricColorImg
	vis[:h2, w1:w1+w2] = mainColorImg
	vis[:h3, w1+w2:w1+w2+w3] = acousticColorImg 

	green = (0, 255, 0)
	red = (0, 0, 255)
	electricColor = (10, 10, 255)
	acousticColor = (0,255,255)
	electricLines = (10,255,10)
	acousticLines = (10,255,10)
	
	if H1 is not None:
		corners1 = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]])
		corners1 = np.int32( cv2.perspectiveTransform(corners1.reshape(1, -1, 2), H1).
			reshape(-1, 2) + (w1, 0) )
		cv2.polylines(vis, [corners1], True, electricColor, 3)

	if status1 is None:
		status1 = np.ones(len(kp_pairs1), np.bool_)
	
	p1_1 = np.int32([kpp[0].pt for kpp in kp_pairs1])
	p2_1 = np.int32([kpp[1].pt for kpp in kp_pairs1]) + (w1, 0)


	if H2 is not None:
		corners2 = np.float32([[0, 0], [w3, 0], [w3, h3], [0, h3]])
		corners2 = np.int32( cv2.perspectiveTransform(corners2.reshape(1, -1, 2), H2).
			reshape(-1, 2) + (w1, 0))
		cv2.polylines(vis, [corners2], True, acousticColor, 3)

	if status2 is None:
		status2 = np.ones(len(kp_pairs2), np.bool_)
	p1_2 = np.int32([kpp[0].pt for kpp in kp_pairs2])
	p2_2 = np.int32([kpp[1].pt for kpp in kp_pairs2]) + (w3, 0)

	
	for (x1, y1), (x2, y2), inlier in zip(p1_1, p2_1, status1):
		if inlier:
			col = green
			thickness = 3
			cv2.circle(vis, (x1, y1), 2, col, -1)
			cv2.circle(vis, (x2, y2), 2, col, -1)
		else:
			col = red
			r = 2
			thickness = 3
			cv2.line(vis, (x1-r, y1-r), (x1+r, y1+r), col, thickness)
			cv2.line(vis, (x1-r, y1+r), (x1+r, y1-r), col, thickness)
			cv2.line(vis, (x2-r, y2-r), (x2+r, y2+r), col, thickness)
			cv2.line(vis, (x2-r, y2+r), (x2+r, y2-r), col, thickness)

	for (x1, y1), (x2, y2), inlier in zip(p1_2, p2_2, status2):
		if inlier:
			col = green
			thickness = 3
			cv2.circle(vis, (x1 + w1 + w2 , y1), 2, col, -1)
			cv2.circle(vis, (x2 + w1 - w3, y2), 2, col, -1)
		else:
			col = red
			r = 2
			thickness = 3
			cv2.line(vis, (x1-r+(w1+w2), y1-r), (x1+r+(w1+w2), y1+r), col, thickness)
			cv2.line(vis, (x1-r+(w1+w2), y1+r), (x1+r+(w1+w2), y1-r), col, thickness)
			cv2.line(vis, (x2-r+(w1-w3), y2-r), (x2+r+(w1-w3), y2+r), col, thickness)
			cv2.line(vis, (x2-r+(w1-w3), y2+r), (x2+r+(w1-w3), y2-r), col, thickness)
	
	vis0 = vis.copy()
	
	if (H1 is not None):
		for (x1, y1), (x2, y2), inlier in zip(p1_1, p2_1, status1):
			if inlier:
				cv2.line(vis, (x1, y1), (x2, y2), electricLines)

	if (H2 is not None):
		for (x1, y1), (x2, y2), inlier in zip(p1_2, p2_2, status2):
			if inlier:
				cv2.line(vis, (x1+(w1+w2), y1), (x2+w1-w3, y2), acousticLines)

	cv2.imshow(win, vis)


def draw_matches(window_name, kp_pairs1, kp_pairs2, electricImg, acousticImg,
		mainImg, electricColorImg, acousticColorImg, mainColorImg):
	
	mkp1_1, mkp2_1 = zip(*kp_pairs1)
	p1_1 = np.float32([kp.pt for kp in mkp1_1])
	p2_1 = np.float32([kp.pt for kp in mkp2_1])

	mkp1_2, mkp2_2 = zip(*kp_pairs2)
	p1_2 = np.float32([kp.pt for kp in mkp1_2])
	p2_2 = np.float32([kp.pt for kp in mkp2_2])

	if len(kp_pairs1) >= 5:
		H1, status1 = cv2.findHomography(p1_1, p2_1, cv2.RANSAC, 5.0)
	else:
		H1, status1 = None, None

	if len(kp_pairs2) >= 5:
		H2, status2 = cv2.findHomography(p1_2, p2_2, cv2.RANSAC, 5.0)
	else:
		H2, status2 = None, None
    
	if len(p1_1):
		explore_match(window_name, kp_pairs1, kp_pairs2, electricImg, 
		acousticImg, mainImg, electricColorImg, acousticColorImg, 
		mainColorImg, status1, H1, status2, H2)



def captureCamera(fn1, fn2, method):
	cap = cv2.VideoCapture(0)
	electricImg = cv2.imread(fn1, 0)
	acousticImg = cv2.imread(fn2, 0)
	electricColorImg = cv2.imread(fn1)
	acousticColorImg = cv2.imread(fn2) 
	if electricImg is None:
		print ('Failed to load fn1:', fn1)
		sys.exit(1)
	
	if acousticImg is None:
		print ('Failed to load fn2:', fn2)
		sys.exit(1)

	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()

		mainImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)	   
		mainColorImg = frame

		kp_pairs1 = match_images(electricImg, mainImg, method)
		kp_pairs2 = match_images(acousticImg, mainImg, method)
    
		if kp_pairs1:
			draw_matches('find_obj', kp_pairs1, kp_pairs2, electricImg, acousticImg,
			mainImg, electricColorImg, acousticColorImg, mainColorImg)   
		else:
			cv2.imshow('frame',frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# Main


def main():
	if len(sys.argv) < 3:
		print ("No filenames specified")
		print ("USAGE: find_obj.py <image1> <image2>")
		sys.exit(1)

	if (sys.argv[2] == "true"):
		fn1 = "electricNarrow.png"
		fn2 = "acousticNarrow.png"
	elif (sys.argv[2] == "false"):
		fn1 = "electricNoNeck.png"
		fn2 = "acousticNoNeck.png"
	else:
		print ("Wrong parameter")

	fn3 = sys.argv[1]
	method = sys.argv[3]

	if (fn3 == 'camera'):
		captureCamera(fn1, fn2, method)
	else:
		findGuitars(fn1, fn2, fn3, method)
		cv2.waitKey()
		cv2.destroyAllWindows() 

if __name__ == '__main__': main()
