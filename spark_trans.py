#!/usr/bin/env python 
# -*- coding:utf-8 -*-

#
# 机器翻译2.0(niutrans) WebAPI 接口调用示例
# 运行前：请先填写Appid、APIKey、APISecret
# 运行方法：直接运行 main 即可 
# 结果： 控制台输出结果信息
# 
# 1.接口文档（必看）：https://www.xfyun.cn/doc/nlp/niutrans/API.html
# 2.错误码链接：https://www.xfyun.cn/document/error-code （错误码code为5位数字）
# 3.个性化翻译术语自定义：
#   登陆开放平台 https://www.xfyun.cn/
#   在控制台--机器翻译(niutrans)--自定义翻译处
#   上传自定义翻译文件（打开上传或更新窗口，可下载示例文件）
#

import requests
import datetime
import hashlib
import base64
import hmac
import json
import sys

class get_result(object):
    def __init__(self,host):
        # 应用ID（到控制台获取）
        self.APPID = "1"
        # 接口APISercet（到控制台机器翻译服务页面获取）
        self.Secret = "YTIyOGQ5zI4ZTI0ZGRm"
        # 接口APIKey（到控制台机器翻译服务页面获取）
        self.APIKey= "40b7feb52dc87ae9"
        
        
        # 以下为POST请求
        self.Host = host
        self.RequestUri = "/v2/ots"
        # 设置url
        # print(host)
        self.url="https://"+host+self.RequestUri
        self.HttpMethod = "POST"
        self.Algorithm = "hmac-sha256"
        self.HttpProto = "HTTP/1.1"

        # 设置当前时间
        curTime_utc = datetime.datetime.utcnow()
        self.Date = self.httpdate(curTime_utc)
        # 设置业务参数
        # 语种列表参数值请参照接口文档：https://www.xfyun.cn/doc/nlp/niutrans/API.html
        self.Text="How old are you"
        self.BusinessArgs={
                "from": "en",
                "to": "cn",
            }

    def hashlib_256(self, res):
        m = hashlib.sha256(bytes(res.encode(encoding='utf-8'))).digest()
        result = "SHA-256=" + base64.b64encode(m).decode(encoding='utf-8')
        return result

    def httpdate(self, dt):
        """
        Return a string representation of a date according to RFC 1123
        (HTTP/1.1).

        The supplied date must be in UTC.

        """
        weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
                 "Oct", "Nov", "Dec"][dt.month - 1]
        return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
                                                        dt.year, dt.hour, dt.minute, dt.second)

    def generateSignature(self, digest):
        signatureStr = "host: " + self.Host + "\n"
        signatureStr += "date: " + self.Date + "\n"
        signatureStr += self.HttpMethod + " " + self.RequestUri \
                        + " " + self.HttpProto + "\n"
        signatureStr += "digest: " + digest
        signature = hmac.new(bytes(self.Secret.encode(encoding='utf-8')),
                             bytes(signatureStr.encode(encoding='utf-8')),
                             digestmod=hashlib.sha256).digest()
        result = base64.b64encode(signature)
        return result.decode(encoding='utf-8')

    def init_header(self, data):
        digest = self.hashlib_256(data)
        #print(digest)
        sign = self.generateSignature(digest)
        authHeader = 'api_key="%s", algorithm="%s", ' \
                     'headers="host date request-line digest", ' \
                     'signature="%s"' \
                     % (self.APIKey, self.Algorithm, sign)
        #print(authHeader)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Method": "POST",
            "Host": self.Host,
            "Date": self.Date,
            "Digest": digest,
            "Authorization": authHeader
        }
        return headers

    def get_body(self):
        content = str(base64.b64encode(self.Text.encode('utf-8')), 'utf-8')
        postdata = {
            "common": {"app_id": self.APPID},
            "business": self.BusinessArgs,
            "data": {
                "text": content,
            }
        }
        body = json.dumps(postdata)
        #print(body)
        return body

    def call_url(self):
        if self.APPID == '' or self.APIKey == '' or self.Secret == '':
            print('Appid 或APIKey 或APISecret 为空！请打开demo代码，填写相关信息。')
        else:
            code = 0
            body=self.get_body()
            headers=self.init_header(body)
            #print(self.url)
            response = requests.post(self.url, data=body, headers=headers,timeout=8)
            status_code = response.status_code
            #print(response.content)
            if status_code!=200:
                # 鉴权失败
                print("Http请求失败，状态码：" + str(status_code) + "，错误信息：" + response.text)
                print("请根据错误信息检查代码，接口文档：https://www.xfyun.cn/doc/nlp/niutrans/API.html")
            else:
                # 鉴权成功
                respData = json.loads(response.text)
                #print(respData)
                print("翻译结果：")
                print(respData["data"]["result"]["trans_result"]["dst"]);
                # 以下仅用于调试
                # code = str(respData["code"])
                # if code!='0':
                #     print("请前往https://www.xfyun.cn/document/error-code?code=" + code + "查询解决办法")



if __name__ == '__main__':
    ## 示例: host="ntrans.xfyun.cn"域名形式
    host = "ntrans.xfyun.cn"
    # 初始化类
    gClass = get_result(host)

    # 检查是否通过管道输入
    if not sys.stdin.isatty():
        # 从标准输入读取内容
        text_to_translate = sys.stdin.read().strip()
        if not text_to_translate:
            print("输入内容为空，请提供需要翻译的文本。")
            sys.exit(1)

        # 默认源语言为英文，目标语言为中文
        source_language = "en"
        target_language = "cn"

        # 更新翻译内容和语言参数
        gClass.Text = text_to_translate
        gClass.BusinessArgs = {
            "from": source_language,
            "to": target_language,
        }

        # 调用翻译接口
        gClass.call_url()
    else:
        print("请通过管道输入内容，例如：cat README | python3 WebOTS.py")

# if __name__ == '__main__':
#     ## 示例: host="ntrans.xfyun.cn"域名形式
#     host = "ntrans.xfyun.cn"
#     # 初始化类
#     gClass = get_result(host)

#     while True:
#         # 提示用户输入翻译内容
#         text_to_translate = input("请输入需要翻译的内容（输入 q 退出）：\n> ")
#         if text_to_translate.strip().lower() == 'q':
#             print("退出程序。")
#             break

#         # 提示用户输入源语言
#         source_language = input("请输入源语言代码（例如 'en' 表示英文）：\n> ").strip()
#         if not source_language:
#             source_language = "en"  # 默认英文

#         # 提示用户输入目标语言
#         target_language = input("请输入目标语言代码（例如 'cn' 表示中文）：\n> ").strip()
#         if not target_language:
#             target_language = "cn"  # 默认中文

#         # 更新翻译内容和语言参数
#         gClass.Text = text_to_translate
#         gClass.BusinessArgs = {
#             "from": source_language,
#             "to": target_language,
#         }

#         # 调用翻译接口
#         gClass.call_url()
