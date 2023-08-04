# https://github.com/encode/httpx
# https://www.python-httpx.org/
import httpx

params = {'key': 'BDSBZ-MSHCJ-QXSFT-XXEDY-4PY73-TBFI6', 'ip': '223.99.197.190'}
r = httpx.get('https://apis.map.qq.com/ws/location/v1/ip', params=params)
print(r.json())
status = r.json()['status']
print(status)
