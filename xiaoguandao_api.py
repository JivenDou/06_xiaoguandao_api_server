"""
@File  : xiaoguandao_api.py
@Author: djw
@CreateDate  : 2022/11/4 15:20:30
@Description  : 此文件为小管岛海洋牧场集控页面的接口
"""

import uvicorn
import body_model
import enums
import other_methods
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise
from tortoise.contrib.fastapi import register_tortoise
from datetime import datetime
from enums import param_name_list

app = FastAPI(title='小管岛海洋牧场监测系统接口文档',
              description='好好工作！努力赚钱！！')
# 配置允许域名
# origins = [
#     "http://localhost.tiangolo.com",
#     "https://localhost.tiangolo.com",
#     "http://localhost",
#     "http://localhost:8080",
#     "http://192.168.1.30",
# ]
# 配置允许域名列表、允许方法、请求头、cookie等
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])
# 连接数据库
register_tortoise(
    app,
    db_url='mysql://root:zzZZ4144670..@127.0.0.1:3306/shucai_xiaoguandao',
    modules={"models": []},
    generate_schemas=True,
    add_exception_handlers=True)


# ----------------------------------------接口-------------------------------------------
@app.post("/xiaoguandao/Login", summary="验证登录信息")
async def verify_login(item: body_model.LoginInfo):
    """
    请求参数说明：
    - "userName"：用户名（类型：str）
    - "password"：密码（类型：str）
    """
    db = Tortoise.get_connection("default")
    user_name = item.userName
    password = item.password
    sql = f"SELECT * FROM user WHERE user_name = '{user_name}' AND password = '{password}'"
    result = await db.execute_query_dict(sql)
    if result:
        return {"msg": "success"}
    else:
        return {"msg": "error"}


@app.post("/xiaoguandao/realData", summary="获取指定页面实时数据")
async def real_data(item: body_model.GetRealData):
    """
    请求参数说明：
    - "pageName"：页面名称（类型：str）【参数："SZ"(水质)、"SW"(水文)、"TYN"(太阳能)】
    """
    db = Tortoise.get_connection("default")
    page_name = item.pageName
    if page_name == "SZ":
        param_names = enums.sz_param_name_list
    elif page_name == "SW":
        param_names = enums.sw_param_name_list
    elif page_name == "TYN":
        param_names = enums.tyn_param_name_list
    else:
        return {"msg": "page_name error"}

    sql = f"SELECT {','.join(param_names)} FROM table_shucai ORDER BY times DESC LIMIT 1"
    result = await db.execute_query_dict(sql)
    if result:
        for r in result[0]:
            if result[0][r] is not None:
                result[0][r] = round(result[0][r], 2)
        return result[0]
    else:
        return result


@app.post("/xiaoguandao/echartsData", summary="获取指定时间参数的echarts图数据")
async def echarts_data(item: body_model.GetEchartsData):
    """
    请求参数说明：
    - "timeRange"：时间段（类型：str）【参数："HOUR"(24小时内)、"WEEK"(一周内)、"MONTH"(一个月内)】
    - "paramName"：参数名（类型：str）【参数："c24"(温度)、"c25"(盐度)、......具体查看点表】
    """
    db = Tortoise.get_connection("default")
    time_range = item.timeRange
    param_name = item.paramName
    if param_name not in param_name_list:
        return {"msg": "param_name error"}
    # 取现在、24小时内、7天内、30天内的时间
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hour_before = other_methods.get_time_range(1)
    week_before = other_methods.get_time_range(7)
    month_before = other_methods.get_time_range(30)
    # 判断时间段
    if time_range == "HOUR":
        sql = f"SELECT times, ROUND({param_name},2) {param_name} FROM `table_shucai` " \
              f"WHERE times >= '{hour_before}' and times <= '{now_time}'"
    elif time_range == "WEEK":
        sql = f"SELECT times, ROUND({param_name},2) {param_name} FROM `table_shucai` " \
              f"WHERE times >= '{week_before}' and times <= '{now_time}'"
    elif time_range == "MONTH":
        sql = f"SELECT times, ROUND({param_name},2) {param_name} FROM `table_shucai` " \
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


