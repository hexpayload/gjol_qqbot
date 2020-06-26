#-*-coding:gb2312-*-
import requests
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from flask import Flask, request
import json
import logging
import os
import threading
import schedule
from time import sleep
import redis
from datetime import datetime,timedelta
import chardet
import sys
import traceback
import csv


app = Flask(__name__)
os.environ['WERKZEUG_RUN_MAIN'] = "true"                # 去除flask的启动提示
logging.getLogger('werkzeug').setLevel(logging.ERROR)   # 去除flask的日志

#-----------


#1107099465,247948153，2149508211

admin=[1356720321,1107099465]
cbot=False
q=False
an=False
quee=""
def readcsv():
    global rawdata
    global head_row
    with open("1.csv") as f:#读入dict
        #1.创建阅读器对象
        reader = csv.reader(f)
        #2.读取文件第一行数据
        head_row=next(reader)
        for i in (head_row):
            print ((i).decode("utf-8").encode("gbk"))#str utf-8
        for i in reader:
            rawdata[i[0]]=i

def findcsv(str1):#返回空则没有找到
    str1=str1.decode("gbk").encode("utf-8")
    for i in rawdata:
        if str1 in i:
            return rawdata[i]
    return

def send_private_message(userid,content):
    cqAddress = 'http://127.0.0.1:8900'
    sendMsgApi = '/send_private_msg'#_rate_limited
    apiUrl = cqAddress + sendMsgApi
    data = {
        'user_id':str(userid),
        'message':unicode(content,"gbk")   # 示例1 发送群消息，并@某人
        # 'message':f'[CQ:image,file=base64://xxx]'     # 示例2 通过图片的base64码发送图片 （图片编码base64自行百度）
        # 'message':f'[CQ:image,file=http://xxx]'       # 示例3 发送网络图片
    }                                                   # 发送语音同理 但是语音不能和任何其他消息同时发
    r = requests.get(apiUrl,params=data)                      # 如果不需要插件返回状态下面就不用写了 发送出去就完事
    print (r.url)


def send_group_message(ide,content):
    cqAddress = 'http://127.0.0.1:8900'
    sendMsgApi = '/send_group_msg'#_rate_limited
    apiUrl = cqAddress + sendMsgApi
    data = {
        'group_id':str(ide),
        'message':unicode(content,"gbk")   # 示例1 发送群消息，并@某人
        # 'message':f'[CQ:image,file=base64://xxx]'     # 示例2 通过图片的base64码发送图片 （图片编码base64自行百度）
        # 'message':f'[CQ:image,file=http://xxx]'       # 示例3 发送网络图片
    }                                                   # 发送语音同理 但是语音不能和任何其他消息同时发
    r = requests.get(apiUrl,params=data)                      # 如果不需要插件返回状态下面就不用写了 发送出去就完事
    print (r.url)
    # ......

def getreadbot(q):
    cqAddress = 'http://127.0.0.1:8898'
    sendMsgApi = '/get?msg='+q
    apiUrl = cqAddress + sendMsgApi
                                                     # 发送语音同理 但是语音不能和任何其他消息同时发
    r = requests.get(apiUrl)                      # 如果不需要插件返回状态下面就不用写了 发送出去就完事
    return r.content
    # ......

#----------
def botlea(q,a):
    cqAddress = 'http://127.0.0.1:8898'
    sendMsgApi = '/lea?ans='+a+"&que="+q
    apiUrl = cqAddress + sendMsgApi
                                                    
    r = requests.get(apiUrl)                    
    return r.content
    # ......


    

