# -*- coding:utf-8 -*-
"""
@Time : 2022/11/25 17:30
@Author: djw
@Des: 路由聚合
"""

from api.api import api_router
# from views.views import views_router
from fastapi import APIRouter


router = APIRouter()
# API路由
router.include_router(api_router)
# 视图路由
# router.include_router(views_router)
