__author__ = 'Xuan Han'


class Article:
    """article class"""

    def __init__(self, text_id, txt):
        self.id = text_id
        self.text = txt

    def get_id(self):
        return self.id

    def get_text(self):
        return self.text

    def to_string(self):
        print("*********start")
        print self.id
        print self.text
        print "*********end"
