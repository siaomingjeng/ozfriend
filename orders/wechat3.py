import requests
import json
import urllib
import socket


message = 'Test Message using Requests on Python3!'


def send_wechat(message=message):
    message = socket.gethostname() + '\n' + message
    touser = 'xiaomingjeng|meigong'  # '|' split more users, '@all' for all.
    url_raw = 'https://qyapi.weixin.qq.com/cgi-bin'
    corpid = 'wxfc188285b26f1305'
    secret = 'ThcfEnlKkJGF-V82zz1507Occ9o4X__KwL2PZkhkjXI'
    agentid = '1000003'
    url = url_raw + '/gettoken?' +\
        urllib.parse.urlencode({'corpid': corpid, 'corpsecret': secret})
    data = json.dumps({'touser': touser,   # 'toparty': toparty,
                       'msgtype': "text", 'agentid': agentid,
                       'text': {'content': message}, 'safe': "0"},
                      ensure_ascii=False).encode("utf-8")
    result = "ERROR"
    try:
        res = requests.get(url)
        content = json.loads(res.content)
        url2 = url_raw + '/message/send?access_token=%s' %\
            content['access_token']
        result = requests.post(url2, data)
    except Exception as e:
            result = e
    finally:
        return result

if __name__ == '__main__':
    print(send_wechat(message="中文测试"))
