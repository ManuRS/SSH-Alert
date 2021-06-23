import re
import requests
import aux
from subprocess import Popen, PIPE

#################
# Main fucntion #
#################
def getIPdata(text, html=True):
  ip_regex = r'[0-9]+(?:\.[0-9]+){3}'
  ips = re.findall(ip_regex, text)
  ips = list(set(ips))
  if html:
    results = '<b><u><big>Detected IP details</b></u></big><br>'
  else:
    results = 'Detected IP details:\n'

  for ip in ips:
    if ip_is_private(ip)==True:
      ######
      # Private range message
      ######
      if html==True:
        results += '<br><b>****************   ' + ip + '   ***************</b><br>'
        results += 'Private range, this attempt was made from the internal network <br>'
    
    elif ip != "0.0.0.0":
      #######
      # Select your service here
      #######
      results = ip_api_com(ip, results, html)
      #results = ipinfo_io(ip, results, html)
      #results = ipstack_com(ip, results, html)

  return results+'<br>'

#######################
# Private range check #
#######################
def ip_is_private(ip):
  ret = False
  numbers = ip.split('.')
  
  if numbers[0]=='10':
    ret=True
  elif numbers[0]=='172' and int(numbers[1])>=16 and int(numbers[1])<=31:
    ret=True
  elif numbers[0]=='192' and numbers[1]=='168':
    ret=True
  elif numbers[0]=='169' and numbers[1]=='254':
    ret=True
  
  return ret

#################
#   ipinfo.io   #
#################
def ipinfo_io(ip, results, html=True):
  url = "https://ipinfo.io/" + ip

  result = requests.get(url).text
  result = result.replace('\n  "', '\n  ')
  result = result.replace('": "', ': ')
  result = result.replace('",\n', '\n')
  result = result.replace('{', '')
  result = result.replace('}', '')
  result = result.replace('"\n', '\n')

  if html:
    result = re.sub(r'(ip: '+ip_regex+')', r'<b>****************   \1   ***************</b>' ,result)
    result = result.replace('\n', '<br>')
    results = results + result

  return results

#################
#  ipstack.com  #
#################
# API Key needed
def ipstack_com(ip, results, html=True):
  url = "http://api.ipstack.com/" +ip+ "?access_key=" +aux.ipstack_com+ "&hostname=1"
  result = requests.get(url)
  result = result.json()

  if html:
    loc = str(result['latitude'])+','+str(result['longitude'])

    results += '<br><b>****************   ' + result['ip'] + '   ***************</b><br>'

    results += 'hostname: ' + result['hostname']      + '<br>'
    results += 'city: '     + result['city']          + '<br>'
    results += 'region: '   + result['region_name']   + '<br>'
    results += 'country: '  + result['country_name']  + '<br>'       # ' <img src="' + result['location']['country_flag'] + '"><br>' No funciona por culpa de Google
    results += 'loc: '      + loc                     + '<br>'
    results += 'postal: '   + result['zip']           + '<br>'
    #results += 'isp: '     + result['connection']['isp'] + '<br>' # No la manda aunque aparece en la guia
      
  return results

#################
#   ip-api.com  #
#################
def ip_api_com(ip, results, html=True):
  url = "http://ip-api.com/json/" + ip
  result = requests.get(url)
  result = result.json()
  print(result)

  if html:
    loc = str(result['lat'])+','+str(result['lon'])
    terminal_hostname = "nslookup "+ result['query'] +" | awk '/name = / {print $4}' | head -1 | sed 's/.$//'"
    hostname = console(terminal_hostname)[1].decode("utf-8") 

    if hostname == '':
      hostname = 'No info'

    results += '<br><b>****************   ' + result['query'] + '   ***************</b><br>'

    results += 'hostname: ' + str(hostname)         + '<br>'
    results += 'city: '     + result['city']          + '<br>'
    results += 'region: '   + result['regionName']   + '<br>'
    results += 'country: '  + result['country']       + '<br>'    
    results += 'loc: '      + loc                     + '<br>'
    results += 'postal: '   + result['zip']           + '<br>'
    results += 'isp: '      + result['isp']           + '<br>'
    results += 'org: '      + result['org']           + '<br>'

  return results

def console(cmd):
  p = Popen(cmd, shell=True, stdout=PIPE)
  out, err = p.communicate()
  return (p.returncode, out, err)
