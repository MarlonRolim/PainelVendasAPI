import requests
import pandas as pd
import urllib
import json

response = urllib.request.urlopen('http://192.168.0.123:8053/api/pdvs/avare')
response = response.read()
response = json.loads(response)
db = pd.DataFrame(response)