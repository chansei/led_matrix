# import urequests as requests
import requests
import json

KEY = "bbmjpswmz5f1sgekikb41ei95lvaact4vbcb8mh6invm7ja8wr4j9g6psfyja9ly"

URL_TIMETABLE = "https://api-challenge2024.odpt.org/api/v4/odpt:StationTimetable?acl:consumerKey=" + KEY
URL_POSITION = "https://api-challenge2024.odpt.org/api/v4/odpt:Train?acl:consumerKey=" + KEY

CALENDER = "odpt.Calendar:Weekday"  # Weekday or SaturdayHoliday
DIRECTION = "odpt.RailDirection:Inbound"  # Inbound or Outbound
RAILWAY = "odpt.Railway:JR-East.ChuoRapid"
STATION = "odpt.Station:JR-East.ChuoRapid.HigashiKoganei"

STATIONS = [
    "odpt.Station:JR-East.ChuoRapid.HigashiKoganei",
    "odpt.Station:JR-East.ChuoRapid.MusashiKoganei",
    "odpt.Station:JR-East.ChuoRapid.Kokubunji",
    "odpt.Station:JR-East.ChuoRapid.NishiKokubunji",
    "odpt.Station:JR-East.ChuoRapid.Kunitachi",
    "odpt.Station:JR-East.ChuoRapid.Tachikawa",
    "odpt.Station:JR-East.Ome.Tachikawa"
]
STATIONS_NAME = [
    "東小金井",
    "武蔵小金井",
    "国分寺",
    "西国分寺"
]


def get_train_timetable():
    param = f"&odpt:calendar={CALENDER}&odpt:operator=odpt.Operator:JR-East&odpt:railDirection={DIRECTION}&odpt:railway=odpt.Railway:JR-East.ChuoRapid&odpt:station={STATION}"
    _res = requests.get(URL_TIMETABLE + param)
    # print(_res.status_code)
    _res = _res.json()
    res = _res[0]["odpt:stationTimetableObject"]

    timetables = dict()

    for elem in res:
        train = elem["odpt:train"]
        trainNumber = elem["odpt:trainNumber"]
        destination = elem["odpt:destinationStation"]
        trainType = elem["odpt:trainType"]
        departureTime = elem["odpt:departureTime"]
        if departureTime < "04:00":  # 4:00以前の場合は24時間表記に変換
            departureTime = str(int(departureTime[:2])+24) + departureTime[2:]
        timetables[trainNumber] = [departureTime, train, trainType, destination[0]]

    timetables = dict(sorted(timetables.items(), key=lambda x: x[1][0]))  # 時刻順に並び替え
    return timetables


def get_current_train_timetable(timetables, time: str):
    # time以降に発車する3本を取得する関数
    # time = "HH:MM"のstr形式で与える
    if time < "04:00":
        time = str(int(time[:2])+24) + time[2:]
    current_timetables = {k: v for k, v in timetables.items() if v[0] >= time}
    current_timetables = dict(list(current_timetables.items())[:3])
    current_trainNumbers = list(current_timetables.keys())

    return current_timetables, current_trainNumbers


def get_train_position():
    param = "&odpt:operator=odpt.Operator:JR-East&odpt:railway=odpt.Railway:JR-East.ChuoRapid"
    _res = requests.get(URL_POSITION + param)
    # print(_res.status_code)
    res = _res.json()

    positions = []

    for elem in res:
        if DIRECTION != elem["odpt:railDirection"]:
            continue

        extracted_info = {
            "odpt:trainNumber": elem["odpt:trainNumber"],
            "odpt:delay": elem["odpt:delay"],
            "odpt:carComposition": elem["odpt:carComposition"],
            "odpt:trainType": elem["odpt:trainType"],
            "odpt:destinationStation": elem["odpt:destinationStation"][0],  # リスト形式
            "odpt:toStation": elem.get("odpt:toStation", None),
            "odpt:fromStation": elem.get("odpt:fromStation", None)
        }

        positions.append(extracted_info)

    # TrainTypeが"odpt.TrainType:JR-East.Rapid”のものだけにフィルター
    positions = [x for x in positions if x["odpt:trainType"] == "odpt.TrainType:JR-East.Rapid"]

    return positions


