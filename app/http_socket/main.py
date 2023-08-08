# import random
# import receive
# import request
#
# images = [
#     'https://www.somode.com/uploadimg/image/20230129/20230129150835_59024.jpg',
#     'https://b0.bdstatic.com/617c56f8bf6cb6b56f40f53dd8482348.jpg',
#     'https://b0.bdstatic.com/6b61eef52d574b0d308ca065a8db92a7.jpg',
#     'https://b0.bdstatic.com/fc26e801b86376293f01fcad59adc22b.jpg',
#     'https://b0.bdstatic.com/0043521dd25204d03708ca19a92cbc8e.jpg',
#     'https://b0.bdstatic.com/775fdcd124ed1a0c48705adfd07d2f3e.jpg',
#     'https://b0.bdstatic.com/949c0ad1cab83cb796108faa43e98f3e.jpg',
#     'https://pic3.zhimg.com/80/v2-82e3a87fc2ed6c8aeb7633680f237792_720w.webp',
#     'https://pica.zhimg.com/v2-2d431630bc2cdf202952d886bd9aec19_1440w.jpg?source=172ae18b',
#     'https://pic1.zhimg.com/80/v2-d317b3b39003cd046b4866e455043f74_720w.webp'
# ]
# keywords = ['小黑子', '你干嘛', '鸡你太美']
#
#
# def main():
#     while True:
#         recv_req = receive.recv_request()
#         if recv_req is None:
#             continue
#         print('监听到事件: ', recv_req)
#
#         # 数据
#         if recv_req.get('post_type') == 'message':
#             message = recv_req.get('message')
#             user_id = recv_req.get('user_id')
#
#             # 私聊
#             if recv_req.get('message_type') == 'private':
#                 if message in keywords:
#                     answer = ''.join(['[CQ:image,file=', random.choice(images), ']'])
#                 else:
#                     # 获取 AI 返回结果
#                     answer = request.get_ai_answer(message, user_id)
#                 # 发送消息
#                 request.send_private_msg(user_id, answer)
#             # 群聊
#             elif recv_req.get('message_type') == 'group':
#                 self_id = str(recv_req.get('self_id'))
#
#                 if message in keywords:
#                     answer = ''.join(['[CQ:image,file=', random.choice(images), ']'])
#                     request.send_group_msg(recv_req.get('group_id'), ''.join(['[CQ:at,qq=', str(user_id), ']', answer]))
#                 elif -1 != message.find(''.join(['[CQ:at,qq=', self_id, ']'])):
#                     answer = request.get_ai_answer(message.replace(''.join(['[CQ:at,qq=', self_id, ']']), ''), user_id)
#                     request.send_group_msg(recv_req.get('group_id'), ''.join(['[CQ:at,qq=', str(user_id), ']', answer]))
#         # 通知
#         elif recv_req.get('post_type') == 'notice':
#             # 私聊消息撤回
#             if recv_req.get('notice_type') == 'friend_recall':
#                 recall_msg = request.get_msg(recv_req.get('message_id'))
#                 call_msg = ''.join(['对方撤回了一条消息\n消息内容: ', recall_msg.get('message')])
#                 request.send_private_msg(recv_req.get('user_id'), call_msg)
#             # 群聊消息撤回
#             elif recv_req.get('notice_type') == 'group_recall':
#                 recall_msg = request.get_msg(recv_req.get('message_id'))
#                 sender = recall_msg.get('sender')
#                 operator_id = recv_req.get('operator_id')
#
#                 if operator_id == recv_req.get('user_id'):
#                     call_msg = ''.join(
#                         [sender.get('nickname'), '(', str(sender.get('user_id')), ')撤回了一条消息\n消息内容: ',
#                          recall_msg.get('message')])
#                 else:
#                     operator_info = request.get_stranger_info(operator_id)
#                     call_msg = ''.join(
#                         [operator_info.get('nickname'), '(', str(operator_id), ')', '撤回了',
#                          sender.get('nickname'), '(', str(sender.get('user_id')), ')的一条消息\n消息内容: ',
#                          recall_msg.get('message')])
#
#                 request.send_group_msg(recall_msg.get('group_id'), call_msg)
#             # 群成员增加
#             elif recv_req.get('notice_type') == 'group_increase':
#                 user_id = recv_req.get('user_id')
#                 member_info = request.get_stranger_info(user_id)
#                 increase_info = ''.join(
#                     ['[CQ:at,qq=', str(user_id), ']', '欢迎新成员 ', member_info.get('nickname'), '(', str(user_id),
#                      ')加入本群'])
#                 request.send_group_msg(recv_req.get('group_id'), increase_info)
#             # 群成员减少
#             elif recv_req.get('notice_type') == 'group_decrease':
#                 user_id = recv_req.get('user_id')
#                 member_info = request.get_stranger_info(user_id)
#                 operator_id = recv_req.get('operator_id')
#
#                 if operator_id == user_id:
#                     decrease_info = ''.join([member_info.get('nickname'), '(', str(user_id),
#                                              ')在与崩坏兽的斗争中不幸的被吃掉了, 永远的离开了我们!'])
#                 else:
#                     operator_info = request.get_stranger_info(operator_id)
#                     decrease_info = ''.join(
#                         [operator_info.get('nickname'), '(', str(operator_id), ')将',
#                          member_info.get('nickname'), '(', str(user_id), ')踢出了本群'])
#                 request.send_group_msg(recv_req.get('group_id'), decrease_info)
#
#
# if __name__ == '__main__':
#     main()
