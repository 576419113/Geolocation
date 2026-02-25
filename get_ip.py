#!/usr/bin/env python3
import requests
import time
import os
# 可配置区域
clean_method=[20,8]         #每当有20条清理8条
ip_file="resource/ip.txt"   #记录保存位置
# 可配置区域结束
current_time = time.localtime()
format_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
line_lists=[]           #读入历史数据
last_line=""            #在历史数据中识别到的非空最后一行
ipv4_local=""           #从历史得到的ipv4地址
ipv4_web="127.0.1.1"    #从云端得到的ipv4地址
cover_mod=False         #是否覆盖上一条记录
clean_mod=False         #是否要清理历史记录
# 当前使用的api
# https://openapi.lddgo.net/base/gtool/api/v1/GetIp
def update():
    global ipv4_local
    global ipv4_web
    global line_lists
    if os.path.exists(ip_file):
        with open(ip_file, "r") as f:
            line_lists=f.readlines()
        # 自动清理文件
        if(len(line_lists)>=clean_method[0]):
            del line_lists[:clean_method[1]]
            with open(ip_file,"w") as f:
                f.writelines(line_lists)
    # 读入并处理历史记录
    if(line_lists):
        # 逆序读入
        for line in line_lists[::-1]:
            if line!="\n":
                last_line=line
                break
        last_time, last_ipv4 = [item.strip(" ") for item in last_line.split("=>")]
        ipv4_local=last_ipv4
    # 从web服务中更新数据
    try:
        response = requests.get('https://openapi.lddgo.net/base/gtool/api/v1/GetIp')
        ipv4_web=response.json()["data"]["ip"]
    except:
        ipv4_web="127.0.1.1"
    # 开始生成目标数据
    global cover_mod
    if(ipv4_web.split(".")[0]!="127"):
        if(ipv4_local==ipv4_web):
            cover_mod=True
        for i in range(len(line_lists)):
            if line_lists[i]=="\n":
                del line_lists[i]
        if(cover_mod):
            del line_lists[-1]
        line_lists.append(f"{format_time} => {ipv4_web}")
        with open(ip_file,"w") as ipf:
            ipf.writelines(line_lists)
def get():
    # 返回最后一行
    with open(ip_file, "r") as f:
        line_lists=f.readlines()
        for line in line_lists[::-1]:
            if line!="\n":
                last_line=line
                break
        last_time, last_ipv4 = [item.strip(" ") for item in last_line.split("=>")]
    return last_ipv4
