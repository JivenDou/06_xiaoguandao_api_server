"""
@File  : xiaoguandao_api.py
@Author: djw
@CreateDate  : 2022/11/4 15:20:30
@Description  : 此文件为小管岛海洋牧场集控页面的接口
"""

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from tortoise import Tortoise
from fastapi.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

# from datetime import datetime
# from datetime import timedelta

app = FastAPI(title='小管岛海洋牧场监测系统接口文档',
              description='用于前端页面获取数据的接口')

# 配置允许域名
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
]
# 配置允许域名列表、允许方法、请求头、cookie等
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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


# ----------------------------------------请求体模板-------------------------------------------
class LoginInfo(BaseModel):
    userName: str = "sencott"
    password: str = "123456"


class GetRealData(BaseModel):
    name: str = "SZ"


# ----------------------------------------接口-------------------------------------------
@app.post("/xiaoguandao/Login", summary="验证登录信息")
async def verify_login(item: LoginInfo):
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


@app.post("/xiaoguandao/realData", summary="获取页面实时数据")
async def real_data(item: GetRealData):
    """
    请求参数说明：
    - "name"：页面名称（类型：str）【参数："SZ"(水质)、"SW"(水文)、"TYN"(太阳能)】
    """
    db = Tortoise.get_connection("default")
    name = item.name
    if name == "SZ":
        sql = "SELECT c23, c24, c25, c26, c27, c28, c29 FROM table_shucai ORDER BY times DESC LIMIT 1"
    elif name == "SW":
        sql = "SELECT c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c22 " \
              "FROM table_shucai ORDER BY times DESC LIMIT 1"
    elif name == "TYN":
        sql = "SELECT c14, c15, c16, c17, c18, c19, c20, c21 " \
              "FROM table_shucai ORDER BY times DESC LIMIT 1"
    else:
        return {"msg": "name error"}

    result = await db.execute_query_dict(sql)
    if result:
        return result[0]
    else:
        return result


@app.get("/xiaoguandao/SW/echartsData")
async def sw_echarts_data():
    """获取水质页echarts数据"""
    db = Tortoise.get_connection("default")


if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=8000,
        reload=False
    )
