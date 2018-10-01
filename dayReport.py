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
#print(d,m,y)
#d = d-1

text_sshd=""
text_user=""
for line in f:
 if m + " " + str(d) + " " in line or m + "  " + str(d) + " " in line :
  if "sshd" in line:
   text_sshd += line+"\n"
  if "COMMAND=" in line and not ("dayReport" in line or "alert" in line):
   text_user += line+"\n"
   
ip_info = ipInfo.ipInfo(text_sshd)

########
#  ENVIO
########

if text_sshd=="" and text_user=="":
 exit() #Today nothing happend

subj = "Day report " + str(d) + time.strftime("/%m/%Y")
end1 = "Sent using SSH-Alert:"
end2 = "https://github.com/manurs/SSH-Alert"

text_sshd = text_sshd.replace("[", "<b>[")
text_sshd = text_sshd.replace("]", "]</b>")
text_sshd = text_sshd.replace("\n", "<br>")

text_user = text_user.replace("[", "<b>[")
text_user = text_user.replace("]", "]</b>")
text_user = text_user.replace("\n", "<br>")

start = "<b><big>==================<br>"+subj+"<br>==================</b></big><br><br>"
end   = "<b><big>===============================<br>"+end1+"<br>"+end2+"<br>===============================</b></big>"  

start_sshd = "<b><u><big>SSHD Events</b></u></bigbig><br><br>"
start_user = "<b><u><big>Users Events</b></u></bigbig><br><br>"

msg = "\r\n".join([
  "From: " + aux.fromaddr,
  "To: " + aux.toaddrs,
  "MIME-Version: 1.0",
  "Content-type: text/html",
  "Subject: SSH-Alert: "+subj,
  "",
  start + start_sshd + text_sshd + start_user + text_user + ip_info + end
  ])
  
server = smtplib.SMTP(aux.smtp)
server.ehlo()
server.starttls()
server.login(aux.fromaddr,aux.pas)
server.sendmail(aux.fromaddr, aux.toaddrs, msg)
server.quit()