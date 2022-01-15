# -*- coding: utf-8 -*-

from maxgie import *
from akad.ttypes import Message
from akad.ttypes import ContentType as Type
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib.request, urllib.parse, urllib.error, urllib.parse
from gtts import gTTS
#==============================================================================#
botStart = time.time()
#==============================================================================#
cl = LINE()


bot1 = cl.getProfile().mid
clgp = cl.getProfile()
keyword = {"kw":{",":"on"}}
pictureStatus = clgp.pictureStatus
oepoll = OEPoll(cl)
settingsOpen = codecs.open("71.json","r","utf-8")
settings = json.load(settingsOpen)
protectkick = []
protectqr = []
protectinvite = []
Reader = {"readRom":{}}
menu = """คำสั่งทั้งหมด

คำสั่งทั่วไป
- me ส่งคอนแทค
- contact @ ขโมยคอนแทค
- help ดูคำสั่งทั้งหมด
- myid ส่ง mid
- gid ส่ง group id
- gift ส่งของขวัญ
- info @ ขโมยรูป ชื่อ
- addfriend @ เพิ่มเพื่อน
- delfriend @ ลบเพื่อน
- test เช็คว่าทำงานไหม
- pro (ข้อความ) ส่งข้อความไปทุกกลุ่ม
- picall ขโมยรูปสมาชิกทั้งหมดในกลุ่ม
- speed ทดสอบความเร็ว
- reject (ข้อความ) ปฏิเสธการเชิญเข้าร่วมกลุ่ม
- qrcode (ข้อความ) เปลี่ยนข้อความเป็น QR code
- gc ส่งคอนแทคคนสร้างกลุ่ม
- talk (ข้อความ) เสียงสิริ
- uptime ดูเวลาการใช้งาน
- fc (ข้อความ[English เท่านั้น]) สร้างรูป fc
- mul (จำนวน) (จำนวน) คูณเลข
- tagall แท็กสมาชิกทั้งหมด
- number (จำนวน) นับเลข
- print (ข้อความ) สร้างรูป
- bye @ เตะคนในกลุ่ม
- kick @ เตะล้างแชทคนในกลุ่ม
- creator ผู้สร้าง

เช็คคนอ่าน
- reader เช็คคนแอบอ่าน

คำสั่งตอบกลับอัตโนมัติ
- keyadd [คีย์เวิร์ด];;[คำตอบ] เพิ่มการตอบอัตโนมัติ
- keydel [คีย์เวิร์ด] ลบการตอบอัตโนมัติ
- checkkey เช็คการตอบ
- resetkey รีเซ็ตการตอบ

คำสั่งตั้งค่า
- name (ชื่อใหม่) เปลี่ยนชื่อ
- wc on/off เปิด/ปิด ข้อความต้อนรับ
- lv on/off เปิด/ปิด ข้อความบอกลา
- wcset (ข้อความ) ตั้งข้อความต้อนรับ
- lvset (ข้อความ) ตั้งข้อความบอกลา
- surveywc เช็คข้อความต้อนรับ
- surveylv เช็คข้อความบอกลา
- block on/off เปิด/ปิด ออโต้บล็อค
- url on/off เปิด/ปิด URL กลุ่ม
- autoout on/off เปิด/ปิด ปฏิเสธการเข้ากลุ่ม

ระบบป้องกัน (แยกกลุ่ม)
- protectkick on/off เปิด/ปิด โหมดห้ามลบ
- protecturl on/off เปิด/ปิด โหมดป้องกัน URL
- protectinv on/off เปิด/ปิด โหมดป้องกันการเชิญ"""

botStart = time.time()
def logError(text):
    cl.log("ERROR:" + str(text))
    time_ = datetime.now()
    with open("errorLog.txt","a") as error:
        error.write("\n[%s] %s" % (str(time), text))

def sendflex(to, data):
    n1 = LiffChatContext(to)
    n2 = LiffContext(chat=n1)
    view = LiffViewRequest('1602687308-GXq4Vvk9', n2)
    token = cl.issueLiffView(view)
    url = 'https://api.line.me/message/v3/share'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % token.accessToken
    }
    data = {"messages":[data]}
    requests.post(url, headers=headers, data=json.dumps(data))
