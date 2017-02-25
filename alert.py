import time
import smtplib
import aux
import getDates as gd

########
# PARSEO
########

f = open('/var/log/auth.log', 'r')
f2 = open('/var/log/auth.log', 'r')

if time.strftime("%H")=='00':
 #Situacion especial, la hora no se puede restar y hay que calcular el dia de ayer
 h = "23"
 d, m, y = gd.getYesterday()
else:
 #Situacion normal, restamos uno a la hora y el dia se obtiene correctamente
 h = str(int(time.strftime("%H"))-1)
 d = int(time.strftime("%d"))
 m = time.strftime("%B")[0:3]
 y = int(time.strftime("%Y"))

text=""
for line in f:
 if "Failed password" in line:
  if " " + str(d) + " " in line:
   if m in line:
    if h+":" in line:
     text += line+"\n"

text2=""
for line in f2:
 if "terminating" in line or "Server listening" in line:
  if " " + str(d) + " " in line:
   if m in line:
    if h+":" in line:
     text2 += line+"\n"
    
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

start = "<b>"+subj+"<br>==================<br><br></b>"
end = "<b>==============================<br>Send using SSH-Alert:<br>https://github.com/manurs/SSH-Alert</b>"

if text!="":
 msg = "\r\n".join([
  "From: " + aux.fromaddr,
  "To: " + aux.toaddrs,
  "MIME-Version: 1.0",
  "Content-type: text/html",
  "Subject: SSH-Alert: Failed password "+subj,
  "",
  start + text + end
  ])
 server.sendmail(aux.fromaddr, aux.toaddrs, msg)
 
 
if text2!="":
 msg = "\r\n".join([
  "From: " + aux.fromaddr,
  "To: " + aux.toaddrs,
  "MIME-Version: 1.0",
  "Content-type: text/html",
  "Subject: SSH-Alert: Reset server "+subj,
  "",
  start + text2 + end
  ])
 server.sendmail(aux.fromaddr, aux.toaddrs, msg)

server.quit()
