from fastapi import APIRouter
from tortoise import Tortoise
from datetime import datetime
from core import Tools

router = APIRouter()


@router.get("/maxMinAvg", summary="获取24小时内最大最小平均表格数据")
async def sz_max_min_avg():
    """
    说明：
    - 返回的数据顺序：温度 盐度 深度 溶解氧 叶绿素 浊度 PH
    """
    db = Tortoise.get_connection("default")
    table_name = "xiaoguandao_shucai_tbl"
    # 取现在和前一天的时间
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hour_before = Tools.get_time_range(1)
    # 参数名顺序对应 温度 盐度 深度 溶解氧 叶绿素 浊度 PH
    param_names = ['c24', 'c25', 'c28', 'c23', 'c27', 'c29', 'c26']
    result = []
    for name in param_names:
        sql = f"SELECT ROUND(AVG({name}),2 ) avg,ROUND(MAX({name}),2 ) AS max,ROUND(MIN({name}),2 ) AS min " \
              f"FROM `{table_name}` WHERE times >= '{hour_before}' and times <= '{now_time}'"
        temp = await db.execute_query_dict(sql)
        temp[0]['name'] = name
        result.append(temp[0])
    return result


@router.get("/aisTarget", summary="获取ais数据")
async def sz_ais_target():
    """
    说明：
    - 返回所有船只实时信息和历史轨迹
    """
    db = Tortoise.get_connection("default")
    # 查询所有船只实时信息
    now_time = '2022-09-06 08:38:00'
    before_minute = 40
    sql = "SELECT times, mmsi, shipname, lon, lat, speed, course, heading, status, callsign, destination " \
          "FROM xiaoguandao_ais_tbl WHERE mmsi != \"000000000\" " \
          "AND lon>0 AND lon<180 AND lat>0 AND lat<180 " \
          f"AND times >= '{now_time}'-interval {before_minute} minute AND times <= '{now_time}'"
    ais_datas = await db.execute_query_dict(sql)
    # 遍历每条船只信息
    for data in ais_datas:
        # data = {'times': datetime.datetime(2022, 9, 6, 12, 35, 19), 'mmsi': '413255940', 'shipname': None,
        # 'lon': 120.96054, 'lat': 37.96589, 'speed': 10.1, 'course': 99.5, 'heading': 101.0,
        # 'status': 'UnderWayUsingEngine', 'callsign': None, 'destination': None}

        # 添加历史轨迹
        sql = f"SELECT lon, lat FROM xiaoguandao_ais_history_tbl WHERE mmsi = \'{data['mmsi']}\'" \
              f"AND lon>0 AND lon<180 AND lat>0 AND lat<180"
        history_datas = await db.execute_query_dict(sql)
        data["track"] = Tools.get_ais_track(history_datas)
        data["times"] = str(data["times"])
        data["lon"] = round(data["lon"], 5)
        data["lat"] = round(data["lat"], 5)

    return ais_datas
