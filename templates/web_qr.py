class quick_reply:

    def __init__(self):
        self.template = {
            "quick_reply":{
                "text": '',
                "buttons":[]
            }
        }

    def add_quick_reply(self, text, title='', type='', payload=''):
        if not self.template["quick_reply"]["text"]:
            self.template["quick_reply"]['text'] = text
        button = {'title': title, 'type': type, 'payload': payload}
        self.template["quick_reply"]["buttons"].append(button)
        return self.template