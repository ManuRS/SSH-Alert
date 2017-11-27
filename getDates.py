import time

def getYesterday():
  day = int(time.strftime("%d"))
  month = time.strftime("%b")
  year = int(time.strftime("%Y"))

  if day!=1:
    return day-1, month, year
  
  #El dia uno no va hacia atrás
  else:
    list_month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    list_num_m = [31, -1, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    pos_m = int(time.strftime("%m"))-1 #index como un array normal from 0, no 1
    
    if pos_m==0: #Caso especial, nos vamos al año anterior
      pos_m=11
      year=year-1
    
    month = list_month[pos_m]
    day = list_num_m[pos_m]
    
    if day==-1:
      #Febrero tiene miga
      if year%4==0 and year%100!=0 or year%400==0:
        day=29 #Bisiesto
      else:
        day=28
    
    return day, month, year