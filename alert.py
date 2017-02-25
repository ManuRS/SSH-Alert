import time
import datetime as dt
import smtplib
import aux

########
# PARSEO
########

f = open('/var/log/auth.log', 'r')
f2 = open('/var/log/auth.log', 'r')

if time.strftime("%H")=='00':
 h="23"
else:
 h=str(int(time.strftime("%H"))-1)

text=""
for line in f:
 if "Failed password" in line:
  if " "+str(time.strftime("%d"))+" " in line:
   if dt.datetime.now().strftime("%B")[0:3] in line:
    if h+":" in line:
     text += line+"\n"

text2=""
for line in f2:
 if "terminating" in line or "Server listening" in line:
  if " "+str(time.strftime("%d"))+" " in line:
   if dt.datetime.now().strftime("%B")[0:3] in line:
    if h+":" in line:
     text2 += line+"\n"
    
########
# ENVIO
########

if text=="" and text2=="":
 exit() #Today nothing happend

subj= h +"h - "+ str(time.strftime("%d")) + time.strftime("/%m/%Y")

smtp = 'smtp.gmail.com:587' #If you don't use gmail you have to change this setting
server = smtplib.SMTP(smtp)
server.ehlo()
server.starttls()
server.login(aux.fromaddr,aux.pas)

if text!="":
 msg = "\r\n".join([
  "From: " + aux.fromaddr,
  "To: " + aux.toaddrs,
  "Subject: SSH-Alert: Failed password "+subj,
  "",
  subj +"\n====\n\n"+ text + "====\nSend using SSH-Alert:\nhttps://github.com/manurs/SHH-Alert"
  ])
 server.sendmail(aux.fromaddr, aux.toaddrs, msg)
 
 
if text2!="":
 msg = "\r\n".join([
  "From: " + aux.fromaddr,
  "To: " + aux.toaddrs,
  "Subject: SSH-Alert: Reset "+subj,
  "",
  subj +"\n====\n\n"+ text2 + "====\nSend using SSH-Alert:\nhttps://github.com/manurs/SHH-Alert"
  ])
 server.sendmail(aux.fromaddr, aux.toaddrs, msg)

server.quit()
