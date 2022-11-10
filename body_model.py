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

