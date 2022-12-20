# Push info to wx
# AID CID SECRET SENDKEY 
#
from requests_toolbelt import MultipartEncoder
import json
import requests


class wx_push(object):

    CID = your_CID
    AID = your_AID
    SECRET = your_SECRET
    sendkey = your_sendkey

    def decide_push_application(via):
        # decide which app to be sent with
        if via == 'rwth':
            wx_push.AID = your_AID
            wx_push.SECRET = your_SECRET
        elif via == 'important':
            wx_push.AID = your_AID
            wx_push.SECRET = your_SECRET

    def push_text(text, wecom_touid='@all'):
        # push text info
        get_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(
            wx_push.CID, wx_push.SECRET)
        response = requests.get(get_token_url).content
        access_token = json.loads(response).get('access_token')

        if access_token and len(access_token) > 0:
            send_msg_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(
                access_token)
            data = {
                "touser": wecom_touid,
                "agentid": wx_push.AID,
                "msgtype": "text",
                "text": {
                    "content": text
                },
                "duplicate_check_interval": 600
            }
            response = requests.post(
                send_msg_url, data=json.dumps(data)).content
            return response
        else:
            print ("Invalid access_token")

    def push_file(media_id, wecom_touid='@all'):
        # push file info
        get_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(
            wx_push.CID, wx_push.SECRET)
        response = requests.get(get_token_url).content
        access_token = json.loads(response).get('access_token')

        if access_token and len(access_token) > 0:
            send_msg_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(
                access_token)
            data = {
                "touser": wecom_touid,
                "agentid": wx_push.AID,
                "msgtype": "file",
                "file": {
                    "media_id": media_id
                },
                "duplicate_check_interval": 600
            }
            response = requests.post(
                send_msg_url, data=json.dumps(data)).content
            return response
        else:
            print ("Invalid access_token")

    def push_image(media_id, wecom_touid='@all'):
        # push pic info
        get_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(
            wx_push.CID, wx_push.SECRET)
        response = requests.get(get_token_url).content
        access_token = json.loads(response).get('access_token')

        if access_token and len(access_token) > 0:
            send_msg_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(
                access_token)
            data = {
                "touser": wecom_touid,
                "agentid": wx_push.AID,
                "msgtype": "image",
                "image": {
                    "media_id": media_id
                },
                "duplicate_check_interval": 600
            }
            response = requests.post(
                send_msg_url, data=json.dumps(data)).content
            return response
        else:
            print ("Invalid access_token")

    def post_media_to_wechat_get_media_id(filepath, filename):
        # 上传素材 获得median_id
        get_token_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'.format(
            wx_push.CID, wx_push.SECRET)
        response = requests.get(get_token_url).content
        access_token = json.loads(response).get('access_token')
        post_file_url = f"https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=file"
        m = MultipartEncoder(fields={filename: (
            f'{filename}', open(filepath + filename, 'rb'), 'text/plain')})
        r = requests.post(url=post_file_url, data=m, headers={
                          'Content-Type': m.content_type})
        r = json.loads(r.text)
        try:
            media_id = r['media_id']
            return media_id
        except:
            print(r['errmsg'])
        

    def Push(via, type, path="", name="", content=""):
        wx_push.decide_push_application(via)
        if type == "text":
            if content == "":
                print ("Content entry error")
            else:
                ret = wx_push.push_text(content)
                return ret

        elif type == "file":
            if name == "":
                print ("Name entry error")
            else:
                media_id = wx_push.post_media_to_wechat_get_media_id(
                    path, name)
                ret = wx_push.push_file(media_id=media_id)
                return ret

        elif type == "image":
            if name == "":
                print ("Name entry error")
            else:
                media_id = wx_push.post_media_to_wechat_get_media_id(
                    path, name)
                ret = wx_push.push_image(media_id=media_id)
                return ret

        else:
            return "Type entry error"

#example
""" 
wx_push.Push("important","text",content="Hello")
wx_push.Push("important","file",name="test.txt")
wx_push.Push("important","image",name="test.png") """
