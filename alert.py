import time
import datetime as dt
import smtplib
import aux

########
# PARSEO
########

f = open('/var/log/auth.log', 'r')

text=""
for line in f:
 if "Failed password" in line:
  if " "+str(time.strftime("%d"))+" " in line:
   if dt.datetime.now().strftime("%B")[0:3] in line:
    if " "+str(int(time.strftime("%H"))-1)+":" in line:
     text += line+"\n"
    
########
# ENVIO
########

if text=="":
 exit() #Today nothing happend
 
subj= str(int(time.strftime("%H"))-1) +"h - "+ str(time.strftime("%d")) + time.strftime("/%m/%Y")

msg = "\r\n".join([
  "From: " + aux.fromaddr,
  "To: " + aux.toaddrs,
  "Subject: SSH-Alert: !! "+subj,
  "",
  subj +"\n====\n\n"+ text + "====\nSend using SSH-Alert:\nhttps://github.com/manurs/SHH-Alert"
  ])
  
smtp = 'smtp.gmail.com:587' #If you don't use gmail you have to change this setting
  
server = smtplib.SMTP(smtp)
server.ehlo()
server.starttls()
server.login(aux.fromaddr,aux.pas)
server.sendmail(aux.fromaddr, aux.toaddrs, msg)
server.quit()
