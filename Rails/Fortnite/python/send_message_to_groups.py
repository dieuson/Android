# -*- coding: utf-8 -*-
# @Author: dieuson
# @Date:   2018-04-26 21:58:49
# @Last Modified by:   Dieuson Virgile
# @Last Modified time: 2018-06-02 14:59:49
from src.Auth import Auth
from src.Friend import Friend
from src.User import User
from src.Messaging import Messaging
import json
import os
import time
import screenshots

TEXT = 1
PICTURE = 3

group_id = "c2f1553c7ec794caaa6a09d63da5ef0e6654c572-854"
email = "fortnite.ps4.championship@gmail.com"
password = "Sinamari973"
# uuid = "eab93af0-cbcd-4c50-95f1-211806ea585c"
uuid = "4c2ea08e-24e0-4769-a1b1-5226181f931c"
uuid = "fe1fdbfa-f1a1-47ac-b793-e648fba25e86"
# verification_code = "075420"
verification_code = "146355"
directory = "../tournaments/PS4/01-06-2018"
auth = Auth(email, password, uuid, verification_code)
tokens = auth.get_tokens()
print(tokens)
exit()
friend = Friend(tokens)
messaging = Messaging(tokens)



subscribed_teams = None
subscribed_teams_filename = "{}/inscriptions/inscrits_update.json".format(directory)
with open(subscribed_teams_filename) as data_file:
	subscribed_teams = json.load(data_file)


def split_message_by_length(message):
	message_length = 512
	message_parts = []
	splited_message = message.split("\n")
	str_message_part = ""
	for message_part in splited_message:
		if (len(str_message_part) + len(message_part) < message_length):
			str_message_part += message_part + "\n"
		else:
			# str_message_part = str_message_part.replace("\n\n", "\n")
			message_parts.append(str_message_part)
			str_message_part = message_part + "\n"

	# str_message_part = str_message_part.replace("\n\n", "\n")
	message_parts.append(str_message_part)
	return message_parts


def extract_message(message):
	if (message["messageEventDetail"]["eventCategoryCode"] == TEXT):
		return message["messageEventDetail"]["messageDetail"]["body"]
	return None


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

def already_send(group_id, message_parts):
	all_message_data = parse_group_messages(group_id)
	for message_part in message_parts:
		if (message_part in all_message_data):
			print("Message already send to :{}".format(group_id))
			return True
	return False

def send_message_to_groups(message, group_ids):
	hash_array = {}
	message_parts = split_message_by_length(message)
	index_message_send = 0
	print("\n\nMessage to send")
	for message in message_parts:
		print(message)
		print("\n---------------------------\n")
	print("\n")
	for group_id in group_ids.values():
		nb_loop = 0
		if (already_send(group_id, message_parts)):
			continue
		for message_part in message_parts:
			messaging.send_group_message(group_id, message_part)
			# print(parse_group_messages(group_ids))
			if (nb_loop > 0):
				time.sleep(1)
			nb_loop += 1

		print("group_id: {}, index: {}".format(group_id, index_message_send))
		index_message_send += 1
		time.sleep(2)
		# break
	return hash_array

def link_groupId_groupName(all_groups):
	hash_array = {}
	for group in all_groups["messageGroups"]:
		groupId = group["messageGroupId"]
		groupName = group["messageGroupDetail"]["messageGroupName"]
		hash_array[groupName] = groupId
	return hash_array

def get_subscribed_group_names(subscribed_teams):
	data_item = subscribed_teams
	all_group_names = []
	for data in data_item:
		all_group_names.append(data["name"])
	return all_group_names

def get_group_ids_from_names(group_names, group_ids):
	hash_array = {}
	for group_name in group_names:
		# if (group_name == "DzXr"):
		hash_array[group_name] = group_ids[group_name]

		# if (group_name != "Teamort"):
		# 	hash_array[group_name] = group_ids[group_name]
	return hash_array

def get_groups_with_names(group_names, group_ids):
	all_groups = []
	for group_name in group_names:
		data = {"name": group_name, "id": group_ids[group_name]}
		all_groups.append(data)
		# if (group_name == "DzXr"):
		# hash_array[group_name] = group_ids[group_name]

		# if (group_name != "Teamort"):
		# 	hash_array[group_name] = group_ids[group_name]
	return all_groups



message_filename = "{}/messages/message_4.txt".format(directory)
message = None
with open(message_filename) as file:
	message = file.read()


all_groups = messaging.get_all_groups()
group_ids = link_groupId_groupName(all_groups)

group_names = get_subscribed_group_names(subscribed_teams)
# message_group_ids = get_group_ids_from_names(group_names, group_ids)
message_group_ids = get_groups_with_names(group_names, group_ids)
screenshots.parse_groups(message_group_ids, messaging)

# group_name = "Gang"
# group_id = group_ids[group_name]
# message_group_ids = [group_id]
# message_group_ids = group_ids
# message_group_ids = []
# for group_id in group_ids.values():
# 	message_group_ids.append(group_id)


# group_ids = group_ids.values()
# print(message_group_ids)
# print(message_group_ids[0])
# for group in all_groups["messageGroups"]:
# 	if (group["messageGroupDetail"]["messageGroupName"] == "Papel"):
# 		message_group_ids = [group["messageGroupId"]]
	# print(group)
	# 	break
# print(all_groups)
# print(message_group_ids)



# send_message_to_groups(message, message_group_ids)



# group_id = '45960796c2e431f4494cafac6144e2d691be8fd1-960'
# messaging.send_group_message(group_id, "Test message")
