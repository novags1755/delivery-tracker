import urllib.request, urllib.parse
import json

serviceurl = 'http://py4e-data.dr-chuck.net/opengeo?'
address = 'University of New Haven'
params = {'q': address}

url = serviceurl + urllib.parse.urlencode(params)
print('Retrieving', url)

uh = urllib.request.urlopen(url)
data = uh.read().decode()

info = json.loads(data)
print(json.dumps(info, indent=4))  # 👈 Print the full JSON response to debug

# Only try this after confirming 'plus_code' exists
# plus_code = info["plus_code"]["global_code"]
