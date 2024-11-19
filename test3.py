import json
import requests
import network
import uasyncio as asyncio
import time
import gc

SSID = "aterm-3f5e1a-g"
PASSWORD = "2215083363178"

key = "bbmjpswmz5f1sgekikb41ei95lvaact4vbcb8mh6invm7ja8wr4j9g6psfyja9ly"

calendar = "odpt.Calendar:Weekday"
station = "odpt.Station:JR-East.ChuoRapid.HigashiKoganei"
railDirection = "odpt.RailDirection:Outbound"

url_timetable = "https://api-challenge2024.odpt.org/api/v4/odpt:StationTimetable?acl:consumerKey=" + key
param_timetable = f"&odpt:calendar={calendar}&odpt:operator=odpt.Operator:JR-East&odpt:railDirection={railDirection}&odpt:railway=odpt.Railway:JR-East.ChuoRapid&odpt:station={station}"
url_train = "https://api-challenge2024.odpt.org/api/v4/odpt:Train?acl:consumerKey=" + key
param_train = "&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
print("Connecting to WiFi", end="")
while not wlan.isconnected():
    print(".", end="")
    time.sleep(1)
print("\nConnected to WiFi:", wlan.ifconfig())

response = requests.get(url_timetable+param_timetable)
print(response.status_code)
print(len(response.content))
response = requests.get(url_train+param_train)
print(response.status_code)
print(len(response.content))

# ramの状態を確認
print(gc.mem_free())