@app.post("/xiaoguandao/History/historyData", summary="历史数据页：获取历史数据")
async def history_data(item: body_model.GetHistoryData):
    """
    请求参数说明：
    - "pageName"：页面名（类型：str）【参数："SZ"(水质)、"SW"(水文)、"TYN"(太阳能)】
    - "startDate"：开始日期（类型：str）【参数格式："YYYY-MM-DD"】
    - "endDate"：结束日期（类型：str）【参数格式："YYYY-MM-DD"】
    - "excel"：是否下载excel（类型：int）【参数：0（不下载只要数据）、1（要下载）】
    """
    db = Tortoise.get_connection("default")
    page_name = item.pageName
    start_date = item.startDate
    end_date = item.endDate
    excel_flag = item.excel
    # --------------------------------------------------查数据--------------------------------------------------
    if page_name == "SZ":
        param_names = enums.sz_param_name_list
    elif page_name == "SW":
        param_names = enums.sw_param_name_list
    elif page_name == "TYN":
        param_names = enums.tyn_param_name_list
    else:
        return {"msg": "page_name error"}

    select_params = [f"ROUND({name},2)  {name}" for name in param_names]
    if start_date == end_date:
        sql = f"SELECT id,times,{','.join(select_params)} FROM `table_shucai` " \
              f"WHERE date_format(times,'%Y-%m-%d')='{start_date}' ORDER BY times DESC;"
    else:
        sql = f"SELECT id,times,{','.join(select_params)} FROM `table_shucai` " \
              f"WHERE times >= '{start_date} 00:00:00' AND times <= '{end_date} 23:59:59' ORDER BY times DESC;"
    result = await db.execute_query_dict(sql)
    for data in result:
        data['times'] = str(data['times'])
    # --------------------------------------------------返回excel--------------------------------------------------
    if excel_flag:
        df = pd.DataFrame(result)
        df.rename(columns=enums.cnum2chinese, inplace=True)
        # print(df)
        # 生成excel文件
        df.to_excel('./otherFile/excel.xlsx', sheet_name='Sheet1', index=False)  # index false为不写入索引
        headers = {'Content-Disposition': 'attachment; filename="excel.xlsx"'}
        return FileResponse('./otherFile/excel.xlsx', headers=headers)
    else:
        return result


@app.post("/xiaoguandao/ShipTrack/getMmsi", summary="船只轨迹页：获取时间段内船只的mmsi")
async def get_ship_names(item: body_model.GetMmsi):
    """
    请求参数说明：
    - "startDate"：开始日期（类型：str）【参数格式："YYYY-MM-DD"】
    - "endDate"：结束日期（类型：str）【参数格式："YYYY-MM-DD"】
    """
    db = Tortoise.get_connection("default")
    start_date = item.startDate
    end_date = item.endDate
    if start_date == end_date:
        sql = f"SELECT mmsi FROM `ais_data_history` WHERE date_format(times,'%Y-%m-%d')='{start_date}' " \
              "AND mmsi!='000000000' GROUP BY mmsi"
    else:
        sql = f"SELECT mmsi FROM `ais_data_history` WHERE times >= '{start_date}' AND times <= '{end_date}' " \
              "AND mmsi!='000000000' GROUP BY mmsi"
    result = await db.execute_query_dict(sql)
    return result


@app.post("/xiaoguandao/ShipTrack/getHistoryTrack", summary="船只轨迹页：获取船只的历史轨迹")
async def get_history_track(item: body_model.GetHistoryTrack):
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
    if start_date == end_date:
        sql = f"SELECT times, lon, lat FROM `ais_data_history` " \
              f"WHERE mmsi={mmsi} AND date_format(times,'%Y-%m-%d')='{start_date}'"
    else:
        sql = f"SELECT times, lon, lat FROM `ais_data_history` " \
              f"WHERE mmsi={mmsi} AND times >= '{start_date}' AND times <= '{end_date}'"
    result = await db.execute_query_dict(sql)
    return result


