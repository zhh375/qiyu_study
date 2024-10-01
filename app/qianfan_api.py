import requests
import json
from config import QIANFAN_ACCESS_KEY, QIANFAN_SECRET_KEY


def get_access_token():
    url = ("https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}"
           .format(QIANFAN_ACCESS_KEY, QIANFAN_SECRET_KEY))
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


def qianfan_chat(word_list, type_chat=0):
    url = ("https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions?access_token=" + get_access_token())
    if type_chat == 0:
        content = "用下面的汉字和笔画较少的汉字组一个不少于10个字且不超过20个字的短句：" + " ".join(word_list[0])
    else:
        content = "用下面的汉字和笔画较少的汉字组一个不超过50个字的故事：" + " ".join(word_list)
    payload = json.dumps({"messages": [{"role": "user", "content": content}]})
    headers = {'Content-Type': 'application/json'}
    resp = requests.request("POST", url, headers=headers, data=payload).json()

    if "result" in resp:
        return resp["result"].split("\n")[0]
    else:
        return "失败了..."


if __name__ == '__main__':
    result = qianfan_chat(["你好", "世界"], 0)
    print(result)
