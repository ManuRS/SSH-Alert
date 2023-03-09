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
    
    pos_m = int(time.strftime("%m")) # Month as a number from 1 to 12
    pos_m = pos_m-1 # Month as a number from 0 to 11

    # 1st of january
    if pos_m==0:
      # Last day of past year
      return 31, 'Dec', year-1

    # 1st of march
    elif pos_m==2:
      # February has two different cases
      if year%4==0 and year%100!=0 or year%400==0:
        day=29 # Bisiesto
      else:
        day=28 # Normal
      return day, 'Feb', year

    # Others 1st 
    else:
      month = list_month[pos_m-1] 
      day = list_num_m[pos_m-1]
      return day, month, year
