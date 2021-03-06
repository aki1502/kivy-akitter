from datetime import datetime
from typing import NamedTuple

from modules.user import User


class Akeet(NamedTuple):
    icon: str = "./images/anonymous.png"
    author: str = "aki1502"
    text: str = "こんにちは、世界！こんにちは、世界！こんにちは、世界！こんにち"
    published_date: datetime = datetime(1998, 2, 21, 20, 00)

    def row(self):
        """AkeetRowに向けてstr:strのdictに変換する"""
        r = {}
        for k in dir(self):
            v = getattr(self, k)
            if k.startswith("__"):
                pass
            elif isinstance(v, datetime):
                r[k] = v.strftime("%Y/%m/%d %H:%M")
            else:
                r[k] = str(v)
        return r

    @classmethod
    def from_response(cls, response):
        """APIから得たdictをAkeetに加工する"""
        author = response["author"]
        text = response["text"]
        published_date = datetime.fromisoformat(response["published_date"])
        _, icon = User.vio_and_icon(author)
        return cls(
            icon=icon,
            author=author,
            text=text,
            published_date=published_date,
        )