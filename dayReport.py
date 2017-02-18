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
 if "sshd" in line:
  if " "+str(int(time.strftime("%d"))-1)+" " in line:
   if dt.datetime.now().strftime("%B")[0:3] in line:
    text += line+"\n"
    
########
# ENVIO
########

if text=="":
 exit() #Today nothing happend

subj = "Day report " + str(int(time.strftime("%d"))-1) + time.strftime("/%m/%Y")

text = text.replace("[", "<b>[")
text = text.replace("]", "]</b>")
text = text.replace("\n", "<br>")
deco = "Content-Type: text/plain; charset=UTF-8\n"+"Content-Transfer-Encoding: quoted-printable\n"

msg = "\r\n".join([
  "From: " + aux.fromaddr,
  "To: " + aux.toaddrs,
  "MIME-Version: 1.0",
  "Content-type: text/html",
  "Subject: SSH-Alert: "+subj,
  "",
  "<b>"+subj+"<br>==================<br><br></b>"+ text + "<b>==============================<br>Send using SSH-Alert:<br>https://github.com/manurs/SHH-Alert</b>"
  ])
  
smtp = 'smtp.gmail.com:587' #If you don't use gmail you have to change this setting
  
server = smtplib.SMTP(smtp)
server.ehlo()
server.starttls()
server.login(aux.fromaddr,aux.pas)
server.sendmail(aux.fromaddr, aux.toaddrs, msg)
server.quit()
