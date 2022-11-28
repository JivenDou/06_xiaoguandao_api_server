from pydantic import BaseModel


class GetMmsi(BaseModel):
    """获取指定时间内的船只mmsi"""
    startDate: str = "2022-08-31"
    endDate: str = "2022-08-31"


class GetHistoryTrack(BaseModel):
    """获取船只历史轨迹"""
    mmsi: str = "413220010"
    startDate: str = "2022-08-31"
    endDate: str = "2022-08-31"
