import time

def getYesterday():
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
    
  return day, m, year
    

