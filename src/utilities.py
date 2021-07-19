from dataclasses import dataclass
from enum import Enum, auto
import time


def get_time():
    return time.strftime("%H:%M:%S-%D")


class MessageType(Enum):
    TEXT_MESSAGE = auto()
    JSON_MESSAGE = auto()


class MessagePurpose(Enum):
    JOIN_REQUEST = "0000"
    ACCEPT_REQUEST = "1111"
    DENY_REQUEST = "2222"
    CHAT = "3333"
    NEW_MEMBER_JOINED = "4444"
    OTHERS = "5555"


@dataclass
class Message:
    def __init__(self, room_code, content, sender, purpose, to=None):
        self.room_code = room_code
        self.content = content
        self.sender = sender
        self.sent_time = get_time()
        self.purpose = purpose
        self.to = to

    def as_json(self):
        return {"room_code": self.room_code, "content": self.content, "sender": self.sender, "sent_time": self.sent_time, "purpose": self.purpose.value}
