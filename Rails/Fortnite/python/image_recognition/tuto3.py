import tempfile

import cv2
import numpy as np
from PIL import Image
import pytesseract
from imutils import contours
import imutils
from operator import itemgetter
from os import listdir
from os.path import isfile, join


IMAGE_SIZE = 1800
BINARY_THREHOLD = 180

def display_image(img):
    cv2.imshow('image', img)
    k = cv2.waitKey(0)
    cv2.destroyAllWindows()
    if (k == 82):
        return True
    else:
        return False

def process_image_for_ocr(file_path):
    # TODO : Implement using opencv
    temp_filename = set_image_dpi(file_path)
    im_new = remove_noise_and_smooth(temp_filename)
    return im_new, temp_filename


def set_image_dpi(file_path):
    im = Image.open(file_path)
    length_x, width_y = im.size
    factor = max(1, int(IMAGE_SIZE / length_x))
    size = factor * length_x, factor * width_y
    # size = (1800, 1800)
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    print(temp_filename)
    im_resized.save(temp_filename, dpi=(300, 300))
    im_resized.save("../../pictures/resized.png", dpi=(300, 300))
    return temp_filename


def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3

def remove_noise_and_smooth(file_name):
    img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    # or_image = cv2.bitwise_or(img, closing)
    # display_image(or_image)
    return img

def get_contours(image):
    height, width = image.shape[:2]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)

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
        (x, y, w, h) = cv2.boundingRect(c)
        ar = y / height
        if (x > 80 and x < (width - 300)):
            if ar > 0.2 and ar < 0.58:
                # locs.append((x, y))
                locs.append((x, y, w, h))

    # locs.sort(key=itemgetter(0))
    locs.sort(key=itemgetter(1))
    # locs = sorted(locs, key=lambda x:x[0])
    # locs = sorted(locs, key=lambda y:y[1])
    # print(locs)
    # print(locs)
    return locs

def set_line_index(line):
    all_data = []
    for e in line:
        array_data = []
        if (e[0] < 200):
            array_data = ["name", e]
        elif (e[0] < 600):
            array_data = ["date", e]
        elif (e[0] < 800):
            array_data = ["duration", e]
        elif (e[0] < 900):
            array_data = ["rank", e]
        else:
            array_data = ["eliminations", e]
        all_data.append(array_data)
    return all_data


def convert_locs_to_lines(locs):
    ref_y = 0
    line = []
    lines = []
    for (i, (x, y, w, h)) in enumerate(locs):
        element = (x, y, w, h)
        if (ref_y == 0):
            ref_y = y
        if ((y - ref_y) > 3):
            line.sort(key=itemgetter(0))
            line = set_line_index(line)
            if (len(line) == 5):
                lines.append(line)
            line = [element]
            ref_y = y
        else:
            line.append(element)

    line.sort(key=itemgetter(0))
    line = set_line_index(line)
    lines.append(line)
    return lines

def get_reddif_lines_content(image, temp_filename):
    im = cv2.imread(temp_filename)
    all_file_data = []
    if (display_image(im) == False):
        return
    locs = get_contours(im)
    lines = convert_locs_to_lines(locs)
    digits = {}
 
    output = []
    line_number = 1
    line_infos = {}
    for (line) in lines:
        print("\n\nLine: {}".format(line_number))
        for k in line:
            part_type = k[0]
            (gX, gY, gW, gH) = k[1]
            group = image[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5]
            group = cv2.threshold(group, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            text = pytesseract.image_to_string(group, lang = 'fra',config='--psm 7')
            print("{}: {}".format(part_type ,text))
            line_infos[part_type] = text
            cv2.rectangle(im, (gX - 5, gY - 5), (gX + gW + 5, gY + gH + 5), (0, 0, 255), 2)
        line_number += 1
    all_file_data.append(line_infos)
    print(all_file_data)
    display_image(im)




filename = "../../pictures/rediff.png"

pictures_directory_example = "/home/dieuson/Desktop/PS4/27-04-2018/results/all_screenshots/"
all_files = [f for f in listdir(pictures_directory_example) if isfile(join(pictures_directory_example, f))]

for filename in all_files:
    filename = pictures_directory_example + filename
    image, temp_filename = process_image_for_ocr(filename)
    get_reddif_lines_content(image, temp_filename)

# text = pytesseract.image_to_string(image, lang = 'fra')
# print(text)
