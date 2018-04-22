#!/usr/bin/env python
# -*- coding:utf-8 -*-

import RPi.GPIO as GPIO
import time
import traceback
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

def checkSendMail():
    MIN_SEND_PERIOD_S = 30
    MAX_SEND_COUNT = 3
    global lastSendmailTime
    global sendMailCount
    now = int(time.time())
    if (lastSendmailTime == 0 or MIN_SEND_PERIOD_S < (now - lastSendmailTime)) and sendMailCount < MAX_SEND_COUNT:
        ret = doSendMail('sender@163.com', 'token', 'receiver@163.com', 'waring!!!')
        if ret:
            lastSendmailTime = now
            sendMailCount += 1

def doSendMail(sender, sender_token, receiver, content):
    print("do send mail")
    smtp_host = "smtp.163.com"
    smtp_port = 465
    message = MIMEText(content, 'plain', 'utf-8')
    message['Subject'] = Header('[MONITOR]', 'utf-8')
    message['From'] = formataddr(["[RASP-001]", sender])
    message['To'] = formataddr(["[MONITOR CENTER]", receiver])
    try:
        server = smtplib.SMTP_SSL(smtp_host, smtp_port)
        server.login(sender, sender_token)
        server.sendmail(sender, [receiver], message.as_string())
        server.quit()
        return True
    except smtplib.SMTPException, e:
        print(traceback.format_exc())
        return False

channel = 12
setupTime = int(time.time())
lastSendmailTime = 0
sendMailCount = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

try:
    while True:
        stat = GPIO.input(channel)
        print("current gpio %d stat %d" % (channel,stat))
            checkSendMail()
        else:
            sendMailCount = 0
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()
