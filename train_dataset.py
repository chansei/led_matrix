import gtfs_rt_pb2
import requests
import os
import json

key = "bbmjpswmz5f1sgekikb41ei95lvaact4vbcb8mh6invm7ja8wr4j9g6psfyja9ly"

url = "https://api-challenge2024.odpt.org/api/v4/gtfs/realtime/jreast_odpt_train_vehicle?acl:consumerKey=" + key
# url = "https://api-challenge2024.odpt.org/api/v4/odpt:Train?odpt:operator=odpt.Operator:JR-East&acl:consumerKey=" + key


feed = gtfs_rt_pb2.FeedMessage()
response = requests.get(url)

# print(response.status_code)

# # JSONとして取得
# response_json = response.json()
# print(response_json)

# # "odpt:railway"が"odpt.Railway:JR-East.ChuoRapid"のものだけ取得
# response_json = [x for x in response_json if x["odpt:railway"] == "odpt.Railway:JR-East.ChuoRapid"]

# # 整形して保存
# with open('train.json', 'w') as f:
#     json.dump(response_json, f)

# exit()

feed.ParseFromString(response.content)
for entity in feed.entity:
    print(entity)
