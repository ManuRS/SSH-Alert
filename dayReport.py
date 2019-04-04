import time
import smtplib

import aux
import getDates as gd
import getIPdata

from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate
from email import encoders

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
   
ip_info = getIPdata.getIPdata(text_sshd)

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
end   = "<b><big>================================<br>"+end1+"<br>"+end2+"<br>================================<b></big>"  

start_sshd = "<b><u><big>SSHD Events</b></u></bigbig><br><br>"
start_user = "<b><u><big>Users Events</b></u></bigbig><br><br>"

# Email data
msg = MIMEMultipart()
msg['From'] = aux.fromaddr
msg['To'] = aux.toaddrs
msg['Date'] = formatdate(localtime = True)
msg['Subject'] = "SSH-Alert: " + subj

# Email message
msg.attach( MIMEText(start + start_sshd + text_sshd + start_user + text_user + ip_info + end, 'HTML') ) 

# Email File
part = MIMEBase('application', "octet-stream")
part.set_payload( open(aux.auth_log,"rb").read() )
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename="auth_log.txt"')
msg.attach(part) 
  
# Send mail
server = smtplib.SMTP(aux.smtp)
server.ehlo()
server.starttls()
server.login(aux.fromaddr,aux.pas)
server.sendmail(aux.fromaddr, aux.toaddrs, msg.as_string())
server.quit()