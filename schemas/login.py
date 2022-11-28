from pydantic import BaseModel


class LoginInfo(BaseModel):
    """验证登录信息"""
    userName: str = "sencott"
    password: str = "123456"
