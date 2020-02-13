import base64
from datetime import datetime
from functools import lru_cache
from typing import NamedTuple
import uuid

import requests

from variables import url


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
        icon = cls.memoicon(author)
        return Akeet(
            icon=icon,
            author=author,
            text=text,
            published_date=published_date,
        )

    @classmethod
    @lru_cache()
    def memoicon(cls, author):
        icon = f"./cache/images/{author}_{uuid.uuid5(uuid.NAMESPACE_DNS, author)}.png"
        r = requests.get(url.USERINFO, {"username": author})
        with open(icon, "wb") as f:
            f.write(base64.b64decode(r.json()["base64_image"]))
        return icon