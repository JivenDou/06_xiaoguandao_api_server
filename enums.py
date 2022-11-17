"""
@File  : enums.py
@Author: djw
@CreateDate  : 2022/11/8 15:20:30
@Description  : 此文件存放各枚举类
"""
from enum import Enum

param_name_list = ["c1", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12", "c13", "c14", "c15", "c16",
                   "c17", "c18", "c19", "c20", "c21", "c22", "c23", "c24", "c25", "c26", "c27", "c28", "c29"]

sz_param_name_list = ["c23", "c24", "c25", "c26", "c27", "c28", "c29"]
sw_param_name_list = ["c1", "c3", "c4", "c5", "c6", "c7", "c8", "c9", "c10", "c11", "c12", "c13", "c22"]
tyn_param_name_list = ["c14", "c15", "c16", "c17", "c18", "c19", "c20", "c21"]

cnum2chinese = {
        "times": "时间",
        "c1": "压力(kpa)",
        "c3": "潮位压力(kpa)",
        "c4": "潮位(m)",
        "c5": "有效波高(m)",
        "c6": "最大波高(m)",
        "c7": "平均周期(s)",
        "c8": "峰值波周期(s)",
        "c9": "能量周期(s)",
        "c10": "平均跨零周期(s)",
        "c11": "坡陡",
        "c12": "不规则度",
        "c13": "截断频率(HZ)",
        "c14": "逆变器电压(V)",
        "c15": "逆变器电流(A)",
        "c16": "逆变器有功功率(W)",
        "c17": "蓄电池剩余电量(%)",
        "c18": "蓄电池电压(V)",
        "c19": "蓄电池电流(A)",
        "c20": "太阳能电压(V)",
        "c21": "太阳能电流(A)",
        "c22": "雷达液位计(cm)",
        "c24": "温度(℃)",
        "c25": "盐度(psu)",
        "c28": "深度(m)",
        "c23": "溶解氧(mg/L)",
        "c27": "叶绿素(μg/L)",
        "c29": "浊度(NTU)",
        "c26": "PH值",
    }
# class IoPointName(str, Enum):
#     """点名对应序列号"""
#     water_pressure = "c1"
#     water_mark_pressure = "c3"
#     water_mark = "c4"
#     valid_wave_height = "c5"
#     max_wave_height = "c6"
#     avg_period = "c7"