@app.post("/xiaoguandao/control/powerSwitch", summary="控制电源开关(未完成)")
async def control_power_switch(item: body_model.ControlSwitch):
    """
    请求参数说明：
    - "masterSta"：总电源开关状态（类型：int）【参数：0(关)、1(开)】
    - "winchSta"：绞车电源开关状态（类型：int）【参数：0(关)、1(开)】
    """
    master_status = item.masterSta
    winch_status = item.winchSta
    if master_status not in [0, 1] or winch_status not in [0, 1]:
        return {"msg": "master_status or winch_status error"}
    # 建立连接
    sock = other_methods.ModbusRtuConnector(ip="192.168.2.200", port=4001)
    send_data = {"device_id": '', "function_code": '', "start_addr": '', "output_value": ''}
    # 判断命令
    if master_status and winch_status:
        pass
    elif master_status:
        pass
    elif winch_status:
        pass
    else:
        pass
    back_data = sock.exec_command(send_data)
    print(back_data)


@app.get("/xiaoguandao/control/getSwitchStatus", summary="获取电源开关状态(未完成)")
async def get_switch_status():
    """
    说明：
    - 获取电源开关状态
    """
    # 建立socket连接
    sock = other_methods.ModbusRtuConnector(ip="192.168.2.200", port=4001)
    send_data = {"device_id": '', "function_code": '', "start_addr": ''}
    back_data = sock.exec_command(send_data)
    print(back_data)


@app.get("/xiaoguandao/SZ/maxMinAvg", summary="水质页：获取24小时内最大最小平均表格数据")
async def sz_max_min_avg():
    """
    说明：
    - 返回的数据顺序：温度 盐度 深度 溶解氧 叶绿素 浊度 PH
    """
    db = Tortoise.get_connection("default")
    # 取现在和前一天的时间
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hour_before = other_methods.get_time_range(1)
    # 参数名顺序对应 温度 盐度 深度 溶解氧 叶绿素 浊度 PH
    param_names = ['c24', 'c25', 'c28', 'c23', 'c27', 'c29', 'c26']
    result = []
    for name in param_names:
        sql = f"SELECT ROUND(AVG({name}),2 ) avg,ROUND(MAX({name}),2 ) AS max,ROUND(MIN({name}),2 ) AS min " \
              f"FROM `table_shucai` WHERE times >= '{hour_before}' and times <= '{now_time}'"
        temp = await db.execute_query_dict(sql)
        temp[0]['name'] = name
        result.append(temp[0])
    return result


@app.get("/xiaoguandao/SZ/aisTarget", summary="水质页：获取ais数据")
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
          "FROM table_ais WHERE mmsi != \"000000000\" " \
          "AND lon>0 AND lon<180 AND lat>0 AND lat<180 " \
          f"AND times >= '{now_time}'-interval {before_minute} minute AND times <= '{now_time}'"
    ais_datas = await db.execute_query_dict(sql)
    # 遍历每条船只信息
    for data in ais_datas:
        # data = {'times': datetime.datetime(2022, 9, 6, 12, 35, 19), 'mmsi': '413255940', 'shipname': None,
        # 'lon': 120.96054, 'lat': 37.96589, 'speed': 10.1, 'course': 99.5, 'heading': 101.0,
        # 'status': 'UnderWayUsingEngine', 'callsign': None, 'destination': None}

        # 添加历史轨迹
        sql = f"SELECT lon, lat FROM ais_data_history WHERE mmsi = \'{data['mmsi']}\'" \
              f"AND lon>0 AND lon<180 AND lat>0 AND lat<180"
        history_datas = await db.execute_query_dict(sql)
        data["track"] = other_methods.get_ais_track(history_datas)
        data["times"] = str(data["times"])
        data["lon"] = round(data["lon"], 5)
        data["lat"] = round(data["lat"], 5)

    return ais_datas


if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host="0.0.0.0",
        port=8000,
        reload=False
    )
