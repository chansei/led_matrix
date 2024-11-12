import gtfs_rt_pb2
import requests
import os
import json
from datetime import datetime

key = "bbmjpswmz5f1sgekikb41ei95lvaact4vbcb8mh6invm7ja8wr4j9g6psfyja9ly"

url_Train = "https://api-challenge2024.odpt.org/api/v4/odpt:Train?odpt:operator=odpt.Operator:JR-East&acl:consumerKey=" + key
url_TrainTimetable = "https://api-challenge2024.odpt.org/api/v4/odpt:TrainTimetable?odpt:operator=odpt.Operator:JR-East&acl:consumerKey=" + key

response = requests.get(url_TrainTimetable)
print(response.status_code)
response_json = response.json()
# print(response_json)

# "odpt:railway"が"odpt.Railway:JR-East.ChuoRapid"のものだけ取得
response_json = [x for x in response_json if x["odpt:railway"] == "odpt.Railway:JR-East.ChuoRapid"]

result = []

# 検索条件
calendar = "odpt.Calendar:Weekday"  # Weekday or SaturdayHoliday
direction = "odpt.RailDirection:Inbound"  # Inbound or Outbound

for timetable in response_json:
    train = timetable["odpt:train"]
    trainNumber = timetable["odpt:trainNumber"]
    destination = timetable["odpt:destinationStation"]

    if calendar not in timetable["odpt:calendar"] or direction not in timetable["odpt:railDirection"]:
        continue

    for stop in timetable["odpt:trainTimetableObject"]:
        try:
            if stop["odpt:departureStation"] == "odpt.Station:JR-East.ChuoRapid.HigashiKoganei":
                result.append({"odpt:departureTime": stop["odpt:departureTime"], "odpt:train": train, "odpt:trainNumber": trainNumber, "odpt:destinationStation": destination})
        except:
            pass

result = sorted(result, key=lambda x: x["odpt:departureTime"])

# 結果の出力
# print(result)

# 現在時刻より後ろの3本を取得
now = datetime.now()
now = now.strftime("%H:%M")
result = [x for x in result if x["odpt:departureTime"] > now]
result = result[:3]
# print(result)

TrainNumbers = [x["odpt:trainNumber"] for x in result]

response = requests.get(url_Train)
print(response.status_code)
response_json = response.json()

# odpt:trainNumberがTrainNumbersに含まれるものだけ取得
# response_json = [x for x in response_json if x["odpt:trainNumber"] in TrainNumbers]

result = []
for train_info in response_json:
    if direction not in train_info["odpt:railDirection"]:
        continue

    extracted_info = {
        "odpt:trainNumber": train_info["odpt:trainNumber"],
        "odpt:delay": train_info["odpt:delay"],
        "odpt:carComposition": train_info["odpt:carComposition"],
        "odpt:toStation": train_info.get("odpt:toStation", None),
        "odpt:fromStation": train_info.get("odpt:fromStation", None)
    }
    result.append(extracted_info)

stations = [
    "odpt.Station:JR-East.ChuoRapid.HigashiKoganei",
    "odpt.Station:JR-East.ChuoRapid.MusashiKoganei",
    "odpt.Station:JR-East.ChuoRapid.Kokubunji",
    "odpt.Station:JR-East.ChuoRapid.NishiKokubunji"
]

stations_name = [
    "東小金井",
    "武蔵小金井",
    "国分寺",
    "西国分寺"
]

# 各駅の位置情報を格納する辞書
train_position = [[] for _ in range(2*len(stations)-1)]

# 列車の位置を整理
for train in result:
    train_number = train["odpt:trainNumber"]
    delay = int(train["odpt:delay"]/60)
    to_station = train.get("odpt:toStation", None)
    from_station = train.get("odpt:fromStation", None)

    # 駅間を走行中
    if to_station in stations:
        station_index = stations.index(to_station)
        if station_index < len(stations):
            train_position[station_index+1].append((train_number, delay))

    # 駅に停車中
    elif from_station in stations:
        station_index = stations.index(from_station)
        # 最後の駅～表示外の駅間を確認するためto_stationが存在するか確認
        if not to_station:
            train_position[station_index].append((train_number, delay))

print(train_position)

# 結果の出力
for i, trains in enumerate(train_position):
    line = ""
    if i % 2 == 0:
        line += stations_name[int(i/2)]
        for train in train_position[i]:
            line += f" {train[0]}(遅れ{train[1]}分)"
    elif i % 2 == 1:
        line += "｜"
        for train in train_position[i]:
            line += f" {train[0]}(遅れ{train[1]}分)"
    print(line)


# # 整形して保存
# with open('train.json', 'w') as f:
#     json.dump(response_json, f)
