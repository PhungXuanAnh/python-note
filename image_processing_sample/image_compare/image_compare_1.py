"""
	Reference: https://github.com/khalillakhdhar/opencv-python-image-compare-and-detect

	pip install opencv-python scikit-image imutils

	Usage: 
"""

from skimage.metrics import structural_similarity as compare_ssim

import imutils
import cv2


imageA = cv2.imread("/home/xuananh/repo/python-note/image_processing_sample/test_images/banana.jpg")
imageB = cv2.imread("/home/xuananh/repo/python-note/image_processing_sample/test_images/banana2.jpg")
dim = (500, 500)

imageA = cv2.resize(imageA, dim, interpolation = cv2.INTER_AREA)
imageB = cv2.resize(imageB, dim, interpolation = cv2.INTER_AREA)
# convertion en gris
grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

# Calcule de 'Structural Similarity '(SSIM) 
# images, assure le retour
(score, diff) = compare_ssim(grayA, grayB, full=True)
diff = (diff * 255).astype("uint8")
print("indice de simularité SSIM: {}".format(score))

# detection de contour
# obtain the regions of the two input images that differ
thresh = cv2.threshold(diff, 0, 255,
	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# loop over the contours
for c in cnts:
	#dessiner un rectangle rouge autour
	(x, y, w, h) = cv2.boundingRect(c)
	cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
	cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

# afficher les images
cv2.imshow("Original", imageA)
cv2.imshow("Modified", imageB)
cv2.imshow("Diff", diff)
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)
