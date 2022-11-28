from fastapi import APIRouter
from api.endpoints import login, sz, allPages, historyData, shipTrack, control

api_router = APIRouter()
api_router.include_router(login.router, prefix='/User', tags=["用户登录页"])
api_router.include_router(sz.router, prefix='/SZ', tags=["水质页"])
api_router.include_router(allPages.router, prefix='/AllPages', tags=["应用水质、水文、太阳能页"])
api_router.include_router(historyData.router, prefix='/History', tags=["历史数据页"])
api_router.include_router(shipTrack.router, prefix='/ShipTrack', tags=["船只轨迹页"])
api_router.include_router(control.router, prefix='/Control', tags=["控制窗口"])
