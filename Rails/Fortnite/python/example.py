from src.Auth import Auth
from src.Friend import Friend
from src.User import User
from src.Messaging import Messaging

def extract_message(message):
	# print(message)
	return
	if (message["messageEventDetail"]["eventCategoryCode"] == 1):
		print(message["messageEventDetail"]["messageDetail"]["body"])
	elif (message["messageEventDetail"]["eventCategoryCode"] == 3):
		messaging.download_picture(message)

def get_messages(all_groups):
	print("\n\n")
	for thread in all_groups["threads"]:
		thread_id = thread["threadId"]
		messages = messaging.get_messages(thread_id)
		print(thread)
		for message in messages["threadEvents"]:
			extract_message(message)
		print("\n\n")

def send_message(psn, text):
	response = messaging.send_message(psn, text)
	# print(response)
    # def send_message(self, psn_ids, message_text = "", attachment = "", message_type = 1, audio_length = ""):



email = "dieuson.v@gmail.com"
password = "Sinamari973"
uuid = "55950157-ae9d-4b10-b0de-94dbef199f2c"
verification_code = 309334
verification_code = 718264
auth = Auth(email, password, uuid, verification_code)
tokens = auth.get_tokens()
# print(tokens)

friend = Friend(tokens)

messaging = Messaging(tokens)

psn = "FrtnChampionship"
msg = "Salut toi"
# send_message(psn, msg)
print("\n\n")
all_groups = messaging.get_all_groups()
print(all_groups)
# get_messages(all_groups)


# thread_id = all_groups["threads"][0]["threadId"]

# messages = messaging.get_messages(thread_id)
# message = messages["threadEvents"][2]

# if (message["messageEventDetail"]["eventCategoryCode"] == 1):
# 	print("Text message")
# elif (message["messageEventDetail"]["eventCategoryCode"] == 3):
# 	print("Image message")
# 	messaging.download_picture(message)


# print(all_groups)

# friend_list = friend.my_friends()

# friend_string = ''

# if bool(friend_list):
#     for key, value in friend_list.items():
#         friend_string += key+' is playing '+value+"\n"
# else:
#     friend_string = 'No friends online'

# print(friend_string)
