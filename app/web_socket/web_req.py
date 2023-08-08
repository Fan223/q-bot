import json

import requests

base_url = 'http://localhost:5701'
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer '}


def get_ai_answer(spoken, user_id):
    url = 'https://api.ownthink.com/bot'
    data = {
        'spoken': spoken,
        'appid': 'c5f24ccda9246230683d69d4e3ed2133',
        'userid': user_id
    }
    response = requests.post(url=url, data=data, headers=headers)

    res = json.loads(response.text)
    print('思知机器人返回为: ', res)
    return res.get('data').get('info').get('text')


def send_private_msg(user_id, message):
    return {
        'action': 'send_private_msg',
        'params': {
            'user_id': user_id,
            'message': message
        }
    }


def send_group_msg(group_id, message):
    return {
        'action': 'send_group_msg',
        'params': {
            'group_id': group_id,
            'message': message
        }
    }


def get_msg(message_id):
    url = base_url + '/get_msg'
    json_data = {
        'message_id': message_id,
    }
    response = requests.post(url=url, json=json_data, headers=headers)
    return json.loads(response.text).get('data')


def get_stranger_info(user_id):
    url = base_url + '/get_stranger_info'
    json_data = {
        'user_id': user_id,
    }
    response = requests.post(url=url, json=json_data, headers=headers)
    return json.loads(response.text).get('data')
