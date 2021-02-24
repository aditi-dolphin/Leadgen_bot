from copy import deepcopy as copy

FB_QUICK_REPLY_LIMIT = 13
TITLE_CHARACTER_LIMIT = 20
PAYLOAD_CHARACTER_LIMIT = 1000


def add_quick_reply(message, content_type='text', title='', payload='', image_url=None):
    message_with_quick_reply = copy(message)
    if 'quick_replies' not in message_with_quick_reply:
        message_with_quick_reply['quick_replies'] = []
    if len(message_with_quick_reply['quick_replies']) < FB_QUICK_REPLY_LIMIT:
        quick_reply = {'content_type': content_type, 'title': title[:TITLE_CHARACTER_LIMIT],
                       'payload': payload[:PAYLOAD_CHARACTER_LIMIT]}
        if image_url is not None:
            quick_reply['image_url'] = image_url
        message_with_quick_reply['quick_replies'].append(quick_reply)
    return message_with_quick_reply