def get_latest_train_list(timetables, current_timetables, current_trainNumbers, positions):
    # 時刻表+位置情報にもとづいて直近に発車する列車のリストを取得する関数

    near_positions = [x for x in positions if x["odpt:fromStation"] in STATIONS and x["odpt:toStation"] != "odpt.Station:JR-East.ChuoRapid.MusashiSakai"]
    near_positions = sorted(near_positions, key=lambda x: STATIONS.index(x["odpt:fromStation"]))  # 近い順にソート
    # print("near_positions", near_positions)
    near_trainNumbers = [x["odpt:trainNumber"] for x in near_positions]
    # current_timetablesとnear_trainNumbersの和と差を取る
    _set_trainNumbers = list(set(current_trainNumbers) | set(near_trainNumbers))
    _diff_trainNumbers = list(set(near_trainNumbers) - set(current_trainNumbers))
    # print("near_trainNumbers", near_trainNumbers, "current_trainNumbers", current_trainNumbers, "_diff_trainNumbers", _diff_trainNumbers)
    # diff_trainNumbersの時刻表情報をtimetableから抽出
    _diff_timetables = {key: timetables[key] for key in _diff_trainNumbers if key in timetables}
    # current_timetablesに追加
    current_timetables.update(_diff_timetables)
    # 遅れと接近情報を追加
    delays = get_train_delay(positions, _set_trainNumbers[:3])
    carCompositions = get_train_carComposition(positions, _set_trainNumbers)
    approaches = get_train_approach(positions, _set_trainNumbers[:3])
    # 時刻表に遅れと接近情報を追加
    for k, v in current_timetables.items():
        v.append(delays.get(k, 0))
        v.append(carCompositions.get(k, 10))
        v.append(approaches.get(k, None))
    # 位置情報を優先して並び替え+残りは時刻表通り
    latest_timetables = dict(sorted(current_timetables.items(), key=lambda x: (x[1][6] is None, x[1][6])))
    return latest_timetables


def get_train_delay(positions, trainNumbers):
    # trainNumbersから遅れを取得
    return {item['odpt:trainNumber']: item['odpt:delay'] for item in positions if item['odpt:trainNumber'] in trainNumbers}


def get_train_carComposition(positions, trainNumbers):
    # trainNumbersから両数を取得
    return {item['odpt:trainNumber']: item['odpt:carComposition'] for item in positions if item['odpt:trainNumber'] in trainNumbers}


def get_train_approach(positions, trainNumbers):
    approachs = dict()
    stations_index = {station: idx for idx, station in enumerate(STATIONS[:4])}
    for trainNumber in trainNumbers:
        train = next((item for item in positions if item['odpt:trainNumber'] == trainNumber), None)
        if train:
            from_station = train['odpt:fromStation']
            to_station = train['odpt:toStation']
            # (A) fromStationまたはtoStationがstationsリストに含まれていない場合はNone
            if from_station not in stations_index and to_station not in stations_index:
                approachs[trainNumber] = None
            else:
                # (B) toStationがNoneならfromStationに停車中として計算
                if to_station is None and from_station in stations_index:
                    position = 2 * stations_index[from_station]
                # (C) toStationに向かっている途中として計算
                elif to_station in stations_index:
                    position = 2 * stations_index[to_station] + 1
                else:
                    position = None
                approachs[trainNumber] = position
        else:
            approachs[trainNumber] = None  # 列車番号が存在しない場合
    return approachs


def get_latest_timetable(now: str):
    timetables = get_train_timetable()
    current_timetables, current_trainNumbers = get_current_train_timetable(timetables, now)
    positions = get_train_position()
    latest_timetables = get_latest_train_list(timetables, current_timetables, current_trainNumbers, positions)
    return latest_timetables


def main():
    from datetime import datetime
    from itertools import islice
    import time

    # コンソールをクリア
    print("\033[2J\033[0;0H")

    # 30秒ごとに最新の時刻表を取得
    while True:
        print(datetime.now().strftime("%H:%M:%S"))
        now = datetime.now().strftime("%H:%M")
        latest_timetables = get_latest_timetable(now)
        positions = []
        for train in dict(islice(latest_timetables.items(), 3)).values():
            print(train[0], train[1].split(".")[-1], train[2].split(".")[-1], train[3].split(".")[-1], "遅れ"+str(int(train[4]/60))+"分", str(train[5])+"両")
            if train[6] is not None and train[6] < 7:
                positions.append(train[6])
        for i in range(0, 7):
            if i % 2 == 1:
                if i in positions:
                    print("=■=", end="")
                else:
                    print("===", end="")
            else:
                if i in positions:
                    print("□■□", end="")
                else:
                    print("□□□", end="")
        print()
        # 更新時間の表示
        print("東小--武小--国分--西国")
        print("\033[F" * 6, end="")
        time.sleep(30)


if __name__ == "__main__":
    main()
