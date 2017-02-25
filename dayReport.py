import time
import datetime as dt
import smtplib
import aux

########
# PARSEO
########

f = open('/var/log/auth.log', 'r')

dia = int(time.strftime("%d"))
if dia!=1:
 dia=dia-1
else:
 #El dia uno no va hacia atrás
 mes = dt.datetime.now().strftime("%B")[0:3]
 if mes=='Jan' or mes=='Feb' or mes=='Apr' or mes=='Jun' or mes=='Aug' or mes=='Sep' or mes=='Nov':
  dia=31
 elif mes=='May' or mes=='Jul' or mes=='Oct' or mes=='Dec':
  dia=30
 else:
  #Febrero tiene miga
  y=int(dt.datetime.now().strftime("%Y"))
  if y%4==0 and y%100!=0 or y%400==0:
   dia=29
  else:
   dia=28

text=""
for line in f:
 if "sshd" in line:
  if " "+str(dia)+" " in line:
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
  "<b>"+subj+"<br>==================<br><br></b>"+ text + "<b>==============================<br>Send using SSH-Alert:<br>https://github.com/manurs/SSH-Alert</b>"
  ])
  
smtp = 'smtp.gmail.com:587' #If you don't use gmail you have to change this setting
  
server = smtplib.SMTP(smtp)
server.ehlo()
server.starttls()
server.login(aux.fromaddr,aux.pas)
server.sendmail(aux.fromaddr, aux.toaddrs, msg)
server.quit()
