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
os.environ['WERKZEUG_RUN_MAIN'] = "true"                # ȥ��flask��������ʾ
logging.getLogger('werkzeug').setLevel(logging.ERROR)   # ȥ��flask����־

#-----------


#1107099465,247948153��2149508211

admin=[1356720321,1107099465]
cbot=False
q=False
an=False
quee=""
def readcsv():
    global rawdata
    global head_row
    with open("1.csv") as f:#����dict
        #1.�����Ķ�������
        reader = csv.reader(f)
        #2.��ȡ�ļ���һ������
        head_row=next(reader)
        for i in (head_row):
            print ((i).decode("utf-8").encode("gbk"))#str utf-8
        for i in reader:
            rawdata[i[0]]=i

def findcsv(str1):#���ؿ���û���ҵ�
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
        'message':unicode(content,"gbk")   # ʾ��1 ����Ⱥ��Ϣ����@ĳ��
        # 'message':f'[CQ:image,file=base64://xxx]'     # ʾ��2 ͨ��ͼƬ��base64�뷢��ͼƬ ��ͼƬ����base64���аٶȣ�
        # 'message':f'[CQ:image,file=http://xxx]'       # ʾ��3 ��������ͼƬ
    }                                                   # ��������ͬ�� �����������ܺ��κ�������Ϣͬʱ��
    r = requests.get(apiUrl,params=data)                      # �������Ҫ�������״̬����Ͳ���д�� ���ͳ�ȥ������
    print (r.url)


def send_group_message(ide,content):
    cqAddress = 'http://127.0.0.1:8900'
    sendMsgApi = '/send_group_msg'#_rate_limited
    apiUrl = cqAddress + sendMsgApi
    data = {
        'group_id':str(ide),
        'message':unicode(content,"gbk")   # ʾ��1 ����Ⱥ��Ϣ����@ĳ��
        # 'message':f'[CQ:image,file=base64://xxx]'     # ʾ��2 ͨ��ͼƬ��base64�뷢��ͼƬ ��ͼƬ����base64���аٶȣ�
        # 'message':f'[CQ:image,file=http://xxx]'       # ʾ��3 ��������ͼƬ
    }                                                   # ��������ͬ�� �����������ܺ��κ�������Ϣͬʱ��
    r = requests.get(apiUrl,params=data)                      # �������Ҫ�������״̬����Ͳ���д�� ���ͳ�ȥ������
    print (r.url)
    # ......

def getreadbot(q):
    cqAddress = 'http://127.0.0.1:8898'
    sendMsgApi = '/get?msg='+q
    apiUrl = cqAddress + sendMsgApi
                                                     # ��������ͬ�� �����������ܺ��κ�������Ϣͬʱ��
    r = requests.get(apiUrl)                      # �������Ҫ�������״̬����Ͳ���д�� ���ͳ�ȥ������
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
    # ��������Ҫ����Ϣ��ȡ����Ϣ�Ĵ��� ��ȡ��Ϣ����/������/Ⱥ������ Ȼ�������Ϣ���ظ���Ϣ
    global admin
    global cbot
    global q
    global quee
    global an
    print ("RAW")
    print (data)
    print ("raw")
    if data:
        selfId = data.get('self_id')#���˺�qq��
        #print ("������QQ:"+str(selfId))
        na=data.get('sender').get("nickname")
        
        userId = data.get('user_id')
        try:
            print ("������QQ:"+str(userId)+" ��:"+na.encode("gbk"))
        except:
            print ("������QQ:"+str(userId))
        subType = data.get('sub_type')
        #print ("����������:"+str(subType))
        #groupId = data.get('group_id')
        
        
        
        postType = data.get('post_type')                    # ������������������ж���Ϣ���� Ⱥ��Ϣ/˽����Ϣ/֪ͨ/����
        #print ("������������:"+str(postType))
        messageType = data.get('message_type')
        ti=data.get('time')
        ti=time.localtime(ti)
        ti = time.strftime("%Y--%m--%d %H:%M:%S", ti)
        #print ("����ʱ��:"+str(ti))
        # ��Ϣ���� /��Ϣ��һ���б�Ƕ���ֵ����ʽ�����忴CQhttp���ĵ�
        message = data.get('message')
        if message:
            print (u"��Ϣ��Ϣ:".encode("gbk")+message.encode("gbk"))

        if("normal" in subType.encode("gbk")):
            tarq=data.get(u'group_id')
        
        
        if(userId in admin):
            
            if   (unicode("�ʴ�ѧϰ�ر�","gbk") in message):
                if "normal" in subType.encode("gbk"):#��Ⱥ
                    send_group_message(tarq,"��ѧ�˲�ѧ��")
                else:
                    send_private_message(userId,"��ѧ�˲�ѧ��")
                
                cbot=False
                an=False
                q=False
                return
            
            
            if cbot:#�ʴ�ѧϰ
                quee=message
                if "normal" in subType.encode("gbk"):#��Ⱥ
                    send_group_message(tarq,getreadbot(message).decode("utf-8").encode("gbk"))
                    time.sleep(2)
                    send_group_message(tarq,"����Ǵ��𣿡��ǵ�/���ǡ�")
                    cbot=False
                    q=True
                else:
                    send_private_message(userId,getreadbot(message).decode("utf-8").encode("gbk"))
                    time.sleep(2)
                    send_private_message(userId,"����Ǵ��𣿡��ǵ�/���ǡ�")
                    cbot=False
                    q=True
                return
            if  q:#�Ƿ�
                if   (unicode("����","gbk") in message):
                    if "normal" in subType.encode("gbk"):#��Ⱥ
                        send_group_message(tarq,"����ȷ����ʲô�أ�")
                        
                    else:
                        send_private_message(userId,"����ȷ����ʲô�أ�")
                    an=True
                    q=False
                else:
                    an=False
                    q=False
                    cbot=True
                return
            if an:#botlea
                if "normal" in subType.encode("gbk"):#��Ⱥ
                    send_group_message(tarq,botlea(quee,message).decode("utf-8").encode("gbk"))
                else:
                    send_private_message(userId,botlea(quee,message).decode("utf-8").encode("gbk"))
                
                an=False
                q=False
                cbot=True
                return
                
                    
            if   (unicode("�ʴ�ѧϰ","gbk") in message):
                if "normal" in subType.encode("gbk"):#��Ⱥ
                    send_group_message(tarq,"������Ҫѧϰ����")
                else:
                    send_private_message(userId,"������Ҫѧϰ����")
                cbot=True
                an=False
                q=False
                return
            
            #[CQ:at,qq=1264104754]
        if   (unicode("[CQ:at,qq=1343498018] ","gbk") in message) or (unicode("@��ϷС����@��������Ŷ","gbk") in message):
            message=(message).encode("gbk").replace("[CQ:at,qq=1343498018]","")
            message=(message).replace("@��ϷС����@��������Ŷ","")
            message=message.strip()
            if ("�Ĵ���" in message):
                x=message.split("�Ĵ���")[0]
                y=message.split("�Ĵ���")[1]
                if "normal" in subType.encode("gbk"):#��Ⱥ
                    send_group_message(tarq,botlea(unicode(x,"gbk"),unicode(y,"gbk")).decode("utf-8").encode("gbk"))
                else:
                    send_private_message(userId,botlea(unicode(x,"gbk"),unicode(y,"gbk")).decode("utf-8").encode("gbk"))
                
                return
            if "normal" in subType.encode("gbk"):#��Ⱥ
                send_group_message(tarq,getreadbot(unicode(message,"gbk")).decode("utf-8").encode("gbk"))
            else:
                send_private_message(userId,getreadbot(unicode(message,"gbk")).decode("utf-8").encode("gbk"))
            
            
        
             
            
            
                
            

            
            
    # ��Ϣ���� ������ĳ������ ������/����/ͼƬ �� ʡ��


