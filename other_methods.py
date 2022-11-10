"""
@File  : other_methods.py
@Author: djw
@CreateDate  : 2022/11/8 15:20:30
@Description  : 此文件为其他功能函数
"""
from datetime import datetime
from datetime import timedelta


def get_time_range(days):
    """获取从几天前的时间点"""
    times = datetime.now() + timedelta(days=-days)
    return times.strftime('%Y-%m-%d %H:%M:%S')


def get_ais_track(data):
    """获取船只历史轨迹"""
    lon_lat = []
    for his_data in data:
        # 格式化
        temp = [round(his_data["lon"], 5), round(his_data["lat"], 5)]
        # 字典转列表
        lon_lat.append(temp)
    # 去重
    result = []
    for l1 in lon_lat:
        if l1 not in result:
            result.append(l1)
    return result
