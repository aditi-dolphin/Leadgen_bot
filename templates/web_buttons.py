class Button:

    def __init__(self):
        self.template = []

    def add_postback(self, title='', payload=''):
        json_payload = {"title": title, "type": "postback", "payload": payload}
        self.template.append(json_payload)

    def add_web_url(self, title='', url=''):
        json_payload = {"title": title, "type": "web_url", "url": url}
        self.template.append(json_payload)

    def get_button(self):
        return self.template