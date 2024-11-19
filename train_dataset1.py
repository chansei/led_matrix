import gtfs_rt_pb2
import requests
import os
import json
from datetime import datetime
from itertools import islice

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
line = "odpt.Railway:JR-East.ChuoRapid"

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
    if train_info["odpt:railDirection"] != direction or train_info["odpt:railway"] != line:
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

# TrainTypeが"odpt.TrainType:JR-East.Rapid”のものだけにフィルター
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

stations_name = [
    "東小金井",
    "武蔵小金井",
    "国分寺",
    "西国分寺"
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
filtered_timeTable.update(filtered_data)

# timetable_stationをpositions_trainNumberの順に並び替える
# 元のtimeTable_stationは時刻表通りに並んでいるはず
# そのため，positions_trainNumberに含まれる列車番号が先頭に来るように並び替える，それ以外は末尾にまとめる
current_timetable_station = dict(sorted(filtered_timeTable.items(), key=lambda x: x[0] not in positions_trainNumber))

# print(current_timetable_station)

# 遅れの情報を取得
filtered_delay = {item['odpt:trainNumber']: item['odpt:delay'] for item in positions if item['odpt:trainNumber'] in set_trainNumber[:3]}

# 現在位置を取得
# 列車番号ごとに処理
filtered_position = dict()
station_index = {station: idx for idx, station in enumerate(stations[:4])}
for train_number in set_trainNumber:
    # 該当する列車情報を検索
    train_data = next((item for item in positions if item['odpt:trainNumber'] == train_number), None)

    if train_data:
        from_station = train_data['odpt:fromStation']
        to_station = train_data['odpt:toStation']

        # (A) fromStationまたはtoStationがstationsリストに含まれていない場合はNone
        if from_station not in station_index and to_station not in station_index:
            filtered_position[train_number] = None
        else:
            # (B) toStationがNoneならfromStationに停車中として計算
            if to_station is None and from_station in station_index:
                position = 2 * station_index[from_station]
            # (C) toStationに向かっている途中として計算
            elif to_station in station_index:
                position = 2 * station_index[to_station] + 1
            else:
                position = None

            filtered_position[train_number] = position
    else:
        filtered_position[train_number] = None  # 列車情報が存在しない場合

for k, v in current_timetable_station.items():
    v.append(filtered_delay.get(k, 0))
    v.append(filtered_position.get(k, None))

print(current_timetable_station)

for train in dict(islice(current_timetable_station.items(), 3)).values():
    print(train[0], train[1].split(".")[-1], train[2].split(".")[-1], train[3].split(".")[-1], "遅れ"+str(train[4])+"分")
    if train[5] is not None:
        if train[5] % 2 == 0:
            print(f"->{stations_name[int(train[5]/2)]}駅に停車中です")
        else:
            print(f"->{stations_name[int((train[5]+1)/2)]}駅を発車しました")
