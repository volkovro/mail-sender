#!/usr/bin/env python3

######### -*- coding: utf-8 -*-

import os
import sys
import smtplib
import subprocess
import time

from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sender_mail(BODY):


    start_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(start_path, 'config.ini')
    
    if not os.path.isdir('report'):
             os.mkdir('report')

    if os.path.exists(config_path):
        cfg_pars = ConfigParser()
        cfg_pars.read(config_path)
    else:
        print('Config not found. Need make config.ini')
        sys.exit(1)

    
    name_f = str(time.ctime())
    open_f = open(str(start_path)+'/report/'+name_f+'.txt', 'w')
    open_f.write(BODY)
    open_f.close()
    
    HOST = str(cfg_pars.get('smtp', 'server'))
    addr_from = str(cfg_pars.get('smtp', 'user'))
    password = str(cfg_pars.get('smtp', 'pass'))
    EMAILS = str(cfg_pars.get('TO', 'emails'))
    SUBJECT = str(cfg_pars.get('SUBJECT', 'subject'))



    TRASH = str(cfg_pars.get('trash', 'trash'))



    if 'recips' in cfg_pars:
        msg = MIMEMultipart('utf-8')
        msg['From'] = addr_from
        msg['To'] = ', '.join(EMAILS.split(', '))
        msg['Subject'] = SUBJECT
        body = MIMEText(BODY+TRASH)
        msg.attach(body)
    else:
        msg = MIMEMultipart('utf-8')
        msg['From'] = addr_from
        msg['To'] = EMAILS
        msg['Subject'] = SUBJECT
        body = MIMEText(BODY+TRASH)
        msg.attach(body)





    if 'port' in cfg_pars:
        PORT = cfg_pars.get('smtp', 'port')
    else:
        PORT = 25

    if 'ssl' in cfg_pars:
        server = smtplib.SMTP_SSL(HOST, PORT)
    else:
        server = smtplib.SMTP(HOST, PORT)

    if 'tls' in cfg_pars:
        server.starttls()
    
    if 'debug' in cfg_pars:
        server.set_debuglevel(True)
    

    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()


if __name__ == '__main__':
    CMD = sys.argv
    BODY = str(subprocess.check_output(CMD[1::], universal_newlines=True, timeout=20000))
    sender_mail(BODY)

