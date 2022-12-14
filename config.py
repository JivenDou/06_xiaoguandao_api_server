import os
from pydantic import BaseSettings
from typing import List


class Config(BaseSettings):
    # 调试模式
    APP_DEBUG: bool = False
    # 接口ip和端口
    API_IP: str = "0.0.0.0"
    API_PORT: int = 8000
    RELOAD: bool = False
    # 数据库连接
    DB_USERNAME: str = "root"
    DB_PASSWORD: str = "zzZZ4144670.."
    DB_IP: str = "127.0.0.1"
    DB_PORT: str = "3306"
    DATABASE: str = "shucai_xiaoguandao"
    # 项目信息
    VERSION: str = "0.0.1"
    PROJECT_NAME: str = "小管岛海洋牧场监测系统接口文档"
    DESCRIPTION: str = '<a href="" target="_blank">好好工作！努力赚钱！！</a>'
    # 静态资源目录
    STATIC_DIR: str = os.path.join(os.getcwd(), "static")
    TEMPLATE_DIR: str = os.path.join(STATIC_DIR, "templates")
    # 跨域请求
    CORS_ORIGINS: List = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]


settings = Config()
