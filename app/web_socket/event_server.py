import json
import random

from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer

from app.web_socket import web_req

images = [
    'https://www.somode.com/uploadimg/image/20230129/20230129150835_59024.jpg',
    'https://b0.bdstatic.com/617c56f8bf6cb6b56f40f53dd8482348.jpg',
    'https://b0.bdstatic.com/6b61eef52d574b0d308ca065a8db92a7.jpg',
    'https://b0.bdstatic.com/fc26e801b86376293f01fcad59adc22b.jpg',
    'https://b0.bdstatic.com/0043521dd25204d03708ca19a92cbc8e.jpg',
    'https://b0.bdstatic.com/775fdcd124ed1a0c48705adfd07d2f3e.jpg',
    'https://b0.bdstatic.com/949c0ad1cab83cb796108faa43e98f3e.jpg',
    'https://pic3.zhimg.com/80/v2-82e3a87fc2ed6c8aeb7633680f237792_720w.webp',
    'https://pica.zhimg.com/v2-2d431630bc2cdf202952d886bd9aec19_1440w.jpg?source=172ae18b',
    'https://pic1.zhimg.com/80/v2-d317b3b39003cd046b4866e455043f74_720w.webp'
]
keywords = ['黑子', '你干嘛', '鸡你', '两年半']


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        # 接受这个客户端的连接
        self.accept()
        # 获取群号, 即路由匹配中的地址
        group = self.scope['url_route']['kwargs'].get('group')
        # 将这个客户端的连接对象分组加入到内存或 Redis, 由配置决定使用内存还是 Redis
        # self.channel_layer.group_add('group_code', self.channel_name)  # group_add() 方法默认为异步
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)  # 转换为同步

    def websocket_receive(self, message):
        text = json.loads(message.get('text'))
        print('event 接收到的消息: ', text, type(text))
        group = self.scope['url_route']['kwargs'].get('group')

        post_type = text.get('post_type')
        # 生命周期事件
        if post_type == 'meta_event':
            return
        # 消息
        elif post_type == 'message':
            message_type = text.get('message_type')
            msg = text.get('message')
            user_id = text.get('user_id')
            answer = ''.join(['[CQ:image,file=', random.choice(images), ']'])
            key_flag = False
            for word in keywords:
                if -1 != msg.find(word):
                    key_flag = True
                    break

            if message_type == 'private':
                if not key_flag:
                    # 获取 AI 返回结果
                    answer = web_req.get_ai_answer(msg, user_id)
                json_data = web_req.send_private_msg(user_id, answer)
                async_to_sync(self.channel_layer.group_send)(group, {'type': 'send_msg', 'message': json_data})
            elif message_type == 'group':
                group_id = text.get('group_id')
                user_at = ''.join(['[CQ:at,qq=', str(user_id), ']'])
                self_at = ''.join(['[CQ:at,qq=', str(text.get('self_id')), ']'])
                rep_msg = msg.replace(self_at, '')

                if key_flag:
                    json_data = web_req.send_group_msg(group_id, ''.join([user_at, answer]))
                    async_to_sync(self.channel_layer.group_send)(group, {'type': 'send_msg', 'message': json_data})
                elif -1 != msg.find(self_at):
                    answer = web_req.get_ai_answer(rep_msg, user_id)
                    json_data = web_req.send_group_msg(group_id, ''.join([user_at, answer]))
                    async_to_sync(self.channel_layer.group_send)(group, {'type': 'send_msg', 'message': json_data})
        # 通知
        elif post_type == 'notice':
            notice_type = text.get('notice_type')

            # 私聊消息撤回
            if notice_type == 'friend_recall':
                recall_msg = web_req.get_msg(text.get('message_id'))
                call_msg = ''.join(['对方撤回了一条消息\n消息内容: ', recall_msg.get('message')])
                json_data = web_req.send_private_msg(text.get('user_id'), call_msg)
                async_to_sync(self.channel_layer.group_send)(group, {'type': 'send_msg', 'message': json_data})
            # 群聊消息撤回
            elif notice_type == 'group_recall':
                recall_msg = web_req.get_msg(text.get('message_id'))
                sender = recall_msg.get('sender')
                operator_id = text.get('operator_id')

                if operator_id == text.get('user_id'):
                    call_msg = ''.join(
                        [sender.get('nickname'), '(', str(sender.get('user_id')), ')撤回了一条消息\n消息内容: ',
                         recall_msg.get('message')])
                else:
                    operator_info = web_req.get_stranger_info(operator_id)
                    call_msg = ''.join(
                        [operator_info.get('nickname'), '(', str(operator_id), ')', '撤回了',
                         sender.get('nickname'), '(', str(sender.get('user_id')), ')的一条消息\n消息内容: ',
                         recall_msg.get('message')])
                json_data = web_req.send_group_msg(recall_msg.get('group_id'), call_msg)
                async_to_sync(self.channel_layer.group_send)(group, {'type': 'send_msg', 'message': json_data})
            # 群成员增加
            elif notice_type == 'group_increase':
                user_id = text.get('user_id')
                member_info = web_req.get_stranger_info(user_id)
                increase_info = ''.join(
                    ['[CQ:at,qq=', str(user_id), ']', '欢迎新成员 ', member_info.get('nickname'), '(', str(user_id),
                     ')加入本群'])
                json_data = web_req.send_group_msg(text.get('group_id'), increase_info)
                async_to_sync(self.channel_layer.group_send)(group, {'type': 'send_msg', 'message': json_data})
            # 群成员减少
            elif notice_type == 'group_decrease':
                user_id = text.get('user_id')
                member_info = web_req.get_stranger_info(user_id)
                operator_id = text.get('operator_id')

                if operator_id == user_id:
                    decrease_info = ''.join([member_info.get('nickname'), '(', str(user_id),
                                             ')在与崩坏兽的斗争中不幸的被吃掉了, 永远的离开了我们!'])
                else:
                    operator_info = web_req.get_stranger_info(operator_id)
                    decrease_info = ''.join(
                        [operator_info.get('nickname'), '(', str(operator_id), ')将',
                         member_info.get('nickname'), '(', str(user_id), ')踢出了本群'])
                json_data = web_req.send_group_msg(text.get('group_id'), decrease_info)
                async_to_sync(self.channel_layer.group_send)(group, {'type': 'send_msg', 'message': json_data})

    def send_msg(self, event):
        text = event['message']
        self.send(json.dumps(text, ensure_ascii=False))

    def websocket_disconnect(self, message):
        group = self.scope['url_route']['kwargs'].get('group')
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
        raise StopConsumer