def timeChange(secs):
    mins, secs = divmod(secs,60)
    hours, mins = divmod(mins,60)
    days, hours = divmod(hours,24)
    weeks, days = divmod(days,7)
    months, weeks = divmod(weeks,4)
    text = ""
    if months != 0: text += "%02d เดือน" % (months)
    if weeks != 0: text += " %02d สัปดาห์" % (weeks)
    if days != 0: text += " %02d วัน" % (days)
    if hours !=  0: text +=  " %02d ชั่วโมง" % (hours)
    if mins != 0: text += " %02d นาที" % (mins)
    if secs != 0: text += " %02d วินาที" % (secs)
    if text[0] == " ":
            text = text[1:]
    return text
def mentionReader(to, mids=[], result=''):
    parsed_len = len(mids)//20+1
    mention = '@zeroxyuuki\n'
    no = 0
    for point in range(parsed_len):
        mentionees = []
        for mid in mids[point*20:(point+1)*20]:
            no += 1
            result += '%i. %s' % (no, mention)
            slen = len(result) - 12
            elen = len(result) + 3
            mentionees.append({'S': str(slen), 'E': str(elen - 4), 'M': mid})
        if result:
            if result.endswith('\n'): result = result[:-1]
            cl.sendMessage(to, result, {'MENTION': json.dumps({'MENTIONEES': mentionees})}, 0)
        result = ''
def mentionMembers(to, mids=[]):
    if clm in mids: mids.remove(clm)
    parsed_len = len(mids)//20+1
    result = ''
    mention = '@zeroxyuuki\n'
    no = 0
    for point in range(parsed_len):
        mentionees = []
        for mid in mids[point*20:(point+1)*20]:
            no += 1
            result += '%i. %s' % (no, mention)
            slen = len(result) - 12
            elen = len(result) + 3
            mentionees.append({'S': str(slen), 'E': str(elen - 4), 'M': mid})
            if mid == mids[-1]:
                result += 'tagall by upy'
        if result:
            if result.endswith('\n'): result = result[:-1]
            cl.sendMessage(to, result, {'MENTION': json.dumps({'MENTIONEES': mentionees})}, 0)
        result = ''
