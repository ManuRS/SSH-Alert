import time
import smtplib
import os
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.utils import COMMASPACE, formatdate

import aux
import getDates as gd
import ipInfo

########
# PARSEO
########

f = open('/var/log/auth.log', 'r')

if time.strftime("%H")=='00':
 #Situacion especial, la hora no se puede restar y hay que calcular el dia de ayer
 h = "23"
 d, m, y = gd.getYesterday()
else:
 #Situacion normal, restamos uno a la hora y el dia se obtiene correctamente
 h = str(int(time.strftime("%H"))-1)
 #Para test
 #h = str(int(time.strftime("%H"))) 
 if len(h)==1:
  h = "0"+h
 d = int(time.strftime("%d"))
 m = time.strftime("%b")
 y = int(time.strftime("%Y"))

text  = ""
text2 = ""
for line in f:

 if "Failed password" in line:
  if m + " " + str(d) + " " + h + ":" in line or m + "  " + str(d) + " " + h + ":" in line:
   text += line+"\n"

 if "terminating" in line or "Server listening" in line:
  if m + " " + str(d) + " " + h + ":" in line or m + "  " + str(d) + " " + h + ":" in line:
   text2 += line+"\n"

ip_info = ipInfo.ipInfo(text+text2)

########
#  ENVIO
########

if text=="" and text2=="":
 exit() #Today nothing happend

smtp = 'smtp.gmail.com:587' #If you don't use gmail you have to change this setting
server = smtplib.SMTP(smtp)
server.ehlo()
server.starttls()
server.login(aux.fromaddr,aux.pas)

subj= h +"h - "+ str(d) + time.strftime("/%m/%Y")

text = text.replace("\n", "<br>")
text2 = text2.replace("\n", "<br>")

start = subj+"<br>============================<br><br></b>"
start2 = subj+"<br>=========================<br><br></b>"
end = "<b>==============================<br>Send using SSH-Alert:<br>https://github.com/manurs/SSH-Alert<br>==============================</b>"

if text!="":
 msg = "\r\n".join([
  "From: " + aux.fromaddr,
  "To: " + aux.toaddrs,
  "MIME-Version: 1.0",
  "Content-type: text/html",
  "Subject: SSH-Alert: Failed password "+subj,
  "",
  "<b>============================<br>Failed password - " + start + text + ip_info + end
  ])
 server.sendmail(aux.fromaddr, aux.toaddrs, msg)
 
if text2!="":
 msg = MIMEMultipart()
 msg['From'] = aux.fromaddr
 msg['To'] = aux.toaddrs
 msg['Date'] = formatdate(localtime = True)
 msg['Subject'] = "SSH-Alert: Reset server " + subj

 msg.attach( MIMEText("<b>============================<br>Reset server - " + start2 + text2 + end, 'HTML') ) 
  
 part = MIMEBase('application', "octet-stream")
 f="/etc/ssh/sshd_config"
 part.set_payload( open(f,"rb").read() )
 encoders.encode_base64(part)
 part.add_header('Content-Disposition', 'attachment; filename="{0}"'.format(os.path.basename(f)+".txt"))
 msg.attach(part) 
 server.sendmail(aux.fromaddr, aux.toaddrs, msg.as_string())

server.quit()