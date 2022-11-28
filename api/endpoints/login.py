from fastapi import APIRouter
from schemas import login
from tortoise import Tortoise

router = APIRouter()


@router.post("/Login", summary="验证登录信息")
async def verify_login(item: login.LoginInfo):
    """
    请求参数说明：
    - "userName"：用户名（类型：str）
    - "password"：密码（类型：str）
    """
    db = Tortoise.get_connection("default")
    user_name = item.userName
    password = item.password
    sql = f"SELECT * FROM xiaoguandao_user WHERE user_name = '{user_name}' AND password = '{password}'"
    result = await db.execute_query_dict(sql)
    if result:
        return {"msg": "success"}
    else:
        return {"msg": "error"}