"""
���� ��Ϣ����/����
����API�뿴CQhttp���ĵ��� ��һ������������Ϣ�󣬵��÷���/������Ϣ��API��������Ӧ��
ĳЩ��Ϣ����ͼƬ��@ �ȣ���Ҫʹ��CQ�뷢�ͣ�Ҳ�뿴�ĵ�
"""





@app.route('/message', methods=["POST"])                # ָ����Ϣ���յ�uri·�����޶�Ϊhttp POST
def handle_message():
    data = request.get_data().decode('utf-8')           # ����http��Ϣ������Ϊutf-8
    data = json.loads(data)                             # ����Ϣת��Ϊ�ֵ䣨dict��
    threading.Thread(target=parse_message, args=(data,)).start()  # ��Ϣ���� �Ƽ�ʹ�ö��̣߳�����100%�����������
    return ''                                           # �����з��أ�������������


app.run(host='127.0.0.1', port=8010)                      # ���� �������õĻ���cq������ post_url ����http://127.0.0.1:5001/message




"""
���� ��Ϣ�Ĵ���
ͨ�����post����ԭʼ���ݣ���ȡpost type,sub type,message type ���ж���Ϣ������ Ⱥ��Ϣ/˽����Ϣ/֪ͨ/����
Ȼ�������Ϣ�����ͽ��д���
ͬʱ����Ҫ��ȡ��Ⱥ�ţ�qq�ŵ����ݣ����ڻظ���Ϣ��
"""

# ����ʾ��һ����Ϣ������


"""
�ġ� ��ʱ����
�����Ҫ��ʱ���񣬿�����httpServer ����ǰ����һ����ʱ�����߳� (��ΪhttpServer���л��������̣߳����º�����벻������)
������ע�⣬������һ��Ҫ���ã���Ȼһ��������ʱ������߳̾ͱ���
"""

# ��ʱ����ʾ��
def run_jobs():
    schedule.every().day.at('00:01').do(send_like_job)  # ����һ����ʱ���� ÿ��0��1��ִ��
    # ... ͬ���ɶ����� ʡ�� ����д�������аٶ� schedule ģ��
    while True:
        schedule.run_pending()
        sleep(59)


def send_like_job():                                    # дһ����������ȫȺ��Ա����
    groupMembers = get_group_members('12345')           # ����Ⱥ�� ����Ⱥ��Ա��qq
    for member in groupMembers:
        send_like(member)                               # ���������Լ�д�� send_like ����
        sleep(3)                                        # ��������һ��Ҫ�ʵ�����Ƶ�� ��Ȼ�������ױ�����


def get_group_members(group):
    # ʡ�� ���е���api ����һ��ȫȺ��Աqq�ŵ�list����
    return ['1111','2222']





# ���ж�ʱ���� ��ע��Ҫ�ŵ� httpServer����֮ǰ

# app = HTTPServer(('0.0.0.0',5001),Resquest)
# threading.Thread(target=run_job).start()
# app.serve_forever()


