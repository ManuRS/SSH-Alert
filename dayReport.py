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
 if "password" in line or "AllowUsers" in line:
  if " "+str(int(time.strftime("%d"))-1)+" " in line:
   if dt.datetime.now().strftime("%B")[0:3] in line:
    text += line
    
########
# ENVIO
########

msg = "\r\n".join([
  "From: " + aux.fromaddr,
  "To: " + aux.toaddrs,
  "Subject: SSH-Alert: "+ time.strftime("%d/%m/%Y"),
  "",
  text
  ])
  
smtp = 'smtp.gmail.com:587'
  
server = smtplib.SMTP(smtp)
server.ehlo()
server.starttls()
server.login(aux.fromaddr,aux.pas)
server.sendmail(aux.fromaddr, aux.toaddrs, msg)
server.quit()
