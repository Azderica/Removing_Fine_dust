from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus
import json

url = 'http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnMesureSidoLIst'
serviceKey = 'Dc6ewA1eR8iB5JzsB5vrC8Bt9Xs%2F43rSAnXksoR3ZYoaAs3qb%2F8sfb8zeMdDtg4ZHrnEO4j1aSQCQshB5h2P1A%3D%3D'
queryParams = '?serviceKey='+serviceKey+'&numOfRows=10&pageNo=1&sidoName=%EB%8C%80%EA%B5%AC&searchCondition=DAILY&_returnType=json'


request = Request(url + queryParams)
request.get_method = lambda: 'GET'
response_body = urlopen(request).read()
dict = json.loads(response_body)
#print(dict)

print(dict["list"][4]["cityName"])
print(dict["list"][4]["pm25Value"])
print(dict["list"][4]["pm10Value"])