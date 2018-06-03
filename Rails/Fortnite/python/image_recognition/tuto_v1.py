# -*- coding: utf-8 -*-
# @Author: dieuson
# @Date:   2018-06-03 02:55:34
# @Last Modified by:   Dieuson Virgile
# @Last Modified time: 2018-06-03 22:45:58
from PIL import Image
import pytesseract
import cv2
import numpy as np
from imutils import contours
import imutils
import time

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

image = cv2.imread(filename)
image = imutils.resize(image, width=1080, height=720)
height, width = image.shape[:2]
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# gray = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY_INV)[1]



rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))


tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)

digits = {}

gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0,
	ksize=-1)
gradX = np.absolute(gradX)
(minVal, maxVal) = (np.min(gradX), np.max(gradX))
gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
gradX = gradX.astype("uint8")



# apply a closing operation using the rectangular kernel to help
# cloes gaps in between credit card number digits, then apply
# Otsu's thresholding method to binarize the image
gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
thresh = cv2.threshold(gradX, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
 

# apply a second closing operation to the binary image, again
# to help close gaps between credit card number regions
thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)


# find contours in the thresholded image, then initialize the
# list of digit locations
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
locs = []

# loop over the contours
for (i, c) in enumerate(cnts):
	# compute the bounding box of the contour, then use the
	# bounding box coordinates to derive the aspect ratio
	(x, y, w, h) = cv2.boundingRect(c)
	ar = y / height
	# ar = w / float(h)
	# ar = x / float(h)
	# since credit cards used a fixed size fonts with 4 groups
	# of 4 digits, we can prune potential contours based on the
	# aspect ratio
	if ar > 0.2 and ar < 0.25:
		# contours can further be pruned on minimum/maximum width
		# and height
		# append the bounding box region of the digits group
		# to our locations list
		locs.append((x, y, w, h))

locs = sorted(locs, key=lambda y:y[0])
output = []

# print(locs)
# display_image(gray)

# print(locs)
# loop over the 4 groupings of 4 digits
for (i, (gX, gY, gW, gH)) in enumerate(locs):
	# initialize the list of group digits
	groupOutput = []
 
	# extract the group ROI of 4 digits from the grayscale image,
	# then apply thresholding to segment the digits from the
	# background of the credit card
	group = gray[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5]
	# group = cv2.adaptiveThreshold(group,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
 #            cv2.THRESH_BINARY,11,2)
	group = cv2.threshold(group, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	# detect the contours of each individual digit in the group,
	# then sort the digit contours from left to right
	# text = pytesseract.image_to_string(group, lang = 'fra')
	# print(text)
	# display_image(group)
	# exit()

	digitCnts = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	digitCnts = digitCnts[0] if imutils.is_cv2() else digitCnts[1]
	digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]

	# display_image(group)
	# time.sleep(3)

	# loop over the digit contours
	for c in digitCnts:
		# compute the bounding box of the individual digit, extract
		# the digit, and resize it to have the same fixed size as
		# the reference OCR-A images
		(x, y, w, h) = cv2.boundingRect(c)
		roi = group[y:y + h, x:x + w]
		roi = cv2.resize(roi, (57, 88))
		# display_image(roi)
		digits[i] = roi

		# initialize a list of template matching scores	
		scores = []

		# loop over the reference digit name and digit ROI
		
		for (digit, digitROI) in digits.items():
			# apply correlation-based template matching, take the
			# score, and update the scores list
			result = cv2.matchTemplate(roi, digitROI,
				cv2.TM_CCOEFF)
			(_, score, _, _) = cv2.minMaxLoc(result)
			scores.append(score)

		# the classification for the digit ROI will be the reference
		# digit name with the *largest* template matching score
		# print(scores)
		groupOutput.append(str(np.argmax(scores)))

	# display_image(group)
	# draw the digit classifications around the group
	cv2.rectangle(image, (gX - 5, gY - 5), (gX + gW + 5, gY + gH + 5), (0, 0, 255), 2)
	cv2.putText(image, "".join(groupOutput), (gX, gY - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)
	# update the output digits list
	output.extend(groupOutput)


# display the output credit card information to the screen
# print("Credit Card Type: {}".format(output[0]))
# print("Credit Card #: {}".format("".join(output)))
# cv2.imshow("Image", image)
# cv2.waitKey(0)
display_image(image)

exit()



refCnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
refCnts = refCnts[0] if imutils.is_cv2() else refCnts[1]
refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]
digits = {}


# loop over the OCR-A reference contours
for (i, c) in enumerate(refCnts):
	# compute the bounding box for the digit, extract it, and resize
	# it to a fixed size
	(x, y, w, h) = cv2.boundingRect(c)
	roi = ref[y:y + h, x:x + w]
	roi = cv2.resize(roi, (57, 88))
 
	# update the digits dictionary, mapping the digit name to the ROI
	digits[i] = roi


# initialize a rectangular (wider than it is tall) and square
# structuring kernel


# image = cv2.imread(filename)
# image = imutils.resize(image, width=300)
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# text = pytesseract.image_to_string(ref, lang = 'fra')
# print(text)
display_image(image)










exit()





cv2.imwrite(result_filename, img)
extract_text(result_filename)

lower_red = np.array([30,150,50])
upper_red = np.array([255,255,180])


# ret, thresh = cv2.threshold(img, 70, 255, cv2.THRESH_BINARY_INV)
# 	ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
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