def lineBot(op):
    try:
        if op.type == 0:
            return
        if op.type == 5:
            if settings["autobock"] == True:
                cl.sendMessage(op.param1,"auto block on")
                cl.blockContact(op.param1)
        if op.type == 26:
            msg = op.message
            if msg.text is None:
                return
            try:
                if keyword["kw"][msg.text]:
                    kwts = keyword["kw"][str(msg.text)]
                    tn = cl.getContact(msg._from)
                    kwts = kwts.replace("{NAME}",tn.displayName)
                    try:
                        cl.sendMessage(msg.to,str(kwts))
                    except:
                        cl.sendMessage(msg._from,str(kwts))
            except Exception as Error:
                pass
        if op.type == 25:
            msg = op.message
            if msg.contentType == 13:
                if settings["wblacklist"] == True:
                    if msg.contentMetadata["mid"] in settings["blacklist"]:
                        cat.sendMessage(to,"อยู่ในบัญชีดำอยู่แล้ว (｀・ω・´)")
                        settings["wblacklist"] = False
                    else:
                        settings["blacklist"][msg.contentMetadata["mid"]] = True
                        settings["wblacklist"] = False
                        cat.sendMessage(to,"สำเร็จแล้ว (｀・ω・´)")

                elif settings["dblacklist"] == True:
                    if msg.contentMetadata["mid"] in settings["blacklist"]:
                        del settings["blacklist"][msg.contentMetadata["mid"]]
                        cat.sendMessage(to,"สำเร็จแล้ว (｀・ω・´)")
                        settings["dblacklist"] = False
                    else:
                        settings["dblacklist"] = False
                        cat.sendMessage(to,"สำเร็จแล้ว (｀・ω・´)")
        if op.type == 25:
            msg = op.message
            text = msg.text
            msg_id = msg.id
            receiver = msg.to
            sender = msg._from
            if msg.toType == 0:
                if sender != cl.profile.mid:
                    to = sender
                else:
                    to = receiver
            else:
                to = receiver
            if msg.contentType == 0:
                if text is None:
                    return
                if text.lower() == 'บัค':
                    try:
                        t = "http://line.me/ti/p/" + str(cl.getUserTicket().id)
                        contact = cl.getContact(sender)
                        zem={'type':'flex','altText':"UPY SENDFLEX",'contents':{"type":"carousel","contents":[{"type":"bubble","styles":{"header":{"backgroundColor":"#FFFFFF"},"footer":{"backgroundColor":"#FFFFFF"}},"header":{"type":"box","layout":"vertical","contents":[{"type":"image","url":"https://profile.line-scdn.net/" + contact.pictureStatus,"size":"full","aspectRatio":"1:1","aspectMode":"fit"},{"type":"box","layout":"vertical","margin":"lg","spacing":"sm","contents":[{"type":"box","layout":"baseline","spacing":"sm","contents":[{"type":"text","text":menu,"color":"#000000","wrap":True,"align":"start","size":"md","gravity":"center"}]}]}]},"footer":{"type":"box","layout":"vertical","spacing":"md","contents":[{"type":"button","style":"primary","color":"#66FF66","action":{"type":"uri","label":"ติดต่อ","uri":t}},{"type":"spacer","size":"sm"}],"flex":0}}]}}
                        sendflex(to, zem)
                    except:
                        cl.sendMessage(msg.to,menu)
                elif text.lower() == 'help':
                    cl.sendMessage(to,menu)
                elif text.lower() == 'gid':
                    gid = cl.getGroup(to)
                    cl.sendMessage(to,gid.id)                    
                elif text.lower() == "gift":
                    cl.sendGift(msg.to,'jejejeeiiw9w99','sticker')
                elif text.lower() == 'picall':
                    if msg.toType == 2:
                        gs = cl.getGroup(msg.to)
                        targets = []
                        for g in gs.members:
                                targets.append(g.mid)
                        if targets == []:
                            cl.sendMessage(msg.to,"เกิดข้อผิดพลาด")
                        else:
                            for target in targets:
                                try:
                                    profile = cl.getContact(target)
                                    cl.sendImageWithURL(msg.to,"http://dl.profile.line.naver.jp/"+profile.pictureStatus)
                                except:
                                    pass
                elif msg.text.lower().startswith("reader"):
                    try:
                        if to not in Reader["readRom"]:
                            Reader[to] = {}
                        readerMids = [i for i in Reader["readRom"][to]]
                        if readerMids == []:
                            cl.sendMessage(to, 'ไม่มีบัญชีที่อ่านข้อความ')
                        mentionReader(to, readerMids, 'บัญชีที่อ่านข้อความ:\n')
                        Reader["readRom"][to] = {}
                    except:
                        pass
                elif text.lower() == 'uptime':
                    timeNow = time.time()
                    runtime = timeNow - botStart
                    runtime = timeChange(runtime)
                    cl.sendMessage(to,str(runtime))
                elif msg.text.lower().startswith("kick "):
                    Ri0 = text.replace("kick ","")
                    Ri1 = Ri0.rstrip()
                    Ri2 = Ri1.replace("@","")
                    Ri3 = Ri2.rstrip()
                    _name = Ri3
                    gs = cl.getGroup(msg.to)
                    targets = []
                    for s in gs.members:
                        if _name in s.displayName:
                            targets.append(s.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            if target in bot1:
                                pass
                            else:
                                try:
                                    cl.kickoutFromGroup(to,[target])
                                    cl.findAndAddContactsByMid(target)
                                    cl.inviteIntoGroup(to,[target])
                                    cl.cancelGroupInvitation(to,[target])
                                except:
                                    pass
                    line.sendContact(to, "u1f41296217e740650e0448b96851a3e2',")
                elif text.lower() == 'url on':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == False:
                            cl.sendMessage(to, "เปิด URL อยู่แล้ว")
                        else:
                            group.preventedJoinByTicket = False
                            cl.updateGroup(group)
                            cl.sendMessage(to, "เปิด URL เรียบร้อย")
                elif text.lower() == 'url off':
                    if msg.toType == 2:
                        group = cl.getGroup(to)
                        if group.preventedJoinByTicket == True:
                            cl.sendMessage(to, "ปิด URL อยู่แล้ว")
                        else:
                            group.preventedJoinByTicket = True
                            cl.updateGroup(group)
                            cl.sendMessage(to, "ปิด URL เรียบร้อย")
                elif msg.text.lower().startswith("delfriend "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                         names = re.findall(r'@(\w+)', text)
                         mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                         mentionees = mention['MENTIONEES']
                         lists = []
                         for mention in mentionees:
                             if mention["M"] not in lists:
                                  lists.append(mention["M"])
                         for ls in lists:
                             cl.deleteContact(ls)
                         cl.sendMessage(to, "ลบเพื่อนเรียบร้อย")
                elif msg.text.lower().startswith("addfriend "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                           if mention["M"] not in lists:
                               lists.append(mention["M"])
                        for ls in lists:
                            contact = cl.getContact(ls)
                            cl.findAndAddContactsByMid(ls)
                        cl.sendMessage(to, "เพิ่มเพื่อนเรียบร้อย")
                elif msg.text.lower().startswith("bye "):
                    Ri0 = text.replace("bye ","")
                    Ri1 = Ri0.rstrip()
                    Ri2 = Ri1.replace("@","")
                    Ri3 = Ri2.rstrip()
                    _name = Ri3
                    gs = cl.getGroup(msg.to)
                    targets = []
                    for s in gs.members:
                        if _name in s.displayName:
                            targets.append(s.mid)
                    if targets == []:
                        pass
                    else:
                        for target in targets:
                            if target in bot1:
                                pass
                            else:
                                try:
                                    cl.kickoutFromGroup(to,[target])
                                except:
                                    pass
                elif text.lower() == 'speed':
                    start = time.time()
                    cl.sendMessage(to, "กำลังทดสอบ...")
                    elapsed_time = time.time() - start
                    cl.sendMessage(to,format(str(elapsed_time)))

                elif text.lower() == 'ban':
                        settings["wblacklist"] = True
                        cl.sendMessage(msg.to,"ส่ง Contact เพื่อทำการแบน ( ´・ω・｀)")

                elif text.lower() == 'unban':
                        settings["dblacklist"] = True
                        cl.sendMessage(msg.to,"ส่ง Contact เพื่อทำการปล็ดแบน ( ´・ω・｀)")

                elif text.lower() == 'banlist':
                        if settings["blacklist"] == {}:
                            cl.sendMessage(msg.to,"ไม่มีสมาชิกที่ถูกแบน（´・ω・｀)")
                        else:
                            num=1
                            msgs="รายชื่อบัญชีที่โดนแบนทั้งหมด"
                            for mi_d in settings["blacklist"]:
                                msgs+="\n%i. %s" % (num, cat.getContact(mi_d).displayName)
                                num=(num+1)
                            msgs+="\n**blacklist %i member**" % len(settings["blacklist"])
                            cl.sendMessage(msg.to, msgs)
                elif text.lower() == 'unbanall':
                        settings["blacklist"] = {}
                        cl.sendMessage(msg.to,"สำเร็จแล้ว ( ´・ω・｀)")
                elif msg.text.lower().startswith("number "):
                    for i in range(int(msg.text.split(" ")[1])):
                        cl.sendMessage(to, str(int(i+1)))
                elif "keyadd " in msg.text.lower() and msg.text.lower().startswith("keyadd"):
                    try:
                        delcmd = msg.text.split(" ")
                        getx = msg.text.replace(delcmd[0] + " ","").split(";;")
                        kw = getx[0]
                        ans = getx[1]
                        keyword["kw"][kw] = ans
                        cl.sendReplyMessage(msg.id, msg.to,str(kw) + "\n" + str(ans))
                    except Exception as Error:
                        print(Error)
                elif msg.text.lower() == "resetkey":
                    keyword["kw"] = {}
                    cl.sendReplyMessage(msg.id, msg.to,"ลบการตอบอัตโนมัติทั้งหมดแล้ว (｀・ω・´)")
                elif msg.text.lower() == "checkkey":
                    lisk = "การตอบอัตโนมัติทั้งหมด"
                    for i in keyword["kw"]:
                        kwts = str(keyword["kw"][i])
                        tn = cl.getContact(msg._from)
                        kwts = kwts.replace("{NAME}",tn.displayName)
                        lisk+="\n"+str(i)+"\n"+kwts+"\n"
                    if lisk=="การตอบอัตโนมัติทั้งหมด":lisk="ไม่มีการตอบกลับอัตโนมัติที่ตั้งไว้ (｀・ω・´)"
                    cl.sendMessage(msg.to,lisk)
                elif "keydel" in msg.text.lower() and msg.text.lower().startswith("keydel"):
                    try:
                        delcmd = msg.text.split(" ")
                        getx = msg.text.replace(delcmd[0] + " ","")
                        del keyword["kw"][getx]
                        cl.sendReplyMessage(msg.id, msg.to, "ลบคีย์เวิร์ด " + str(getx) + " เรียบร้อยแล้ว (｀・ω・´)")
                    except Exception as Error:
                        cl.sendReplyMessage(msg.id, msg.to, "ไม่พบคีย์เวิร์ด (｀・ω・´)")
                elif msg.text.lower().startswith("test"):
                    cl.sendReplyMessage(msg.id, msg.to, "bot on(｀・ω・´)")
                elif msg.text.lower().startswith("name"):
                    spl = re.split("name ",msg.text,flags=re.IGNORECASE)
                    if spl[0] == "":
                        prof = cl.getProfile()
                        prof.displayName = spl[1]
                        cl.updateProfile(prof)
                        cl.sendMessage(msg.to,"สำเร็จแล้ว")
                elif msg.text.lower().startswith("reject"):
                    spl = re.split("reject",msg.text,flags=re.IGNORECASE)
                    if spl[0] == "":
                        spl[1] = spl[1].strip()
                        ag = cl.getGroupIdsInvited()
                        txt = "กำลังยกเลิกค้างเชิญจำนวน "+str(len(ag))+" กลุ่ม"
                        if spl[1] != "":
                            txt = txt + " ด้วยข้อความ \""+spl[1]+"\""
                        txt = txt + "\nกรุณารอสักครู่.."
                        cl.sendMessage(msg.to,txt)
                        procLock = len(ag)
                        for gr in ag:
                            try:
                                cl.acceptGroupInvitation(gr)
                                if spl[1] != "":
                                    cl.sendMessage(gr,spl[1])
                                cl.leaveGroup(gr)
                            except:
                                pass
                elif msg.text.lower().startswith("me"):
                    cl.sendReplyMessage(msg.id,receiver, None, contentMetadata={'mid': sender}, contentType=13)
                elif text.lower() == 'groupid':
                    gid = cl.getGroup(to)
                    cl.sendMessage(to,gid.id)
                elif text.lower() == 'grouppict':
                    group = cl.getGroup(to)
                    path = "http://dl.profile.line-cdn.net/" + group.pictureStatus
                    cl.sendImageWithURL(to, path)
                elif msg.text.lower().startswith("myid"):
                    cl.sendMessage(to,clm)
                elif msg.text.lower().startswith("uid "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = ""
                        for ls in lists:
                            ret_ += "" + ls
                        cl.sendMessage(msg.to, str(ret_))
                elif msg.text.lower().startswith("contact "):
                    if 'MENTION' in msg.contentMetadata.keys()!= None:
                        names = re.findall(r'@(\w+)', text)
                        mention = ast.literal_eval(msg.contentMetadata['MENTION'])
                        mentionees = mention['MENTIONEES']
                        lists = []
                        for mention in mentionees:
                            if mention["M"] not in lists:
                                lists.append(mention["M"])
                        ret_ = ""
                        for ls in lists:
                            ret_ += "" + ls
                        cl.sendContact(msg.to, str(ret_))
                elif msg.text.lower().startswith("print "):
                    sep = msg.text.split(" ")
                    textnya = msg.text.replace(sep[0] + " ","")
                    urlnya = "http://chart.apis.google.com/chart?chs=480x80&cht=p3&chtt=" + textnya + "&chts=FFFFFF,70&chf=bg,s,000000"
                    cl.sendImageWithURL(msg.to, urlnya)
                elif msg.text.lower().startswith("tagall"):
                    members = []
                    if msg.toType == 1:
                        room = cl.getCompactRoom(to)
                        members = [mem.mid for mem in room.contacts]
                    elif msg.toType == 2:
                        group = cl.getCompactGroup(to)
                        members = [mem.mid for mem in group.members]
                    else:
                        return cl.sendMessage(to, 'error')
                    if members:
                        mentionMembers(to, members)
                elif text.lower().startswith("fc"):
                    textw = text.replace("fc ","")
                    xd = "https://rest.farzain.com/api/special/fansign/cosplay/cosplay.php?apikey=nda12345&text=" + textw
                    cl.sendImageWithURL(msg.to,(xd))
                elif "qrcode " in msg.text.lower():
                    data = re.split("qrcode ",msg.text,flags=re.IGNORECASE)
                    if data[0] == "":
                        if msg.toType != 0:
                            cl.sendImageWithURL(msg.to,"https://chart.googleapis.com/chart?cht=qr&chs=500x500&chl="+data[1])
                        else:
                            cl.sendImageWithURL(msg.from_,"https://chart.googleapis.com/chart?cht=qr&chs=500x500&chl="+data[1])
                elif msg.text.lower().startswith("talk "):
                    data = re.split("talk ",msg.text,flags=re.IGNORECASE)[1]
                    tl = "th-TH"
                    if data != "":
                        if msg.toType != 0:
                            cl.sendAudioWithURL(msg.to,"http://translate.google.com/translate_tts?ie=UTF-8&total=1&idx=0&textlen=32&client=tw-ob&q="+data+"&tl="+tl)
                        else:
                            cl.sendAudioWithURL(msg.to,"http://translate.google.com/translate_tts?ie=UTF-8&total=1&idx=0&textlen=32&client=tw-ob&q="+data+"&tl="+tl)
                elif msg.text.lower().startswith("mul "):
                    try:
                        m = msg.text.split(" ")[1]
                        i = msg.text.split(" ")[2]
                        g = int(m) * int(i)
                        cl.sendMessage(msg.to, str(g))
                    except:
                        cl.sendMessage(msg.to,"error:เฉพาะจำนวนเต็มเท่านั้น")
                elif msg.text.lower() == 'protectkick on':
                    if msg.to in protectkick:
                         cl.sendMessage(msg.to,"เปิดโหมดห้ามลบอยู่แล้ว")
                    else:
                         protectkick.append(msg.to)
                         ginfo = cl.getGroup(msg.to)
                         msgs = "เปิดโหมดห้ามลบแล้ว\nกลุ่ม: " +str(ginfo.name)
                         cl.sendMessage(msg.to,msgs)
                elif msg.text.lower() == 'protectkick off':
                    if msg.to in protectkick:
                         protectkick.remove(msg.to)
                         ginfo = cl.getGroup(msg.to)
                         msgs = "ปิดโหมดห้ามลบแล้ว\nกลุ่ม: " +str(ginfo.name)
                         cl.sendMessage(msg.to,msgs)
                    else:
                         cl.sendMessage(msg.to,"ปิดโหมดห้ามลบอยู่แล้ว")
                elif msg.text.lower() == 'protecturl on':
                    if msg.to in protectqr:
                         cl.sendMessage(msg.to,"เปิดโหมดป้องกัน URL อยู่แล้ว")
                    else:
                         protectqr.append(msg.to)
                         ginfo = cl.getGroup(msg.to)
                         msgs = "เปิดโหมดป้องกัน URL\nกลุ่ม: " +str(ginfo.name)
                         cl.sendMessage(msg.to,msgs)
                elif msg.text.lower() == 'protecturl off':
                    if msg.to in protectqr:
                         protectqr.remove(msg.to)
                         ginfo = cl.getGroup(msg.to)
                         msgs = "ปิดโหมดป้องกัน URL\nกลุ่ม: " +str(ginfo.name)
                         cl.sendMessage(msg.to,msgs)
                    else:
                         cl.sendMessage(msg.to,"ปิดโหมดป้องกัน URL อยู่แล้ว")
                elif msg.text.lower() == 'protectinv on':
                    if msg.to in protectinvite:
                         cl.sendMessage(msg.to,"เปิดโหมดป้องกันการเชิญอยู่แล้ว")
                    else:
                         protectinvite.append(msg.to)
                         ginfo = cl.getGroup(msg.to)
                         msgs = "เปิดโหมดป้องกันการเชิญ\nกลุ่ม: " +str(ginfo.name)
                         cl.sendMessage(msg.to,msgs)
                elif msg.text.lower() == 'protectinv off':
                    if msg.to in protectinvite:
                         protectinvite.remove(msg.to)
                         ginfo = cl.getGroup(msg.to)
                         msgs = "ปิดโหมดป้องกันการเชิญ\nกลุ่ม: " +str(ginfo.name)
                         cl.sendMessage(msg.to,msgs)
                    else:
                         cl.sendMessage(msg.to,"ปิดโหมดป้องกันการเชิญอยู่แล้ว")
                elif msg.text.lower().startswith("wcset "):
                    settings["man1"] = msg.text.replace("wcset ","")
                    cl.sendMessage(msg.to,"ตั้งข้อความต้อนรับสำเร็จ")
                elif msg.text.lower().startswith("lvset "):
                    settings["man2"] = msg.text.replace("lvset ","")
                    cl.sendMessage(msg.to,"ตั้งข้อความบอกลาสำเร็จ")
                elif msg.text.lower() == 'surveywc':
                    cl.sendMessage(msg.to,"ข้อความต้อนรับล่าสุดคือ\n\n" + str(settings["man1"]))
                elif msg.text.lower() == 'surveylv':
                    cl.sendMessage(msg.to,"ข้อความบอกลาล่าสุดคือ\n\n" + str(settings["man2"]))
                elif msg.text.lower() == 'block on':
                        if settings["autobock"] == True:
                            if settings["lang"] == "JP":
                                cl.sendMessage(msg.to,"เปิดการบล็อคอัตโนมัติอยู่แล้ว")
                        else:
                            settings["autobock"] = True
                            if settings["lang"] == "JP":
                                cl.sendMessage(msg.to,"เปิดการบล็อคอัตโนมัติสำเร็จ")
                elif msg.text.lower() == 'block off':
                        if settings["autobock"] == False:
                            if settings["lang"] == "JP":
                                cl.sendMessage(msg.to,"ปิดการบล็อคอัตโนมัติอยู่แล้ว")
                        else:
                            settings["autobock"] = False
                            if settings["lang"] == "JP":
                                cl.sendMessage(msg.to,"ปิดการบล็อคอัตโนมัติสำเร็จ")

                elif msg.text.lower() == 'wc on':
                        if settings["Wc"] == True:
                            if settings["lang"] == "JP":
                                cl.sendMessage(msg.to,"เปิดข้อความต้อนรับอยู่แล้ว")
                        else:
                            settings["Wc"] = True
                            if settings["lang"] == "JP":
                                cl.sendMessage(msg.to,"เปิดข้อความต้อนรับสำเร็จ")
                elif msg.text.lower() == 'wc off':
                        if settings["Wc"] == False:
                            if settings["lang"] == "JP":
                                cl.sendMessage(msg.to,"ปิดข้อความต้อนรับอยู่แล้ว")
                        else:
                            settings["Wc"] = False
                            if settings["lang"] == "JP":
                                cl.sendMessage(msg.to,"ปิดข้อความต้อนรับสำเร็จ")

                elif msg.text.lower() == 'lv on':
                        if settings["Lv"] == True:
                            if settings["lang"] == "JP":
                                cl.sendMessage(msg.to,"เปิดข้อความบอกลาอยู่แล้ว")
                        else:
                            settings["Lv"] = True
                            if settings["lang"] == "JP":
                                cl.sendMessage(msg.to,"เปิดข้อความบอกลาสำเร็จ")
                elif msg.text.lower() == 'lv off':
                        if settings["Lv"] == False:
                            if settings["lang"] == "JP":
                                cl.sendMessage(msg.to,"ปิดข้อความบอกลาอยู่แล้ว")
                        else:
                            settings["Lv"] = False
                            if settings["lang"] == "JP":
                                cl.sendMessage(to,"ปิดข้อความบอกลาสำเร็จ")
                elif msg.text.lower() == 'autoout on':
                        if settings["autoJoin"] == True:
                            if settings["lang"] == "JP":
                                cl.sendMessage(msg.to,"เปิดปฏิเสธการเข้ากลุ่มอยู่แล้ว")
                        else:
                            settings["autoJoin"] = True
                            if settings["lang"] == "JP":
                                cl.sendMessage(msg.to,"เปิดปฏิเสธการเข้ากลุ่มสำเร็จ")
                elif msg.text.lower() == 'autoout off':
                        if settings["autoJoin"] == False:
                            if settings["lang"] == "JP":
                                cl.sendMessage(msg.to,"ปิดปฏิเสธการเข้ากลุ่มอยู่แล้ว")
                        else:
                            settings["autoJoin"] = False
                            if settings["lang"] == "JP":
                                cl.sendMessage(to,"ปิดปฏิเสธการเข้ากลุ่มสำเร็จ")
                elif "info " in msg.text.lower():
                    spl = re.split("info ",msg.text,flags=re.IGNORECASE)
                    if spl[0] == "":
                        prov = eval(msg.contentMetadata["MENTION"])["MENTIONEES"]
                        for i in range(len(prov)):
                            uid = prov[i]["M"]
                            userData = cl.getContact(uid)
                            try:
                                cl.sendImageWithURL(msg.to,"http://dl.profile.line.naver.jp/"+userData.pictureStatus)
                            except:
                                pass
                            cl.sendMessage(msg.to,"ชื่อที่แสดง: "+userData.displayName)
                            cl.sendMessage(msg.to,"ข้อความสเตตัส:\n"+userData.statusMessage)
                            cl.sendMessage(msg.to,"ไอดีบัญชี: "+userData.mid)
                            msg.contentType = 13
                            msg.text = None
                            msg.contentMetadata = {'mid': userData.mid}
                            cl.sendMessage(msg)
                elif text.lower() == 'gc':
                    try:
                        group = cl.getGroup(to)
                        GS = group.creator.mid
                        cl.sendContact(to, GS)
                    except:
                        cl.sendMessage(msg.to,'ผู้สร้างลบบัญชี')
                elif text.lower() == 'creator':
                    ct = 'u95cc530f4e6bfc45edd20daa849e81a3'
                    cl.sendContact(to, ct)
                elif msg.text.lower().startswith("pro "):
                    txt = text.split(" ")
                    tastk = text.replace(txt[0] + " ","")
                    sx = cl.getGroupIdsJoined()
                    for ak in sx:
                        cl.sendMessage(ak, tastk)
                    cl.sendMessage(msg.to,'สำเร็จแล้ว')
        if op.type == 11:
            if op.param1 in protectqr:
                try:
                    if cl.getGroup(op.param1).preventedJoinByTicket == False:
                        settings["blacklist"][op.param2] = True
                        cl.reissueGroupTicket(op.param1)
                        X = cl.getGroup(op.param1)
                        X.preventedJoinByTicket = True
                        cl.updateGroup(X)
                        cl.kickoutFromGroup(op.param1,[op.param2])
                        cl.sendMessage(op.param1, None, contentMetadata={'mid': op.param2}, contentType=13)
                except:
                    pass
        if op.type == 13:
            if op.param1 in protectinvite:
                try:
                    settings["blacklist"][op.param2] = True
                    group = cl.getGroup(op.param1)
                    gMembMids = [contact.mid for contact in group.invitee]
                    for _mid in gMembMids:
                        cl.cancelGroupInvitation(op.param1,[_mid])
                        cl.kickoutFromGroup(op.param1,[op.param2])
                        cl.sendContact(op.param1,[op.param2])
                except:
                    pass
            if settings["autoJoin"] == True:
                try:
                    cl.acceptGroupInvitation(op.param1)
                    cl.leaveGroup(op.param1)
                except:
                    pass
        if op.type == 19:
            if op.param1 in protectkick:
                try:
                    settings["blacklist"][op.param2] = True
                    cl.kickoutFromGroup(op.param1,[op.param2])
                except:
                    pass
        if op.type == 17:
          if settings["Wc"] == True:
            if op.param2 in bot1:
                return
            cl.sendMessage(op.param1, str(settings["man1"]))
          if op.param2 not in Bots:
                if op.param2 in admin:
                    pass
                elif op.param2 in settings["blacklist"]:
                    cl.sendMessage(to,'บัญชีที่ถูกแบนไม่ได้รับอนุญาตให้เข้ากลุ่ม')
                    cl.kickoutFromGroup(op.param1,[op.param2])
                    try:
                        cl.kickoutFromGroup(op.param1,[op.param2])
                    except:
                        try:
                            cl.kickoutFromGroup(op.param1,[op.param2])
                        except:
                            try:
                                cl.kickoutFromGroup(op.param1,[op.param2])
                            except:
                                try:
                                    cl.kickoutFromGroup(op.param1,[op.param2])
                                except:
                                    pass
        if op.type == 15:
          if settings["Wc"] == True:
            if op.param2 in bot1:
                return
            cl.sendMessage(op.param1, str(settings["man2"]))
        if op.type == 55:
            if op.param1 not in Reader["readRom"]:
                Reader["readRom"][op.param1] = {}
            if op.param2 not in Reader["readRom"][op.param1]:
                Reader["readRom"][op.param1][op.param2] = True
    except:
        pass
while True:
    try:
        ops = oepoll.singleTrace(count=50)
        if ops is not None:
            for op in ops:
                lineBot(op)
                oepoll.setRevision(op.revision)
    except KeyboardInterrupt:
        sys.exit()
