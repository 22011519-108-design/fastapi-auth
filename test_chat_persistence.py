import json

from app.modules.chat.services import save_message


class DummyDB:
    def __init__(self):
        self.added = []

    def add(self, obj):
        self.added.append(obj)

    def commit(self):
        pass

    def rollback(self):
        pass

    def refresh(self, obj):
        setattr(obj, "id", 1)


def test_save_message_serializes_dict_content():
    db = DummyDB()
    payload = {"message": "No matching books found.", "books": []}

    message = save_message(db, 42, "assistant", payload)

    assert isinstance(message.content, str)
    assert json.loads(message.content) == payload
    assert db.added[0] is message
