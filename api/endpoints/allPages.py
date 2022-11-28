from core import Enums, Tools
from fastapi import APIRouter
from schemas import allPages
from tortoise import Tortoise
from datetime import datetime

router = APIRouter()


@router.post("/realData", summary="获取指定页面实时数据")
async def real_data(item: allPages.GetRealData):
    """
    请求参数说明：
    - "pageName"：页面名称（类型：str）【参数："SZ"(水质)、"SW"(水文)、"TYN"(太阳能)】
    """
    db = Tortoise.get_connection("default")
    page_name = item.pageName
    if page_name == "SZ":
        param_names = Enums.sz_param_name_list
    elif page_name == "SW":
        param_names = Enums.sw_param_name_list
    elif page_name == "TYN":
        param_names = Enums.tyn_param_name_list
    else:
        return {"msg": "page_name error"}

    sql = f"SELECT {','.join(param_names)} FROM xiaoguandao_shucai_tbl ORDER BY times DESC LIMIT 1"
    result = await db.execute_query_dict(sql)
    if result:
        for r in result[0]:
            if result[0][r] is not None:
                result[0][r] = round(result[0][r], 2)
        return result[0]
    else:
        return result


@router.post("/echartsData", summary="获取指定时间参数的echarts图数据")
async def echarts_data(item: allPages.GetEchartsData):
    """
    请求参数说明：
    - "timeRange"：时间段（类型：str）【参数："HOUR"(24小时内)、"WEEK"(一周内)、"MONTH"(一个月内)】
    - "paramName"：参数名（类型：str）【参数："c24"(温度)、"c25"(盐度)、......具体查看点表】
    """
    db = Tortoise.get_connection("default")
    time_range = item.timeRange
    param_name = item.paramName
    table_name = "xiaoguandao_shucai_tbl"
    if param_name not in Enums.param_name_list:
        return {"msg": "param_name error"}
    # 取现在、24小时内、7天内、30天内的时间
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hour_before = Tools.get_time_range(1)
    week_before = Tools.get_time_range(7)
    month_before = Tools.get_time_range(30)
    # 判断时间段
    if time_range == "HOUR":
        sql = f"SELECT times, ROUND({param_name},2) {param_name} FROM `{table_name}` " \
              f"WHERE times >= '{hour_before}' and times <= '{now_time}'"
    elif time_range == "WEEK":
        sql = f"SELECT times, ROUND({param_name},2) {param_name} FROM `{table_name}` " \
              f"WHERE times >= '{week_before}' and times <= '{now_time}'"
    elif time_range == "MONTH":
        sql = f"SELECT times, ROUND({param_name},2) {param_name} FROM `{table_name}` " \
              f"WHERE times >= '{month_before}' and times <= '{now_time}'"
    else:
        return {"msg": "time_range error"}
    # 数据库获取数据
    get_datas = await db.execute_query_dict(sql)
    # 将时间数据提取成数组
    result_time = []
    result_value = []
    for data in get_datas:
        result_time.append(str(data['times']))
        result_value.append(data[param_name])
    # 将提取的数据编成字典返回
    return {'time': result_time, 'value': result_value}
