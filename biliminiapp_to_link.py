import html

import requests
import ujson
from aiocqhttp.event import Event

from hoshino import Service

from .config import PROXIES

sv = Service("biliminiapp", enable_on_default=True, help_="Bilibili小程序转链接")


@sv.on_message("group")
async def biliminiapp_to_link(bot, event: Event):
    msg = str(event.message)
    # 获取小程序 JSON 信息
    data = msg[msg.find("data=") + len("data=") : -1]
    data = html.unescape(data)
    try:
        data_j = ujson.loads(data)
    except ujson.JSONDecodeError:
        return  # 非小程序信息，函数返回

    # 提取视频标题及URL
    if (
        type(data_j) == dict
        and data_j["app"] == "com.tencent.miniapp_01"
        and data_j["meta"]["detail_1"]["appid"] == "1109937557"
    ):
        title = data_j["meta"]["detail_1"]["desc"]
        url_raw = data_j["meta"]["detail_1"]["qqdocurl"]

        # 获取实际BV号的URL
        response = requests.get(url_raw, proxies=PROXIES)
        headers = response.history[0].headers
        url = headers["Location"]
        url = url[: url.find("?")]

        await bot.send(event, f"【{title}】\n{url}")
