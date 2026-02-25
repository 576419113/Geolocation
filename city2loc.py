#!/usr/bin/env python3
import json
data=[]
with open('resource/data.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
def location(province, city, area):
    lat=0.0
    lng=0.0
    for one in data:
        if(one["province"]==province and one["city"]==city and one["area"]==area):
            lat=one["lat"]
            lng=one["lng"]
            break
    return{"lat":lat,"lng":lng}
