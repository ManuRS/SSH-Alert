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
    
    pos_m = int(time.strftime("%m"))-1 #index by 0, no 1
    
    if pos_m==0: #Caso especial, nos vamos al año anterior
      pos_m=12
      year=year-1
    
    month = list_month[pos_m-1]
    day = list_num_m[pos_m-1]
    
    if day==-1:
      #Febrero tiene miga
      if y%4==0 and y%100!=0 or y%400==0:
        day=29 #Bisiesto
      else:
        day=28
    
    return day, month, year

    
def getYesterdayLegacy():
  day = int(time.strftime("%d"))
  month = time.strftime("%B")[0:3]
  year = int(time.strftime("%Y"))

  if day!=1:
    return day-1, month, year
  
  #El dia uno no va hacia atrás
  else:

    if month=='Jan':
      month='Dec'
      day=31
      year=year-1
      
    elif month=='Feb':
      month='Jan'
      day=31
      
    elif month=='Mar':
      month='Feb'
      #Febrero tiene miga
      if y%4==0 and y%100!=0 or y%400==0:
        day=29 #Bisiesto
      else:
        day=28
    
    elif month=='Apr':
      month='Mar'
      day=31
        
    elif month=='May':
      month='Apr'
      day=30  
      
    elif month=='Jun':
      month='May'
      day=31
        
    elif month=='Jul':
      month='Jun'
      day=30
        
    elif month=='Aug':
      month='Jul'
      day=31
        
    elif month=='Sep':
      month='Aug' 
      day=31
      
    elif month=='Oct':
      month='Sep'
      day=30
        
    elif month=='Nov':
      month='Oct'
      day=31
        
    else:#Dec
      month='Nov'
      day=30
    
  return day, month, year
    

