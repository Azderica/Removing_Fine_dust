from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import json

url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst'
serviceKey = 'serviceKey'
queryParams = '?serviceKey='+serviceKey+'&numOfRows=10&pageNo=1&sidoName=%EB%8C%80%EA%B5%AC&searchCondition=DAILY&_returnType=json'


request = Request(url + queryParams)
request.get_method = lambda: 'GET'
response_body = urlopen(request).read()
dict = json.loads(response_body)
#print(dict)

print(dict["list"][4]["cityName"])
print(dict["list"][4]["pm25Value"])
print(dict["list"][4]["pm10Value"])