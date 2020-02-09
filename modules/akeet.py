from datetime import datetime
from typing import NamedTuple



class Akeet(NamedTuple):
    icon: str = "./images/anonymous.png"
    author: str = "aki1502"
    text: str = "こんにちは、世界！こんにちは、世界！こんにちは、世界！こんにち"
    date: datetime = datetime(1998, 2, 21, 20, 00)

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