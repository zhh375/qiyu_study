import os
import qianfan
from config import QIANFAN_ACCESS_KEY, QIANFAN_SECRET_KEY


os.environ["QIANFAN_ACCESS_KEY"] = QIANFAN_ACCESS_KEY
os.environ["QIANFAN_SECRET_KEY"] = QIANFAN_SECRET_KEY


def qianfan_chat(word_list, type_chat=0):
    if type_chat == 0:
        content = "用下面的汉字和笔画较少的汉字组一个不少于10个字且不超过20个字的短句：" + " ".join(word_list)
    else:
        content = "用下面的汉字和笔画较少的汉字组一个不超过50个字的故事：" + " ".join(word_list)
    chat_comp = qianfan.ChatCompletion()
    resp = chat_comp.do(model="ERNIE-3.5-8K", messages=[{
        "role": "user",
        "content": content
    }]).body
    if "result" in resp:
        return resp["result"].split("\n")[0]
    else:
        return "失败了..."


if __name__ == '__main__':
    result = qianfan_chat(["你好", "世界"], 0)
    print(result)
