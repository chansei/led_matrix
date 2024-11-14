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

timetable_station = dict()

# 検索条件
calendar = "odpt.Calendar:Weekday"  # Weekday or SaturdayHoliday
direction = "odpt.RailDirection:Inbound"  # Inbound or Outbound

for timetable in response_json:
    train = timetable["odpt:train"]
    trainNumber = timetable["odpt:trainNumber"]
    destination = timetable["odpt:destinationStation"]
    trainType = timetable["odpt:trainType"]

    if calendar not in timetable["odpt:calendar"] or direction not in timetable["odpt:railDirection"]:
        continue

    for stop in timetable["odpt:trainTimetableObject"]:
        try:
            if stop["odpt:departureStation"] == "odpt.Station:JR-East.ChuoRapid.HigashiKoganei":
                departureTime = stop["odpt:departureTime"]
                if departureTime < "04:00":  # 4:00以前の場合は24時間表記に変換
                    departureTime = str(int(departureTime[:2])+24) + departureTime[2:]
                timetable_station[trainNumber] = [departureTime, train, trainType, destination[0]]
        except:
            pass

timetable_station = dict(sorted(timetable_station.items(), key=lambda x: x[1][0]))

# 結果の出力
# print(timetable_station)

# 現在時刻より後ろの3本を取得
now = datetime.now()
now = now.strftime("%H:%M")
# 現在時刻が4:00以前の場合は24時間表記に変換
if now < "04:00":
    now = str(int(now[:2])+24) + now[2:]
filtered_timeTable = {k: v for k, v in timetable_station.items() if v[0] >= now}
filtered_timeTable = dict(list(filtered_timeTable.items())[:3])
current_trainNumber = list(filtered_timeTable.keys())

response = requests.get(url_Train)
print(response.status_code)
response_json = response.json()

# odpt:trainNumberがTrainNumbersに含まれるものだけ取得
# response_json = [x for x in response_json if x["odpt:trainNumber"] in TrainNumbers]

positions = []
for train_info in response_json:
    if direction not in train_info["odpt:railDirection"]:
        continue

    extracted_info = {
        "odpt:trainNumber": train_info["odpt:trainNumber"],
        "odpt:delay": train_info["odpt:delay"],
        "odpt:carComposition": train_info["odpt:carComposition"],
        "odpt:trainType": train_info["odpt:trainType"],
        "odpt:destinationStation": train_info["odpt:destinationStation"][0],  # リスト形式
        "odpt:toStation": train_info.get("odpt:toStation", None),
        "odpt:fromStation": train_info.get("odpt:fromStation", None)
    }
    positions.append(extracted_info)

# TrainTypeが"odpt.TrainType:JR-East.Rapid”のものだけ取得
positions = [x for x in positions if x["odpt:trainType"] == "odpt.TrainType:JR-East.Rapid"]

stations = [
    "odpt.Station:JR-East.ChuoRapid.HigashiKoganei",
    "odpt.Station:JR-East.ChuoRapid.MusashiKoganei",
    "odpt.Station:JR-East.ChuoRapid.Kokubunji",
    "odpt.Station:JR-East.ChuoRapid.NishiKokubunji",
    "odpt.Station:JR-East.ChuoRapid.Kunitachi",
    "odpt.Station:JR-East.ChuoRapid.Tachikawa",
    "odpt.Station:JR-East.Ome.Tachikawa"
]

# 近辺の列車のみ取得
near_positions = [x for x in positions if x["odpt:fromStation"] in stations[1:]]
near_positions = sorted(near_positions, key=lambda x: stations.index(x["odpt:fromStation"]))  # 近い順にソート

# odpt:trainNumberをリストアップ
positions_trainNumber = [x["odpt:trainNumber"] for x in near_positions]

# current_trainNumberとpositions_trainNumberの和と差を取得
set_trainNumber = list(set(current_trainNumber) | set(positions_trainNumber))
diff_trainNumber = list(set(current_trainNumber) - set(positions_trainNumber))
# diff_trainNumberの時刻表情報をstation_timetableから抽出
filtered_data = {key: timetable_station[key] for key in diff_trainNumber if key in timetable_station}
# filtered_timeTableとfiltered_dataを連結
timetable_station.update(filtered_data)

# timetable_stationをpositions_trainNumberの順に並び替える
# 元のtimeTable_stationは時刻表通りに並んでいるはず
# そのため，positions_trainNumberに含まれる列車番号が先頭に来るように並び替える，それ以外は末尾にまとめる
current_timetable_station = dict(sorted(timetable_station.items(), key=lambda x: x[0] not in positions_trainNumber))

# ここまでで近辺の位置情報をもとに直近の時刻情報を取得
# 遅れの情報を取得

# positionsからset_trainNumberを検索しdelayを取得


# 時刻表に基づくリストと結合，重複は無視
trainNumber_result = list(set(current_trainNumber) | set(positions_trainNumber))
print(trainNumber_result)  # 時刻表+近辺位置の列車番号

# 発車票に表示する要素の整理


for train in trainNumber_result:
    print(train["odpt:trainNumber"])


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
