import base64
from functools import lru_cache
from typing import NamedTuple
import uuid

import requests

from variables import url



class User(NamedTuple):
    """ユーザーデータ"""
    username: str = ""
    user_id: int = 0
    vio: str = ""
    icon: str = "./images/anonymous.png"

    @classmethod
    def fromusername(cls, username):
        vio, icon = cls.vio_and_icon(username)
        return cls(
            username=username,
            vio=vio,
            icon=icon,
        )

    @classmethod
    @lru_cache()
    def vio_and_icon(cls, username):
        icon = f"./cache/images/{username}_{uuid.uuid5(uuid.NAMESPACE_DNS, username)}.png"
        r = requests.get(url.USERINFO, {"username": username})
        data = r.json()
        with open(icon, "wb") as f:
            f.write(base64.b64decode(data["base64_image"]))
        return data["vio"], icon