def parse_message(data):
    # 方法里主要是消息提取和消息的处理 提取消息类型/发送人/群聊名等 然后根据消息，回复信息
    global admin
    global cbot
    global q
    global quee
    global an
    print ("RAW")
    print (data)
    print ("raw")
    if data:
        selfId = data.get('self_id')#本账号qq号
        #print ("接收者QQ:"+str(selfId))
        na=data.get('sender').get("nickname")
        
        userId = data.get('user_id')
        try:
            print ("发送者QQ:"+str(userId)+" 名:"+na.encode("gbk"))
        except:
            print ("发送者QQ:"+str(userId))
        subType = data.get('sub_type')
        #print ("发送者性质:"+str(subType))
        #groupId = data.get('group_id')
        
        
        
        postType = data.get('post_type')                    # 根据这个及下面两个判断消息类型 群消息/私人消息/通知/请求
        #print ("发送内容性质:"+str(postType))
        messageType = data.get('message_type')
        ti=data.get('time')
        ti=time.localtime(ti)
        ti = time.strftime("%Y--%m--%d %H:%M:%S", ti)
        #print ("发送时间:"+str(ti))
        # 消息解析 /消息是一个列表嵌套字典的形式，具体看CQhttp的文档
        message = data.get('message')
        if message:
            print (u"消息信息:".encode("gbk")+message.encode("gbk"))

        if("normal" in subType.encode("gbk")):
            tarq=data.get(u'group_id')
        
        
        if(userId in admin):
            
            if   (unicode("问答学习关闭","gbk") in message):
                if "normal" in subType.encode("gbk"):#是群
                    send_group_message(tarq,"不学了不学了")
                else:
                    send_private_message(userId,"不学了不学了")
                
                cbot=False
                an=False
                q=False
                return
            
            
            if cbot:#问答学习
                quee=message
                if "normal" in subType.encode("gbk"):#是群
                    send_group_message(tarq,getreadbot(message).decode("utf-8").encode("gbk"))
                    time.sleep(2)
                    send_group_message(tarq,"这个是答案吗？【是得/不是】")
                    cbot=False
                    q=True
                else:
                    send_private_message(userId,getreadbot(message).decode("utf-8").encode("gbk"))
                    time.sleep(2)
                    send_private_message(userId,"这个是答案吗？【是得/不是】")
                    cbot=False
                    q=True
                return
            if  q:#是否
                if   (unicode("不是","gbk") in message):
                    if "normal" in subType.encode("gbk"):#是群
                        send_group_message(tarq,"那正确答案是什么呢？")
                        
                    else:
                        send_private_message(userId,"那正确答案是什么呢？")
                    an=True
                    q=False
                else:
                    an=False
                    q=False
                    cbot=True
                return
            if an:#botlea
                if "normal" in subType.encode("gbk"):#是群
                    send_group_message(tarq,botlea(quee,message).decode("utf-8").encode("gbk"))
                else:
                    send_private_message(userId,botlea(quee,message).decode("utf-8").encode("gbk"))
                
                an=False
                q=False
                cbot=True
                return
                
                    
            if   (unicode("问答学习","gbk") in message):
                if "normal" in subType.encode("gbk"):#是群
                    send_group_message(tarq,"接下来要学习了噢")
                else:
                    send_private_message(userId,"接下来要学习了噢")
                cbot=True
                an=False
                q=False
                return
            
            #[CQ:at,qq=1264104754]
        if   (unicode("[CQ:at,qq=1343498018] ","gbk") in message) or (unicode("@游戏小助手@我问问题哦","gbk") in message):
            message=(message).encode("gbk").replace("[CQ:at,qq=1343498018]","")
            message=(message).replace("@游戏小助手@我问问题哦","")
            message=message.strip()
            if ("的答案是" in message):
                x=message.split("的答案是")[0]
                y=message.split("的答案是")[1]
                if "normal" in subType.encode("gbk"):#是群
                    send_group_message(tarq,botlea(unicode(x,"gbk"),unicode(y,"gbk")).decode("utf-8").encode("gbk"))
                else:
                    send_private_message(userId,botlea(unicode(x,"gbk"),unicode(y,"gbk")).decode("utf-8").encode("gbk"))
                
                return
            if "normal" in subType.encode("gbk"):#是群
                send_group_message(tarq,getreadbot(unicode(message,"gbk")).decode("utf-8").encode("gbk"))
            else:
                send_private_message(userId,getreadbot(unicode(message,"gbk")).decode("utf-8").encode("gbk"))
            
            
        
             
            
            
                
            

            
            
    # 消息处理 若满足某条件则 发文字/语音/图片 等 省略


"""
三、 消息发送/处理
具体API请看CQhttp的文档。 上一步处理完了消息后，调用发送/处理消息的API，进行响应。
某些消息，如图片，@ 等，需要使用CQ码发送，也请看文档
"""





@app.route('/message', methods=["POST"])                # 指定消息接收的uri路径，限定为http POST
def handle_message():
    data = request.get_data().decode('utf-8')           # 接收http消息并编码为utf-8
    data = json.loads(data)                             # 把消息转化为字典（dict）
    threading.Thread(target=parse_message, args=(data,)).start()  # 消息处理 推荐使用多线程，可以100%解决假死问题
    return ''                                           # 必须有返回，返回内容随意


app.run(host='127.0.0.1', port=8010)                      # 运行 这样配置的话，cq插件里的 post_url 就是http://127.0.0.1:5001/message




"""
二、 消息的处理
通过插件post来的原始数据，提取post type,sub type,message type 来判断消息的类型 群消息/私人消息/通知/请求
然后根据消息的类型进行处理
同时，需要提取如群号，qq号等数据，用于回复消息。
"""

# 这里示例一个消息处理方法


"""
四、 定时任务
如果需要定时任务，可以在httpServer 运行前，开一个定时任务线程 (因为httpServer运行会阻塞主线程，导致后面代码不会运行)
但是请注意，错误处理一定要做好，不然一旦出错，定时任务的线程就崩了
"""

# 定时任务示例
def run_jobs():
    schedule.every().day.at('00:01').do(send_like_job)  # 定义一个定时任务 每天0点1分执行
    # ... 同样可定义多个 省略 其他写法请自行百度 schedule 模块
    while True:
        schedule.run_pending()
        sleep(59)


def send_like_job():                                    # 写一个方法，给全群人员点赞
    groupMembers = get_group_members('12345')           # 传入群号 返回群成员的qq
    for member in groupMembers:
        send_like(member)                               # 调用下面自己写的 send_like 方法
        sleep(3)                                        # 大量任务一定要适当控制频率 不然极其容易被限制


def get_group_members(group):
    # 省略 自行调用api 返回一个全群成员qq号的list即可
    return ['1111','2222']





# 运行定时任务 请注意要放到 httpServer运行之前

# app = HTTPServer(('0.0.0.0',5001),Resquest)
# threading.Thread(target=run_job).start()
# app.serve_forever()


