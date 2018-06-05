# -*- coding: utf-8 -*-
# @Author: dieuson
# @Date:   2018-04-26 21:58:49
# @Last Modified by:   Dieuson Virgile
# @Last Modified time: 2018-06-05 21:37:40
from src.Auth import Auth
from src.Friend import Friend
from src.User import User
from src.Messaging import Messaging
from image_recognition import menu_rediff_analyzer
import os
import json
import operator
from urllib.request import Request, urlopen
import cv2
import numpy as np

friend = None
messaging = None
TEXT = 1
PICTURE = 3
directory = "../tournaments/PS4/01-06-2018"
email = "fortnite.ps4.championship@gmail.com"
password = "Sinamari973"
uuid = "fe1fdbfa-f1a1-47ac-b793-e648fba25e86"
verification_code = "533421"


auth = Auth(email, password, uuid, verification_code)
tokens = auth.get_tokens()
friend = Friend(tokens)
messaging = Messaging(tokens)

print(tokens)

all_groups = messaging.get_all_groups()

def remove_dupes(hash_array):
	return([i for n, i in enumerate(hash_array) if i not in hash_array[n + 1:]])

def create_group_id_by_names(all_groups):
	group_by_names = {}
	for group in all_groups["messageGroups"]:
		group_id = group["messageGroupId"]
		group_name = group["messageGroupDetail"]["messageGroupName"]
		# if (group_name and group_name == "Djayvi"):
		group_by_names[group_name] = group_id
	return group_by_names

def download_picture(url, filename):
    req = Request(url)
    req.add_header('Authorization', 'Bearer ' + tokens["oauth"])
    resp = urlopen(req)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    cv2.imwrite(filename,image)
    print("Picture saved ! {}".format(filename))

def extract_message(message):
	data = {"sender": message["messageEventDetail"]["sender"]["onlineId"],
			"datetime": message["messageEventDetail"]["postDate"],
			"message_type": message["messageEventDetail"]["eventCategoryCode"], "origin": message}

	if (message["messageEventDetail"]["eventCategoryCode"] == TEXT):
		data["body"] = message["messageEventDetail"]["messageDetail"]["body"]
	elif (message["messageEventDetail"]["eventCategoryCode"] == PICTURE):
		data["body"] = message["messageEventDetail"]["attachedMediaPath"]
	return data


def parse_group_pictures(group_name, all_message_data):
	screenshot_directory = "{}/results/screenshots/".format(directory)
	all_screenshot_directory = "{}/results/all_screenshots/".format(directory)
	group_picture_paths = []

	total_pictures = 0
	group_nb_pictures = {}
	has_pictures = False
	directory_path = screenshot_directory + group_name

	if not os.path.exists(directory_path):
		os.makedirs(directory_path)

	for message_data in all_message_data:
		if (message_data["message_type"] == PICTURE):
			has_pictures = True
			if (message_data["sender"] not in group_nb_pictures.keys()):
				group_nb_pictures[message_data["sender"]] = 0
			else:
				group_nb_pictures[message_data["sender"]] += 1
			nb_picture = group_nb_pictures[message_data["sender"]]


			filename = directory_path
			picture_name = "/" + group_name + "___" + str(nb_picture) + "___" + message_data["sender"] + "___" + str(nb_picture) + ".png"
			picture_name = picture_name.replace(" ", "_")
			filename += picture_name
			all_screenshot_path = all_screenshot_directory + picture_name

			url = message_data["origin"]["messageEventDetail"]["attachedMediaPath"]
			data = {"team_path": filename.replace("..", "."), "all_screenshots_path": all_screenshot_path.replace("..", "."), "url": url}
			group_picture_paths.append(data)
			total_pictures += 1

	return group_picture_paths

def parse_group_messages(group_id):
	print("\n\n")
	messages = messaging.get_messages(group_id)
	all_message_data = []
	if "error" in messages.keys():
		print("ERROR")
		print(messages)
		exit(-1)

	for message in messages["threadEvents"]:
		message_data = extract_message(message)
		all_message_data.insert(0, message_data)
	return all_message_data

def parse_group(group_name):
	group_id = group_ids_by_name[group_name]
	return parse_group_messages(group_id)

def analyse_group_screenshots(group_name):
	all_picture_path_filename = "{}/results/all_picture_path.json".format(directory)
	group_messges = parse_group(group_name)
	group_pictures = parse_group_pictures(group_name, group_messges)

	analysed_pictures = []
	for picture_infos in group_pictures:
		picture_path = ("." + picture_infos["all_screenshots_path"]).replace("//", "/")
		if os.path.isfile(picture_path) == False:
			download_picture(picture_infos["url"], picture_path)
		result = menu_rediff_analyzer.analyse_screenshot(picture_path)
		analysed_pictures.append(result)
		print(result)

	print(analysed_pictures)

def analyse_groups_screenshots(group_ids_by_name):
	for (group_name, group_id) in group_ids_by_name.items():
		analyse_group_screenshots(group_name)


	# all_picture_path = []
	# all_data = []
	# with open(all_picture_path_filename) as data_file:
	# 	all_data = json.load(data_file)



	# menu_rediff_analyzer.analyse_screenshot(all_picture_path[0])



# def parse_groups(groups, messaging):
# 	filename = "{}/results/no_pictures.json".format(directory)
# 	has_no_pictures = []
# 	has_pictures = []
# 	groupd_index = 0

# 	for group in groups:
# 		group_id = group["id"]
# 		group_name = group["name"]
# 		print(group_id)
# 		print(group_name)
# 		print("Index: {}/{} Start extract {} pictures".format(groupd_index, len(group_ids),group_name))
# 		all_message_data = parse_group_messages(group_id, messaging)
# 		if (extract_pictures(all_message_data, group_name) == False):
# 			print("{} has no pictures".format(group_name))
# 		else:
# 			analyse_group_screenshots(group_name)


# 		# print(set(all_picture_path))
# # last_picture_path = all_picture_path[len(all_picture_path) - 1]
# 			# has_no_pictures.append(group_name)
# 			# with open(filename, 'w') as outfile:
# 			# 	json.dump(has_no_pictures, outfile)

# 		groupd_index += 1
# 		# if (groupd_index == 10):
# 		# 	exit(0)
		# print("\n")


# all_picture_path = []



# print("\n\n")

# group_id = '45960796c2e431f4494cafac6144e2d691be8fd1-960'
# parse_group_messages(group_id)

# init()
# exit(0)

group_ids_by_name = create_group_id_by_names(all_groups)

# analyse_group_screenshots("Djayvi")
analyse_groups_screenshots(group_ids_by_name)
# print(group_ids)

# group_ids.sort(key=operator.itemgetter("name"))
# # result = sorted(group_ids.keys(), key=operator.itemgetter("name"), reverse=True)
# print(group_ids)

# # exit(0)
# parse_groups(group_ids, messaging)



	