from pydantic import BaseModel


class GetHistoryData(BaseModel):
    """获取不同表的历史数据"""
    pageName: str = "SZ"
    startDate: str = "2022-11-11"
    endDate: str = "2022-11-11"
    excel: int = 0
