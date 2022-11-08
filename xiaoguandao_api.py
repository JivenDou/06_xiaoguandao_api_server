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

app = FastAPI()

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


# ----------------------------------------登录页接口-------------------------------------------
class LoginInfo(BaseModel):
    userName: str = "sencott"
    password: str = "123456"


@app.post("/xiaoguandao/Login")
async def verify_login(item: LoginInfo):
    """验证登录信息"""
    db = Tortoise.get_connection("default")
    user_name = item.userName
    password = item.password
    sql = f"SELECT * FROM user WHERE user_name = '{user_name}' AND password = '{password}'"
    result = await db.execute_query_dict(sql)
    if result:
        return {"msg": "success"}
    else:
        return {"msg": "error"}


# ----------------------------------------水质页接口-------------------------------------------
@app.get("/xiaoguandao/SZ/realData")
async def sz_real_data():
    """水质实时数据"""
    db = Tortoise.get_connection("default")
    sql = "SELECT c23, c24, c25, c26, c27, c28, c29 FROM table_shucai ORDER BY times DESC LIMIT 1"
    result = await db.execute_query_dict(sql)
    if result:
        return result[0]
    else:
        return result


# ----------------------------------------水文页接口-------------------------------------------
@app.get("/xiaoguandao/SW/realData")
async def sw_real_data():
    """水文实时数据"""
    db = Tortoise.get_connection("default")
    sql = "SELECT c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c22 " \
          "FROM table_shucai ORDER BY times DESC LIMIT 1"
    result = await db.execute_query_dict(sql)
    if result:
        return result[0]
    else:
        return result


# ----------------------------------------太阳能页接口-------------------------------------------
@app.get("/xiaoguandao/TYN/realData")
async def tyn_real_data():
    """太阳能实时数据"""
    db = Tortoise.get_connection("default")
    sql = "SELECT c14, c15, c16, c17, c18, c19, c20, c21 " \
          "FROM table_shucai ORDER BY times DESC LIMIT 1"
    result = await db.execute_query_dict(sql)
    if result:
        return result[0]
    else:
        return result


if __name__ == '__main__':
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=8000,
        reload=False
    )
