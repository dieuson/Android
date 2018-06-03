# -*- coding: utf-8 -*-
# @Author: dieuson
# @Date:   2018-06-03 02:55:34
# @Last Modified by:   Dieuson Virgile
# @Last Modified time: 2018-06-03 16:13:46
from PIL import Image
import pytesseract
import cv2
import numpy as np
import imutils

filename = "../../pictures/sample_p1.png"
filename = "../../pictures/rediff.png"
result_filename = "../../pictures/sample_2.png"


def display_image(img):
	cv2.imshow('image', img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def extract_text(filename):
	img = cv2.imread(filename)	
	text = pytesseract.image_to_string(img, lang = 'fra')
	print(text)	
	display_image(img)

img = cv2.imread(filename)
img = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
img = cv2.threshold(img, 10, 255, cv2.THRESH_BINARY_INV)[1]

display_image(img)
cv2.imwrite(result_filename, img)
extract_text(result_filename)

lower_red = np.array([30,150,50])
upper_red = np.array([255,255,180])


# ret, thresh = cv2.threshold(img, 70, 255, cv2.THRESH_BINARY_INV)
# ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
# ret, img = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY_INV)
height, width = img.shape[:2]
img = cv2.resize(img, (width * 2, height * 2)) 
# print "Threshold selected : ", ret



cv2.imshow('image', img)
cv2.imwrite(result_filename, img)
cv2.waitKey(0)
text = pytesseract.image_to_string(img, lang = 'fra')





img = cv2.imread(result_filename)
# height, width = img.shape[:2]
# img = cv2.resize(img, (width * 2, height * 2)) 
text = pytesseract.image_to_string(img, lang = 'fra')
cv2.imwrite(result_filename, img)


cv2.imshow("Shrinked image", img)
key = cv2.waitKey()



print(text)



# img = cv2.imread(filename)
# px = img[100,100]
# print px

# # accessing only blue pixel
# blue = img[100,100,0]
# print blue




# img = cv2.imread(filename, 0)
# # ret, thresh = cv2.threshold(img, 70, 255, cv2.THRESH_BINARY_INV)
# # ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
# ret, thresh = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY_INV)
# cv2.imshow('image', thresh)
# cv2.imwrite("../../pictures/sample_2.png", thresh)



# ref = cv2.imread(filename)
# ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
# ref = cv2.threshold(ref, 10, 255, cv2.THRESH_BINARY_INV)[1]
# cv2.imwrite("../../pictures/sample_2.png", ref)


# cv2.imwrite("../../pictures/sample_2.png", thresh)
# cv2.waitKey(0)
# cv2.destroyAllWindows()




# img = cv2.imread("../../pictures/sample_2.png", 0)
# img = cv2.imread(result_filename)
# text = pytesseract.image_to_string(img, lang = 'fra')
# print(text)
# cv2.waitKey(0)

# cv2.destroyAllWindows()

# img = cv2.imread(path, 0)
# ret, thresh = cv2.threshold(img, 70, 255, cv2.THRESH_BINARY_INV)
# cv2.imshow('image', thresh)
# cv2.imwrite("h2kcw2/out1.png", thresh)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# im = Image.open(filename)
# im = im.convert('L')
# im.save("../../pictures/sample_2.png")
# text = pytesseract.image_to_string(im, lang = 'fra')

# print(text)
