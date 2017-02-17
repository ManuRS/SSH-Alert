import time
import datetime

f = open('/var/log/auth.log', 'r')
#print (f.read())

text=""
for line in f:
 if "password" in line:
  if str(int(time.strftime("%d"))-1) in line:
   if mydate.strftime("%B")[0:3]) in line:
    text += line
   
print (text)

mydate = datetime.datetime.now()
print (mydate.strftime("%B")[0:3])

