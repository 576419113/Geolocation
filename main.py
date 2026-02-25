#!/usr/bin/env python3
import get_ip
import ip2city
import city2loc
import json
import os
import time
from fastapi import FastAPI
# 可配置区域
time_freq=3600*0.75                #更新频率最快0.75小时
map_file="resource/map.json"       #对应表保存位置
time_file="resource/time.txt"      #记录上一次访问时间
time_lists=[]                      #访问时间列表
time_clean_method=[120,40]         #访问时间清理
# 可配置区域结束
# 接口一览
# get_ip.update()        #更新本地公网ip地址缓存，无返回
# get_ip.get()           #获取ip地址，返回字符串
# ip2city.query(ip)      #传入ipv4或ipv6地址，ipv6应该才有区，返回字符串
# city2loc.location(province, city, area)      #传入三个字符串，area可为空字符串，返回字典{"lat":lat,"lng":lng}
# 目标返回格式
# {
#     "location": {
#         "lat": -22.7539192,
#         "lng": -43.4371081
#     },
#     "accuracy": 100.0
# }
# 尝试解析本地映射表
def map_ip2loc(ip):
    map_json={}
    if not os.path.exists(map_file):
        return 0
    with open(map_file, "r") as mf:
        map_json=json.load(mf)
    map_result=map_json.get(ip)
    if(map_result):
        return map_result
    else:
        return 0
# 构造请求方式
app = FastAPI()
@app.post("/")
async def read_root():
    # 访问时间控制
    main_cur_time = time.localtime()
    main_cf_time = time.strftime("%Y-%m-%d %H:%M:%S", main_cur_time)
    main_last_time=""
    global time_lists
    if os.path.exists(time_file):
        with open(time_file, "r") as tf:
            time_lists=tf.readlines()
        # 自动清理访问时间
        if(len(time_lists)>=time_clean_method[0]):
            del time_lists[:time_clean_method[1]]
            with open(time_file,"w") as f:
                f.writelines(time_lists)
    # 是否需要更新ip地址
    need_update=False
    # 读入并处理时间列表
    if(time_lists):
        # 逆序读入
        for tline in time_lists[::-1]:
            if tline!="\n":
                main_last_time=tline.strip("\n")
                break
        # 转换为时间结构
        main_last_time_t = time.strptime(main_last_time, "%Y-%m-%d %H:%M:%S")
        main_current_time_t = time.strptime(main_cf_time, "%Y-%m-%d %H:%M:%S")
        # 得到差值，单位为秒
        main_dtime=time.mktime(main_current_time_t)-time.mktime(main_last_time_t)
        if(main_dtime>=time_freq):
            need_update=True
        else:
            need_update=False
        # 确保可以get_ip
        if not os.path.exists("resource/ip.txt"):
            need_update=True
    else:
        need_update=True
    with open(time_file,"a+") as tf:
        tf.write(main_cf_time+"\n")
    if(need_update):
        get_ip.update()
    ip_str=get_ip.get()
    # 在本地缓存中使用ip查询经纬度
    ip_map=map_ip2loc(ip_str)
    if(not ip_map):
        city_str=ip2city.query(ip_str).split(" ")
        p=c=a=""
        if(len(city_str)==2):
            p,c=city_str
        else:
            p,c,a=city_str
        result=city2loc.location(p,c,a)
        # 将新的映射写入映射表
        mmap_json={}
        if os.path.exists(map_file):
            with open(map_file, "r") as mmf:
                mmap_json=json.load(mmf)
        mmap_json[ip_str]=result
        with open(map_file, "w") as mff:
            json.dump(mmap_json, mff, ensure_ascii=False, indent=4)
    else:
        result=ip_map
    # 向程序返回结果
    return {
        "location": {
            "lat": float(result["lat"]),
            "lng": float(result["lng"])
            },
        "accurancy": 100.0
        }
