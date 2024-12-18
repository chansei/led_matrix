import json
import requests

key = "bbmjpswmz5f1sgekikb41ei95lvaact4vbcb8mh6invm7ja8wr4j9g6psfyja9ly"

calendar = "odpt.Calendar:Weekday"
station = "odpt.Station:JR-East.ChuoRapid.HigashiKoganei"
railDirection = "odpt.RailDirection:Outbound"

url_timetable = "https://api-challenge2024.odpt.org/api/v4/odpt:StationTimetable?acl:consumerKey=" + key
param_timetable = f"&odpt:calendar={calendar}&odpt:operator=odpt.Operator:JR-East&odpt:railDirection={railDirection}&odpt:railway=odpt.Railway:JR-East.ChuoRapid&odpt:station={station}"
url_train = "https://api-challenge2024.odpt.org/api/v4/odpt:Train?acl:consumerKey=" + key
param_train = "&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid"

response = requests.get(url_timetable+param_timetable)
print(response.status_code)
print(len(response.content))
# response = requests.get(url_train+param_train)
# print(response.status_code)
# print(len(response.content))


response_json = response.json()
# 整形してファイルに保存
with open('response.json', 'w') as f:
    json.dump(response_json, f, indent=4, ensure_ascii=False)
