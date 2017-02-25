import time
import smtplib
import aux
import getDates as gd

########
# PARSEO
########

f = open('/var/log/auth.log', 'r')

d, m, y = gd.getYesterday()

text=""
for line in f:
 if "sshd" in line:
  if " "+str(d)+" " in line:
   if m in line:
    text += line+"\n"
    
########
#  ENVIO
########

if text=="":
 exit() #Today nothing happend

subj = "Day report " + str(d) + time.strftime("/%m/%Y")

text = text.replace("[", "<b>[")
text = text.replace("]", "]</b>")
text = text.replace("\n", "<br>")

start = "<b>"+subj+"<br>==================<br><br></b>"
end = "<b>==============================<br>Send using SSH-Alert:<br>https://github.com/manurs/SSH-Alert</b>"

msg = "\r\n".join([
  "From: " + aux.fromaddr,
  "To: " + aux.toaddrs,
  "MIME-Version: 1.0",
  "Content-type: text/html",
  "Subject: SSH-Alert: "+subj,
  "",
  start + text + end
  ])
  
smtp = 'smtp.gmail.com:587' #If you don't use gmail you have to change this setting
  
server = smtplib.SMTP(smtp)
server.ehlo()
server.starttls()
server.login(aux.fromaddr,aux.pas)
server.sendmail(aux.fromaddr, aux.toaddrs, msg)
server.quit()
