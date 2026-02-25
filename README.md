# Geoclue2 Location Serve
此项目用于解决Linux上的geoclue2定位问题，采用ip地址+本地解析的方法，增强定位可用性。
## 鸣谢
本项目使用到了以下项目：
[GeoCN](https://github.com/ljxi/GeoCN) - 提供了将ip地址高质量转换成地区名的方法
[city-geo](https://github.com/88250/city-geo) - 提供了将地区名转换为经纬度的方法
## 工作原理
get_ip.py用于使用互联网上的api得到ipv4地址(目前只有)
ip2city.py使用mmdb把ipv4或者ipv6地址转换成地区名(ipv4无法精确到区，ipv6极大概率可以，详见GeoCN)
city2loc.py将地区名转换成经纬度(可以不传入区的参数)
main.py使用fastapi制作，制作比较粗糙，同时加入了各种请求时间限制，防止上游ip地址提供方封禁ip。
## 使用说明
修改geoclue2配置文件`/etc/geoclue/geoclue.conf`:
```
url=http://127.0.0.1:8000/
```
ip地址转换为地名的数据更新工具位于`resource/updata.sh`
本python程序依赖见requirement:
```
maxminddb
fastapi
uvicorn
```
注：可以使用conda环境等多种手段，推荐python=3.9(不是我规定的，见GeoCN项目的Dokerfile文件)
注：为什么不做成system service？内存占用100MB，做成系统服务不合适，手动即可(192GB内存豪哥除外)
然后对网址`http://127.0.0.1:8000/`POST一下就可以测试结果
## 恰饭
![](resource/wechat.jpg)
![](resource/alipay.jpg)
