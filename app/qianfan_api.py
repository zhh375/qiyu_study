import requests
import json
import time
from config import QIANFAN_ACCESS_KEY, QIANFAN_SECRET_KEY, QIANFAN_IMAGE_ACCESS_KEY, QIANFAN_IMAGE_SECRET_KEY


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


def get_image_access_token():
    url = ("https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}"
           .format(QIANFAN_IMAGE_ACCESS_KEY, QIANFAN_IMAGE_SECRET_KEY))
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


def qianfan_image(prompt):
    url = ("https://aip.baidubce.com/rpc/2.0/ernievilg/v1/txt2imgv2?access_token=" + get_image_access_token())
    payload = json.dumps({"prompt": prompt, "width": 1024, "height": 1024, "task_time_out": 10})
    headers = {'Content-Type': 'application/json'}
    resp = requests.request("POST", url, headers=headers, data=payload).json()

    if "data" in resp and "task_id" in resp["data"] and resp["data"]["task_id"] != "":
        url = ("https://aip.baidubce.com/rpc/2.0/ernievilg/v1/getImgv2?access_token=" + get_image_access_token())
        payload = json.dumps({"task_id": resp["data"]["task_id"]})
        headers = {'Content-Type': 'application/json'}
        resp = requests.request("POST", url, headers=headers, data=payload).json()
        time_start = time.time()
        time_stop = time.time()
        while time_stop < time_start + 30:
            time.sleep(2)
            if "data" in resp and "task_status" in resp["data"]:
                if resp["data"]["task_status"] == "SUCCESS":
                    if "sub_task_result_list" in resp["data"] and len(resp["data"]["sub_task_result_list"])>0:
                        if "final_image_list" in resp["data"]["sub_task_result_list"][0] and len(resp["data"]["sub_task_result_list"][0]["final_image_list"])>0:
                            if "img_url" in resp["data"]["sub_task_result_list"][0]["final_image_list"][0]:
                                return resp["data"]["sub_task_result_list"][0]["final_image_list"][0]["img_url"]
                            else:
                                return "失败了..."
                        else:
                            return "失败了..."
                    else:
                        return "失败了..."
                elif resp["data"]["task_status"] == "FAILED":
                    return "失败了..."
            else:
                return "失败了..."
            resp = requests.request("POST", url, headers=headers, data=payload).json()
            time_stop = time.time()
        else:
            return "失败了..."

    else:
        return "失败了..."


if __name__ == '__main__':
    result = qianfan_chat(["你好", "世界"], 0)
    print(result)
