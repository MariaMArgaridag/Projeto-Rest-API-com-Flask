import urllib.request
import urllib.error
url='http://127.0.0.1:5000/'
try:
    resp=urllib.request.urlopen(url, timeout=5)
    print('STATUS', resp.getcode())
    print(resp.read().decode())
except urllib.error.HTTPError as e:
    print('HTTPError', e.code)
    try:
        print(e.read().decode())
    except Exception:
        pass
except Exception as e:
    print('ERR', e)
