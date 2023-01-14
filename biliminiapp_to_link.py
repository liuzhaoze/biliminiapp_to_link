from hoshino import Service
from aiocqhttp.event import Event
import ujson
import requests

sv = Service('biliminiapp', enable_on_default=True, help_='Bilibili小程序转链接')


@sv.on_message('group')
async def biliminiapp_to_link(bot, event: Event):
    msg = str(event.message)
    data = msg[msg.find('data=') + len('data='): -1].replace('&#44;', ',')  # 获取小程序 JSON 信息
    try:
        data_j = ujson.loads(data)
    except ujson.JSONDecodeError:
        return # 非小程序信息，函数返回

    # 提取视频标题及URL
    if type(data_j) == dict and data_j['app'] == 'com.tencent.miniapp_01' and data_j['meta']['detail_1']['title'] == '哔哩哔哩':
        title = data_j['meta']['detail_1']['desc']
        url_raw = data_j['meta']['detail_1']['qqdocurl']

        # 获取实际BV号的URL
        response = requests.get(url_raw)
        headers = response.history[0].headers
        url = headers['Location']
        url = url[:url.find('?')]

        await bot.send(event, f'【{title}】\n{url}')
