import json as simplejson
import json
import requests
import os.path
import time

from urllib.request import Request, urlopen
import cv2
import numpy as np

from src.User import User

class Messaging:

    oauth = None
    refresh_token = None
    me = None

    MESSAGE_THREADS_URL = 'https://es-gmsg.np.community.playstation.net/groupMessaging/v1/threads'
    MESSAGE_USERS_URL = 'https://es-gmsg.np.community.playstation.net/groupMessaging/v1/users/'
    SEND_MESSAGE_URL = 'https://es-gmsg.np.community.playstation.net/groupMessaging/v1/messageGroups/'

    def __init__(self, tokens):
        self.oauth = tokens['oauth']
        self.refresh_token = tokens['refresh']

        tokens = {
            'oauth': self.oauth,
            'refresh': self.refresh_token
        }

        user = User(tokens)
        self.me = user.me()['profile']['onlineId']

    def get_all_groups(self):
        header = {
            'Authorization': 'Bearer '+self.oauth
        }

        # url = self.MESSAGE_THREADS_URL + "/?fields=threadMembers,threadNameDetail,threadThumbnailDetail,threadProperty,latestMessageEventDetail,latestTakedownEventDetail,newArrivalEventDetail&limit=8&offset=0"
        # print(self.me)
        url = "https://fr-gmsg.np.community.playstation.net/groupMessaging/v1/users/{}/messageGroups?fields=@default,messageGroupId,messageGroupDetail,totalUnseenMessages,totalMessages,totalDataUsedMessages,latestMessage,latestMessage.messageUid,lastCheckDate,onlineFriendsCount,thumbnailDetail,myGroupDetail,messageGroupNameDetail,newMessageDetail&includeEmptyMessageGroup=true".format(self.me)

        response = requests.get(url, headers=header).text
        data = json.loads(response)

        return data

    def get_favorite_groups(self):
        header = {
            'Authorization': 'Bearer '+self.oauth
        }

        url = self.MESSAGE_THREADS_URL + "/?fields=threadMembers,threadNameDetail,threadThumbnailDetail,threadProperty,latestMessageEventDetail,latestTakedownEventDetail,newArrivalEventDetail&limit=200&offset=0&filter=favorite"
        response = requests.get(url, headers=header).text
        data = json.loads(response)

        return data

    def remove_group(self, group_id):
        header = {
            'Authorization': 'Bearer '+self.oauth
        }

        url = self.MESSAGE_THREADS_URL + "/" + group_id + "/users/me"
        response = requests.remove(url, headers=header)

    def favorite_group(self, group_id):
        self.set_favorite_group(group_id, True)

    def unfavorite_group(self, group_id):
        self.set_favorite_group(group_id, False);

    def set_favorite_group(self, group_id, flag):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + self.oauth
        }

        url = self.MESSAGE_USERS_URL  + "me/threads/" + group_id + "/favorites"

        payload = {"favoriteDetail": {"favoriteFlag": flag}}
        payload = json.dumps(payload)

        response = requests.put(url, headers=header, data=payload)

    def send_message(self, psn_ids, message_text = "", attachment = "", message_type = 1, audio_length = ""):
        header = {
            'Authorization': 'Bearer ' + self.oauth,
            'Content-Type': 'multipart/form-data; boundary="gc0p4Jq0M2Yt08jU534c0p"',
        }
        users_body = {
            "threadDetail": {
                "threadMembers": {}
            }
        }

        if (isinstance(psn_ids, list)):
            i = 0
            for psn_id in psn_ids:
                users_body["threadDetail"]["threadMembers"][i] = {"onlineId": psn_id}
                ++i
        else:
            users_body["threadDetail"]["threadMembers"][0] = {"onlineId": psn_ids}

        users_body["threadDetail"]["threadMembers"][len(users_body["threadDetail"]["threadMembers"])] = {"onlineId": self.me}

        message = "\n"
        message += "--gc0p4Jq0M2Yt08jU534c0p\n"
        message += "Content-Type: application/json; charset=utf-8\n"
        message += "Content-Disposition: form-data; name=\"threadDetail\"\n"
        message += "\n"

        message += json.dumps(users_body) + "\n"

        message_body = {
            "messageEventDetail": {

                "messageDetail": {},
                "eventCategoryCode": message_type
            }
        }
        if (message_type == 1011):
            message_body["messageEventDetail"]["messageDetail"]["voiceDetail"]["playbackTime"] = audio_length

        message_body["messageEventDetail"]["messageDetail"]["body"] = message_text

        if (os.path.isfile(attachment)):
            attachment_content = attachment.bytes()
            attachment_length  = len(attachment_content)

        if (message_type == 1011):
            content_key = "voiceData"
            content_type = "audio/3gpp"
        elif (message_type == 3):
            content_key = "imageData"
            content_type = "image/jpeg"

        if (bool(attachment)):
            message += "\n"
            message += "--gc0p4Jq0M2Yt08jU534c0p\n"
            message += "Content-Type: application/json; charset=utf-8\n"
            message += "Content-Disposition: form-data; name=\"messageEventDetail\"\n"
            message += "\n"

            message += json.dumps(message_body) + "\n"

            message += "--gc0p4Jq0M2Yt08jU534c0p\n"
            message += "Content-Type: ContentType\n"
            message += "Content-Disposition: form-data;name=\"" + content_key + "\"\n"
            message += "Content-Transfer-Encoding: binary\n"
            message += "Content-Length: AttachmentLength\n"
            message += "\n"

            message += attachment_content + "\n"

            message += "--gc0p4Jq0M2Yt08jU534c0p--\n\n"
        else:
            message += "\n"
            message += "--gc0p4Jq0M2Yt08jU534c0p\n"
            message += "Content-Type: application/json; charset=utf-8\n"
            message += "Content-Disposition: form-data; name=\"message\"\n"
            message += "\n"

            # message += json.dumps(message_body) + "\n"
            message += json.dumps({"message":{"messageKind":1,"body":"trtdgd"},"to":["FrtnChampionship"]})

            message += "--gc0p4Jq0M2Yt08jU534c0p--\n\n"
            
        print("\n\n******************************")
        print(header)
        print("\n\n******************************")
        print(message)
        print("******************************\n\n")
        response = requests.post(self.MESSAGE_THREADS_URL, headers=header, data=message).text
        print(response)

        return response

    #Max str = 512 char
    def send_group_message(self, group_id, message_text = "", attachment = "", message_type = 1, audio_length = ""):
        header = {
            'Authorization': 'Bearer ' + self.oauth,
            'Content-Type': 'multipart/form-data; boundary="gc0p4Jq0M2Yt08jU534c0p"',
        }

        message_body = {
            "messageEventDetail": {
                "messageDetail": {

                },
                "eventCategoryCode": message_type
            }
        }
        if (message_type == 1011):
            message_body["messageEventDetail"]["messageDetail"]["voiceDetail"]["playbackTime"] = audio_length

        message_body["messageEventDetail"]["messageDetail"]["body"] = message_text

        if (os.path.isfile(attachment)):
            attachment_content = attachment.bytes()
            attachment_length  = strlen(attachment_content)

        if (message_type == 1011):
            content_key = "voiceData"
            content_type = "audio/3gpp"

        elif (message_type == 3):
            content_key = "imageData"
            content_type = "image/jpeg"

        if (bool(attachment)):
            message = "\n"
            message += "--gc0p4Jq0M2Yt08jU534c0p\n"
            message += "Content-Type: application/json; charset=utf-8\n"
            message += "Content-Disposition: form-data; name=\"messageEventDetail\"\n"
            message += "\n"

            message += json.dumps(message_body) + "\n"

            message += "--gc0p4Jq0M2Yt08jU534c0p\n"
            message += "Content-Type: ContentType\n"
            message += "Content-Disposition: form-data;name=\"" + content_key + "\"\n"
            message += "Content-Transfer-Encoding: binary\n"
            message += "Content-Length: AttachmentLength\n"
            message += "\n"

            message += attachment_content + "\n"

            message += "--gc0p4Jq0M2Yt08jU534c0p--\n\n"
        else:
            message = "\n"
            message += "--gc0p4Jq0M2Yt08jU534c0p\n"
            message += "Content-Type: application/json; charset=utf-8\n"
            message += "Content-Disposition: form-data; name=\"messageEventDetail\"\n"
            message += "\n"

            message += json.dumps(message_body) + "\n"

            message += "--gc0p4Jq0M2Yt08jU534c0p--\n\n"
            response = requests.post(self.MESSAGE_THREADS_URL +  '/' + group_id + '/messages', headers=header, data=message).text

        print(response)

        return json.loads(response)

    def get_messages(self, group_id):
        header = {
            'Authorization': 'Bearer ' + self.oauth
        }
        url = self.MESSAGE_THREADS_URL + '/' + group_id + '?count=200&fields=threadMembers,threadNameDetail,threadThumbnailDetail,threadProperty,latestTakedownEventDetail,newArrivalEventDetail,threadEvents'
        response = requests.get(url, headers=header)
        data = json.loads(response.text)
        return data

    def download_picture(self, message, filenames=None):
        header = {
            'Authorization': 'Bearer ' + self.oauth
        }
        if (message["messageEventDetail"]["eventCategoryCode"] == 3):
            url = message["messageEventDetail"]["attachedMediaPath"]
            splited_url = url.split("/")
            if filenames == None:
                filenames = ["./pictures/{}.jpg".format(splited_url[len(splited_url) - 1])]

            for filename in filenames:
                filename = filename.replace("//", "/")
                if os.path.isfile(filename):
                    print("Picture already stored at {}".format(filename))
                    continue


                q = Request(url)
                q.add_header('Authorization', 'Bearer ' + self.oauth)
                resp = urlopen(q)


                # req = urllib2.Request(url)
                # req.add_header('Authorization', 'Bearer ' + self.oauth)
                # resp = urllib2.urlopen(req)
                image = np.asarray(bytearray(resp.read()), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                cv2.imwrite(filename,image)
                # cv2.imshow("Image", image)
                # cv2.waitKey(0)

                # response = requests.get(url, headers=header).content
                # with open(filename, 'wb') as handler:
                #     handler.write(response)

                # f = open(filename,'wb')
                # f.write(response)
                # f.close()
        
                # print("Url:{}, path:{}".format(url, message["messageEventDetail"]))
                print("Picture stored at {}".format(filename))
                time.sleep(2)
                return filename
        return None



