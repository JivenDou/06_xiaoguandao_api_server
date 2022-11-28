from pydantic import BaseModel


class ControlSwitch(BaseModel):
    """控制总电源和绞车电源"""
    name: str = "master"
    status: int = 1


class ControlWinchUpDown(BaseModel):
    """控制绞车上升下降"""
    behavior: str = "up"
    status: int = 1