#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import smtplib
import subprocess
import time

from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sender_mail(BODY):

    if not os.path.isdir('report'):
        os.mkdir('report')
    
    name_f = str(time.ctime())
    open_f = open(str(start_path)+'/report/'+name_f+'.txt', 'w')
    open_f.write(BODY)
    open_f.close()
    
    HOST = str(cfg_pars.get('smtp', 'server'))
    addr_from = str(cfg_pars.get('smtp', 'user'))
    password = str(cfg_pars.get('smtp', 'pass'))
    EMAILS = str(cfg_pars.get('TO', 'emails'))
    SUBJECT = str(cfg_pars.get('SUBJECT', 'subject'))


    if 'recips' in cfg_pars:
        msg = MIMEMultipart('utf-8')
        msg['From'] = addr_from
        msg['To'] = ', '.join(EMAILS.split(', '))
        msg['Subject'] = SUBJECT
        body = MIMEText(BODY)
        msg.attach(body)
    else:
        msg = MIMEMultipart('utf-8')
        msg['From'] = addr_from
        msg['To'] = EMAILS
        msg['Subject'] = SUBJECT
        body = MIMEText(BODY)
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


def run_proc(CMD):
    
    if 'timeout' in cfg_pars:
        time=int(cfg_pars.get('timeout', 'seconds'))
    else:
        time=2000
    
    PROCESS = subprocess.run(CMD,
                             universal_newlines=True,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             timeout=time
                             )
    out = PROCESS.stdout
    err = PROCESS.stderr
    return out, err


if __name__ == '__main__':

        start_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(start_path, 'config.ini')
 
        
        if os.path.exists(config_path):
            cfg_pars = ConfigParser()
            cfg_pars.read(config_path)
        else:
            print('''
[ERROR]:
        Config not found. Need make config.ini''')
            sys.exit(1)
        
        CMD = str(' '.join(sys.argv[1::]))
        STATE_CMD = run_proc(CMD)
        

        
        if STATE_CMD[1] != '':
            print('''
[WARNING] :
        The process ended with an error:
        '''+ STATE_CMD[1])
            
            BODY = STATE_CMD[1]
        else:
            print('''
[MESSAGE] :

'''+STATE_CMD[0])
            BODY = STATE_CMD[0]
        
        
        
        sender_mail(BODY)
       
        print('[DONE]')
