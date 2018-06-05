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
import operator
import json
from . import rediff_postprocessing
# import rediff_postprocessing


IMAGE_SIZE = 1800
BINARY_THREHOLD = 180
COLUMN_DIFF = 8
LINE_DIFF = 8
SPACE_BETWEEN_LINES = 8

def display_image(img):
    winname = 'image'
    img = cv2.resize(img, (1080, 720))
    cv2.imshow(winname, img)
    cv2.moveWindow(winname, 0, 0)
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
    # im_resized.save("../../pictures/resized.png", dpi=(300, 300))
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
        y_ratio = y / height
        x_ratio = x / width
        if (x_ratio > 0.01 and x_ratio < 0.8 and w > 5 and h > 5):
            if y_ratio > 0.15 and y_ratio < 0.58:
                    # locs.append((x, y))
                locs.append((x, y, w, h))

    locs.sort(key=itemgetter(1))
    return locs

def set_line_index(line):
    all_data = []
    index_names = ["name", "date", "duration", "rank", "eliminations"]
    for i, e in enumerate(line):
        all_data.append([index_names[i], e])
    return all_data


def detect_column_positions(locs):
    all_x_indexes = []
    all_column = {}
    for (i, (x, y, w, h)) in enumerate(locs):
        all_x_indexes.append(x)

    for x_index in all_x_indexes:
        more_close = x_index
        more_close_index = 0
        if (x_index not in all_column.keys()):
            all_column[x_index] = 0

        for i, column in enumerate(all_column):
            if (abs(x_index - column) < COLUMN_DIFF):
                all_column[x_index] += 1
    column_position_hash = sorted(all_column.items(), key=operator.itemgetter(1), reverse=True)
    column_position_hash = column_position_hash[:5]
    # column_position_hash = column_position_hash
    column_position_hash.sort(key=itemgetter(0))
    relevant_column_positions = []
    for column in column_position_hash:
        relevant_column_positions.append(column[0])
    return relevant_column_positions

def detect_line_positions(locs, relevant_column_positions):
    all_y_indexes = []
    all_lines = {}
    for (i, (x, y, w, h)) in enumerate(locs):
        all_y_indexes.append((x,y))

    for (x_index, y_index) in all_y_indexes:
        more_close = y_index
        more_close_index = 0
        if (y_index not in all_lines.keys()):
            all_lines[y_index] = 0

        for i, column in enumerate(all_lines):
            # if (abs(y_index - column) < COLUMN_DIFF and is_a_relevant_column(x_index, relevant_column_positions)):
            if (abs(y_index - column) < LINE_DIFF and is_a_relevant_column(x_index, relevant_column_positions)):

                all_lines[y_index] += 1
    line_position_hash = sorted(all_lines.items(), key=operator.itemgetter(1), reverse=True)
    # line_position_hash = line_position_hash[:10]
    line_position_hash = line_position_hash
    line_position_hash.sort(key=itemgetter(0))
    relevant_line_positions = []
    for column in line_position_hash:
        if (column[1] >= 3):
            relevant_line_positions.append(column[0])
    return relevant_line_positions

def is_a_relevant_column(x_position, relevant_column_positions):
    for relevant_column in relevant_column_positions:
        if (abs(x_position - relevant_column) < COLUMN_DIFF):
            return True
    return False

def is_a_relevant_line(y_position, relevant_column_positions):
    for relevant_column in relevant_column_positions:
        if (abs(y_position - relevant_column) < SPACE_BETWEEN_LINES):
            return True
    return False

def convert_locs_to_lines(locs):
    ref_y = 0
    line = []
    lines = []
    relevant_column_positions = detect_column_positions(locs)
    relevant_line_positions = detect_line_positions(locs, relevant_column_positions)
    # print(relevant_line_positions)
    prev_line = 0
    for (i, (x, y, w, h)) in enumerate(locs):
        element = (x, y, w, h)
        if (prev_line != 0 and (y - prev_line) > SPACE_BETWEEN_LINES):
            line.sort(key=itemgetter(0))
            line = set_line_index(line[:5])
            lines.append(line)
            # print("\n\n")
            # print(y)
            line = [element]
            ref_y = y
        else:
            line.append(element)
            # print(y)
        #     line.append(element)
        prev_line = y

    line.sort(key=itemgetter(0))
    line = set_line_index(line[:5])
    lines.append(line)
    return lines

def extract_part_info(group, line_infos, part_type):
    text = pytesseract.image_to_string(group, lang = 'fra',config='--psm 7')
    if ("DATE" in text or "NOM" in text):
        return None
    line_infos[part_type] = rediff_postprocessing.process(part_type, text)
    if (line_infos[part_type] is None):
        return None
    print("{}: {}".format(part_type ,line_infos[part_type]))
    return(line_infos)

def get_reddif_lines_content(image, temp_filename):
    im = cv2.imread(temp_filename)
    all_file_data = []
    locs = get_contours(im)
    lines = convert_locs_to_lines(locs)
    digits = {}
 
    output = []
    line_number = 1
    for (line) in lines:
        line_infos = {}
        print("\n\nLine: {}".format(line_number))
        if (len(line) != 5):
            continue
        for k in line:
            part_type = k[0]
            (gX, gY, gW, gH) = k[1]
            group = image[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5]
            group = cv2.threshold(group, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

            line_infos = extract_part_info(group, line_infos, part_type)
            if (line_infos is None):
                break
            cv2.rectangle(im, (gX - 5, gY - 5), (gX + gW + 5, gY + gH + 5), (0, 0, 255), 2)


            line_number += 1
        if (line_infos):
            all_file_data.append(line_infos)
    display_image(im)
    return all_file_data

def analyse_screenshot(filename):
    image, temp_filename = process_image_for_ocr(filename)
    file_data = get_reddif_lines_content(image, temp_filename)
    hash_data = {"path": filename, "data": file_data}
    print(hash_data)
    return hash_data


def test_image_recognition():
    filename = "../../pictures/rediff.png"

    # pictures_directory_example = "/home/dieuson/Desktop/PS4/27-04-2018/results/all_screenshots/"
    pictures_directory_example = "../../pictures/menu_rediffs/"
    all_files = [f for f in listdir(pictures_directory_example) if isfile(join(pictures_directory_example, f))]
    all_files.sort()
    # all_files = all_files[14:]
    # all_files = all_files[38:]
    all_screenshots_data = []

    json_data=open('all_screenshots_data.json').read()
    all_screenshots_data = json.loads(json_data)

    for filename in all_files:
        # filename = all_files[0]
        already_analysed = False
        # filename = "Kappa_Army___BliTztangBliTz___4.png"
        filename = pictures_directory_example + filename
        # filename = "../../pictures/kills/Agents_d’élite___Cyrilinho____0.png"
        # filename = "../../pictures/chat_kill/ATN___Singed404___0.png"
        # print(filename)
        for screenshot_data in all_screenshots_data:
            if filename in screenshot_data["path"]:
                already_analysed = True
        if (already_analysed):
            print("Already analysed")
            # continue

        image, temp_filename = process_image_for_ocr(filename)
        file_data = get_reddif_lines_content(image, temp_filename)
        hash_data = {"path": filename, "data": file_data}
        all_screenshots_data.append(hash_data)
        # with open('all_screenshots_data_2.json', 'w') as outfile:
        #     json.dump(all_screenshots_data, outfile)
        exit(0)
# text = pytesseract.image_to_string(image, lang = 'fra')
# print(text)

# test_image_recognition()

