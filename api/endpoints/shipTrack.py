from fastapi import APIRouter
from schemas import shipTrack
from tortoise import Tortoise

router = APIRouter()


@router.post("/getMmsi", summary="获取时间段内船只的mmsi")
async def get_ship_names(item: shipTrack.GetMmsi):
    """
    请求参数说明：
    - "startDate"：开始日期（类型：str）【参数格式："YYYY-MM-DD"】
    - "endDate"：结束日期（类型：str）【参数格式："YYYY-MM-DD"】
    """
    db = Tortoise.get_connection("default")
    start_date = item.startDate
    end_date = item.endDate
    table_name = "xiaoguandao_ais_history_tbl"
    if start_date == end_date:
        sql = f"SELECT mmsi FROM `{table_name}` WHERE date_format(times,'%Y-%m-%d')='{start_date}' " \
              "AND mmsi!='000000000' GROUP BY mmsi"
    else:
        sql = f"SELECT mmsi FROM `{table_name}` WHERE times >= '{start_date}' AND times <= '{end_date}' " \
              "AND mmsi!='000000000' GROUP BY mmsi"
    result = await db.execute_query_dict(sql)
    return result


@router.post("/getHistoryTrack", summary="获取船只的历史轨迹")
async def get_history_track(item: shipTrack.GetHistoryTrack):
    """
    请求参数说明：
    - "mmsi"：船只mmsi（类型：str）【参数："413220010"】
    - "startDate"：开始日期（类型：str）【参数格式："YYYY-MM-DD"】
    - "endDate"：结束日期（类型：str）【参数格式："YYYY-MM-DD"】
    """
    db = Tortoise.get_connection("default")
    mmsi = item.mmsi
    start_date = item.startDate
    end_date = item.endDate
    table_name = "xiaoguandao_ais_history_tbl"
    if start_date == end_date:
        sql = f"SELECT times, lon, lat FROM `{table_name}` " \
              f"WHERE mmsi={mmsi} AND date_format(times,'%Y-%m-%d')='{start_date}'"
    else:
        sql = f"SELECT times, lon, lat FROM `{table_name}` " \
              f"WHERE mmsi={mmsi} AND times >= '{start_date}' AND times <= '{end_date}'"
    result = await db.execute_query_dict(sql)
    return result
