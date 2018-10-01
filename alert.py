import time
import smtplib
import os
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from email.utils import COMMASPACE, formatdate
import difflib

import aux
import getDates as gd
import ipInfo

########
# PARSEO
########

f = open(aux.auth_log, 'r')

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

#ip info
ip_info = ipInfo.ipInfo(text+text2)

#Diferencias fichero configuración
diff = difflib.unified_diff(open(aux.system_sshd_config).readlines(), open(aux.trusted_sshd_config).readlines(), n=0)
diff = list(diff)
#print(len(diff))
#for cosa in diff:
#  print(cosa)

########
#  ENVIO
########

if text=="" and text2=="" and len(diff)==0:
 exit() #Today nothing happend

server = smtplib.SMTP(aux.smtp)
server.ehlo()
server.starttls()
server.login(aux.fromaddr,aux.pas)

subj= h +"h - "+ str(d) + time.strftime("/%m/%Y")

text = text.replace("\n", "<br>")
text2 = text2.replace("\n", "<br>")

start = subj+"<br>============================<br><br></b></big>"
start2 = subj+"<br>=========================<br><br></b></big>"
end = "<b><big>================================<br>Send using SSH-Alert:<br>https://github.com/manurs/SSH-Alert<br>================================</b></big>"

########
#  PASS
########
if text != "":
 text = "<b><u><big>SSHD Events</b></u></bigbig><br><br>" + text
 msg = "\r\n".join([
  "From: " + aux.fromaddr,
  "To: " + aux.toaddrs,
  "MIME-Version: 1.0",
  "Content-type: text/html",
  "Subject: SSH-Alert: Failed password "+subj,
  "",
  "<b><big>============================<br>Failed password - " + start + text + ip_info + end
  ])
 server.sendmail(aux.fromaddr, aux.toaddrs, msg)
 
######################
#  RESET & CONFIG FILE
#######################

if text2!="" or len(diff)!=0:
 text_diff = ""

 if text2 == "":
  text2 = "Nothing about reset on your auth_log file but changes between system and trusted sshd_config.<br>A) somebody made changes to the sshd_config file but edited the log to hide the server restart<br>B) restart pending<br>Take a look at the differences file.<br><br>"
  text2 = "<b><u><big>Attention!!</b></u></bigbig><br><br>" + text2
 elif len(diff)==0:
  text2 = "<b><u><big>SSHD Events</b></u></bigbig><br><br>" + text2
  text_diff = "Reset without changes in the sshd_config.<br><br>"
  text_diff = "<b><u><big>Attention!!</b></u></bigbig><br><br>" + text_diff
 else:
  text2 = "<b><u><big>SSHD Events</b></u></bigbig><br><br>" + text2
  text_diff = "Reset with changes in the sshd_config.<br>Take a look at the differences file.<br><br>"
  text_diff = "<b><u><big>Attention!!</b></u></bigbig><br><br>" + text_diff

 msg = MIMEMultipart()
 msg['From'] = aux.fromaddr
 msg['To'] = aux.toaddrs
 msg['Date'] = formatdate(localtime = True)
 msg['Subject'] = "SSH-Alert: Reset server " + subj

 msg.attach( MIMEText("<b><big>=========================<br>Reset server - " + start2 + text2 + text_diff + end, 'HTML') ) 

 #File
 part = MIMEBase('application', "octet-stream")
 part.set_payload( open(aux.system_sshd_config,"rb").read() )
 encoders.encode_base64(part)
 part.add_header('Content-Disposition', 'attachment; filename="system_sshd_config.txt"')
 msg.attach(part) 

 if len(diff)!=0:
   #File
   part = MIMEBase('application', "octet-stream")
   part.set_payload( open(aux.trusted_sshd_config,"rb").read() )
   encoders.encode_base64(part)
   part.add_header('Content-Disposition', 'attachment; filename="trusted_sshd_config.txt"')
   msg.attach(part) 

   #File
   part = MIMEBase('application', "octet-stream")
   part.set_payload('\n'.join(diff))
   encoders.encode_base64(part)
   part.add_header('Content-Disposition', 'attachment; filename="diff_sshd_config.txt"')
   msg.attach(part) 

 server.sendmail(aux.fromaddr, aux.toaddrs, msg.as_string())

server.quit()