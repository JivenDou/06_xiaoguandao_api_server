"""
@File  : body_model.py
@Author: djw
@CreateDate  : 2022/11/9 15:20:30
@Description  : 此文件存放各接口请求体模板类
"""
from pydantic import BaseModel


class LoginInfo(BaseModel):
    """验证登录信息"""
    userName: str = "sencott"
    password: str = "123456"


class GetRealData(BaseModel):
    """获取页面实时数据"""
    pageName: str = "SZ"


class GetEchartsData(BaseModel):
    """获取指定时间参数的echarts图数据"""
    timeRange: str = "HOUR"
    paramName: str = "c24"


class GetHistoryData(BaseModel):
    """获取不同表的历史数据"""
    pageName: str = "SZ"
    startDate: str = "2022-11-11"
    endDate: str = "2022-11-11"
    excel: int = 0


class GetMmsi(BaseModel):
    """获取指定时间内的船只mmsi"""
    startDate: str = "2022-08-31"
    endDate: str = "2022-08-31"


class GetHistoryTrack(BaseModel):
    """获取船只历史轨迹"""
    mmsi: str = "413220010"
    startDate: str = "2022-08-31"
    endDate: str = "2022-08-31"


class ControlSwitch(BaseModel):
    """控制总电源和绞车电源"""
    name: str = "master"
    status: int = 1


class ControlWinchUpDown(BaseModel):
    """控制绞车上升下降"""
    behavior: str = "up"
    status: int = 1
