# -*- coding: utf-8 -*-
# @Author: dieuson
# @Date:   2018-04-26 21:58:49
# @Last Modified by:   Dieuson Virgile
# @Last Modified time: 2018-06-04 22:35:32
from src.Auth import Auth
from src.Friend import Friend
from src.User import User
from src.Messaging import Messaging
import os
import json
import operator

friend = None
messaging = None
TEXT = 1
PICTURE = 3
directory = "../tournaments/PS4/01-06-2018"

def extract_message(message):
	data = {"sender": message["messageEventDetail"]["sender"]["onlineId"],
			"datetime": message["messageEventDetail"]["postDate"],
			"message_type": message["messageEventDetail"]["eventCategoryCode"], "origin": message}

	if (message["messageEventDetail"]["eventCategoryCode"] == TEXT):
		data["body"] = message["messageEventDetail"]["messageDetail"]["body"]
		# print(data["body"])
		# print(message["messageEventDetail"]["messageDetail"]["body"])
	elif (message["messageEventDetail"]["eventCategoryCode"] == PICTURE):
		data["body"] = message["messageEventDetail"]["attachedMediaPath"]
		# print(data["body"])
		# messaging.download_picture(message)
	return data


def extract_pictures(all_message_data, group_name):
	screenshot_directory = "{}/results/screenshots/".format(directory)
	all_screenshot_directory = "{}/results/all_screenshots/".format(directory)
	all_picture_path_filename = "{}/results/all_picture_path.json".format(directory)

	total_pictures = 0
	group_nb_pictures = {}
	has_pictures = False
	directory_path = screenshot_directory + group_name
	if not os.path.exists(directory_path):
		os.makedirs(directory_path)

	if not os.path.exists(all_picture_path_filename):
		all_picture_path = []
	else:
		with open(all_picture_path_filename) as data_file:
			all_picture_path = json.load(data_file)

	for message_data in all_message_data:
		if (message_data["message_type"] == PICTURE):
			has_pictures = True
			if (message_data["sender"] not in group_nb_pictures.keys()):
				group_nb_pictures[message_data["sender"]] = 0
			else:
				group_nb_pictures[message_data["sender"]] += 1
			nb_picture = group_nb_pictures[message_data["sender"]]


			filename = directory_path
			picture_name = "/" + group_name + "___" + str(total_pictures) + "___" + message_data["sender"] + "___" + str(nb_picture) + ".png"
			picture_name = picture_name.replace(" ", "_")
			filename += picture_name
			all_screenshot_path = all_screenshot_directory + picture_name

			url = message_data["origin"]["messageEventDetail"]["attachedMediaPath"]
			data = {"team_path": filename.replace("..", "."), "all_screenshots_path": all_screenshot_path.replace("..", "."), "url": url}
			all_picture_path.append(data)
			total_pictures += 1
			# print(data)
			# print("\n\n")


			messaging.download_picture(message_data["origin"], [filename, all_screenshot_path])
	# with open("{}/results/all_picture_path.json".format(directory), 'w') as outfile:
	# 	json.dump(all_picture_path, outfile)
	return has_pictures

def parse_group_messages(group_id, messaging):
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

def parse_groups(groups, messaging):

	# print("test")
	# group_name = "La fyre"
	# group_id = group_ids[group_name]
	filename = "{}/results/no_pictures.json".format(directory)
	has_no_pictures = []
	has_pictures = []
	groupd_index = 0

	for group in groups:
		# print(group)
		group_id = group["id"]
		group_name = group["name"]
		print(group_id)
		print(group_name)
		# print("Index: {}/{} Start extract {} pictures".format(groupd_index, len(group_ids),group_name))
		all_message_data = parse_group_messages(group_id, messaging)
		if (extract_pictures(all_message_data, group_name) == False):
			print("{} has no pictures".format(group_name))
			# has_no_pictures.append(group_name)
			# with open(filename, 'w') as outfile:
			# 	json.dump(has_no_pictures, outfile)

		groupd_index += 1
		# if (groupd_index == 10):
		# 	exit(0)
		# print("\n")

def link_groupId_groupName(all_groups):
	hash_array = {}
	groups_array = []
	for group in all_groups["messageGroups"]:
		groupId = group["messageGroupId"]
		groupName = group["messageGroupDetail"]["messageGroupName"]
		if (len(groupName) > 0 and "Djayvi" in groupName):
			groups_array.append({"name": groupName, "id": groupId})
		# hash_array[groupName] = groupId
	# print(hash_array)
	# return hash_array
	return groups_array

# all_picture_path = []
email = "fortnite.ps4.championship@gmail.com"
password = "Sinamari973"

# # uuid = "fe1fdbfa-f1a1-47ac-b793-e648fba25e86"
uuid = "fe1fdbfa-f1a1-47ac-b793-e648fba25e86"

verification_code = "533421"


auth = Auth(email, password, uuid, verification_code)
tokens = auth.get_tokens()
print(tokens)
friend = Friend(tokens)
messaging = Messaging(tokens)

# print("\n\n")

# group_id = '45960796c2e431f4494cafac6144e2d691be8fd1-960'
# parse_group_messages(group_id)

# init()
# exit(0)

all_groups = messaging.get_all_groups()
group_ids = link_groupId_groupName(all_groups)
# print(group_ids)

# group_ids.sort(key=operator.itemgetter("name"))
# # result = sorted(group_ids.keys(), key=operator.itemgetter("name"), reverse=True)
# print(group_ids)

# # exit(0)
parse_groups(group_ids, messaging)



	