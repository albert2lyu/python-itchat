import json
import math
import os
import urllib
import webbrowser
import requests
from PIL import Image

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 扁率


class Geocoding:
    def __init__(self, api_key):
        self.api_key = api_key

    def geocode(self, address):
        """
        利用高德geocoding服务解析地址获取位置坐标
        :param address:需要解析的地址
        :return:
        """
        geocoding = {'s': 'rsv3',
                     'key': self.api_key,
                     'city': '全国',
                     'address': address}
        geocoding = urllib.urlencode(geocoding)
        ret = urllib.urlopen("%s?%s" % (
            "http://restapi.amap.com/v3/geocode/geo", geocoding))

        if ret.getcode() == 200:
            res = ret.read()
            json_obj = json.loads(res)
            if json_obj['status'] == '1' and int(json_obj['count']) >= 1:
                geocodes = json_obj['geocodes'][0]
                lng = float(geocodes.get('location').split(',')[0])
                lat = float(geocodes.get('location').split(',')[1])
                return [lng, lat]
            else:
                return None
        else:
            return None


def gcj02_to_bd09(lng, lat):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    :param lng:火星坐标经度
    :param lat:火星坐标纬度
    :return:
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]


def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]


def wgs84_to_gcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    if out_of_china(lng, lat):  # 判断是否在国内
        return lng, lat
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]


def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return lng, lat
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def bd09_to_wgs84(bd_lon, bd_lat):
    lon, lat = bd09_to_gcj02(bd_lon, bd_lat)
    return gcj02_to_wgs84(lon, lat)


def wgs84_to_bd09(lon, lat):
    lon, lat = wgs84_to_gcj02(lon, lat)
    return gcj02_to_bd09(lon, lat)


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
        0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
        0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)


def get_photo_gps(image_path):
    """
    返回photo坐标[ lng,lat,DateTimeOriginal,DateTime ]  or None
    :return: 
    :lng: 经度
    :lat: 纬度
    :DateTimeOriginal: 拍摄时间
    :DateTime: 最后修改时间
    """
    img = Image.open(image_path)
    try:
        exif_data = img._getexif()
        # print(exif_data)
        if exif_data:
            DateTime = exif_data.get(306)  # 最后修改时间
            DateTimeOriginal = exif_data.get(36867)  # 拍摄时间
            gps_info = exif_data.get(34853)
            gps_n = gps_info.get(2)
            x, y, z = gps_n
            lat = x[0] / x[1] + y[0] / y[1] / 60 + z[0] / z[1] / 3600
            gps_e = gps_info.get(4)
            x, y, z = gps_e
            lng = x[0] / x[1] + y[0] / y[1] / 60 + z[0] / z[1] / 3600
            print( lng, lat)
            result = wgs84_to_gcj02(lng, lat)
            print(result)
            result.append(DateTimeOriginal)
            result.append(DateTime)
            return result
        else:
            print('无法获取图片相关信息')
    except Exception as e:
        print(e)


def get_photo_address(lng, lat):
    locationstr = '{},{}'.format(lng, lat)
    url = 'http://restapi.amap.com/v3/geocode/regeo'  # 高德地图api接口
    key = 'e5aab0a759f5dcd02b55f4f576fd3495'
    res = requests.get(url, params={'location': locationstr, 'key': key})
    if res.status_code == 200:
        data = res.json()
        if data.get('regeocode'):
            address = data.get('regeocode').get('formatted_address')
            return address


if __name__ == '__main__':
    imageName = '20170707134501.jpg' # 当前目录下的图片 必须是相机手机拍摄的图片
    result = get_photo_gps(imageName)
    if result:
        address = get_photo_address(result[0], result[1])
        if address:
            location = '{},{}'.format(round(result[0], 6), round(result[1], 6))
            # open_url = 'http://restapi.amap.com/v3/staticmap?location={}&zoom=10&size=400*400&labels={},2,0,16,0xFFFFFF,0x008000:{}&key=e5aab0a759f5dcd02b55f4f576fd3495&scale=2'.format(
            #     location, address[-14:], location)
            long_html = '<!doctype html><html><head><meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="initial-scale=1,user-scalable=no,width=device-width"><title>图片定位</title><link rel="stylesheet" href="http://cache.amap.com/lbs/static/main1119.css"><script src="http://webapi.amap.com/maps?v=1.3&key=140ac13fc32c621ff09443aad312385d"></script><script type="text/javascript" src="http://cache.amap.com/lbs/static/addToolbar.js"></script></head><body><div id="container"></div><div id="tip" class="tip">鼠标移入点标记试试</div><script>var map=new AMap.Map("container",{resizeEnable:!0,center:['+str(round(result[0], 6))+','+str(round(result[1], 6))+'],zoom:13}),marker=new AMap.Marker({position:map.getCenter()});marker.setMap(map),marker.setTitle("'+address+'"),marker.setLabel({offset:new AMap.Pixel(20,20),content:"'+address+'"});</script></body></html>'
            # long_html = long_html.format(
            #     round(result[0], 6), round(result[1], 6), address, address)
            with open('map.html', 'w+',encoding='utf-8') as f:
                f.write(long_html)
            webbrowser.open('map.html')
            print('定位地址:{},拍摄时间:{}'.format(address, result[2]))
