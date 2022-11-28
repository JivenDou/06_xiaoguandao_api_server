from pydantic import BaseModel


class GetRealData(BaseModel):
    """获取页面实时数据"""
    pageName: str = "SZ"


class GetEchartsData(BaseModel):
    """获取指定时间参数的echarts图数据"""
    timeRange: str = "HOUR"
    paramName: str = "c24"
