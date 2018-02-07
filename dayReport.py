import time
import smtplib

import aux
import getDates as gd
import ipInfo

########
# PARSEO
########

f = open(aux.auth_log, 'r')

d, m, y = gd.getYesterday()
#Para pruebas
#d = d+1
text=""
for line in f:
 if "sshd" in line:
  if m + " " + str(d) + " " in line or m + "  " + str(d) + " " in line :
   text += line+"\n"
   
ip_info = ipInfo.ipInfo(text)

########
#  ENVIO
########

if text=="":
 exit() #Today nothing happend

subj = "Day report " + str(d) + time.strftime("/%m/%Y")

text = text.replace("[", "<b>[")
text = text.replace("]", "]</b>")
text = text.replace("\n", "<br>")

start = "<b>==================<br>"+subj+"<br>==================<br><br></b>"
end = "<b>==============================<br>Send using SSH-Alert:<br>https://github.com/manurs/SSH-Alert<br>==============================</b>"

msg = "\r\n".join([
  "From: " + aux.fromaddr,
  "To: " + aux.toaddrs,
  "MIME-Version: 1.0",
  "Content-type: text/html",
  "Subject: SSH-Alert: "+subj,
  "",
  start + text + ip_info + end
  ])
  
server = smtplib.SMTP(aux.smtp)
server.ehlo()
server.starttls()
server.login(aux.fromaddr,aux.pas)
server.sendmail(aux.fromaddr, aux.toaddrs, msg)
server.quit()