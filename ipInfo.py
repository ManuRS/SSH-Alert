import re
import requests

def ipInfo(text, html=True):
  ip_regex = r'[0-9]+(?:\.[0-9]+){3}'
  ips = re.findall(ip_regex, text)
  ips = list(set(ips))
  if html:
  	results = '<b><u><big>Detected IP details</b></u></bigbig><br>'
  else:
  	results = 'Detected IP details:\n'
  for ip in ips:
  	if ip != "0.0.0.0":
  	  url = "http://ipinfo.io/"+ip
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
  return results+'<br>'