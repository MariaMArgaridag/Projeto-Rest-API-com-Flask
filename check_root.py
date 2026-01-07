import urllib.request
try:
    resp=urllib.request.urlopen('http://127.0.0.1:5000/', timeout=5)
    print(resp.read().decode())
except Exception as e:
    print('ERROR', e)
