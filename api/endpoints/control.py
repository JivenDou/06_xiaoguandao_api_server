from fastapi import APIRouter
from schemas import control
from core import Tools

router = APIRouter()

# 建立控制电源开关的继电器连接
sock_power_switch = Tools.ModbusRtuConnector(ip="127.0.0.1", port=502)
# 建立控制绞车的PLC连接
sock_winch_up_down = Tools.ModbusTcpConnector(ip="127.0.0.1", port=503)


@router.post("/powerSwitch", summary="控制电源开关")
async def control_power_switch(item: control.ControlSwitch):
    """
    - 请求参数说明：
    - "name"：开关名（类型：str）【参数："master"(总电源开关)、"winch"(绞车电源开关)】
    - "status"：开关状态（类型：int）【参数：0(关)、1(开)】
    - ------
    - 返回参数说明：
    - 返回更改后的开关和状态
    """
    name = item.name
    status = item.status
    if status not in [0, 1]:
        return {"msg": "status error"}

    send_data = {"device_id": 1, "function_code": 5, "start_addr": None, "output_value": None}
    # 判断设置哪个开关
    if name == "master":
        send_data["start_addr"] = 0
    elif name == "winch":
        send_data["start_addr"] = 1
    else:
        return {"msg": "name error"}
    # 设置状态
    send_data["output_value"] = 0 if status else 1
    back_data = sock_power_switch.exec_command(send_data)
    if back_data is None:
        return {"error": "connection fail"}
    elif back_data[1] == 0:
        return {"name": name, "status": 1}
    else:
        return {"name": name, "status": 0}


@router.post("/winchUpDown", summary="控制绞车上升下降")
async def control_winch_up_down(item: control.ControlWinchUpDown):
    """
   - 请求参数说明：
   - "behavior"：行为（类型：str）【参数："up"(上升)、"down"(下降)】
   - "status"：开关状态（类型：int）【参数：0(关)、1()】
   - ------
    - 返回参数说明：
    - 返回此时的行为和状态
   """
    behavior = item.behavior
    status = item.status
    if status not in [0, 1]:
        return {"msg": "status error"}

    send_data = {"device_id": 0, "function_code": 5, "start_addr": None, "output_value": None}
    # 判断设置什么行为
    if behavior == "up":
        send_data["start_addr"] = 3075
    elif behavior == "down":
        send_data["start_addr"] = 3074
    else:
        return {"msg": "behavior error"}
    # 启动行为
    send_data["output_value"] = status
    back_data = sock_winch_up_down.exec_command(send_data)
    # if back_data is None:
    #     return {"error": "connection fail"}
    # else:
    return {"behavior": behavior, "status": status}


@router.get("/getSwitchStatus", summary="获取所有电源开关状态")
async def get_switch_status():
    """
    返回参数说明：
    - "master" : 总开关
    - "winch" : 绞车开关
    - 0/1 : 关/开
    """
    send_data = {"device_id": '1', "function_code": '1', "start_addr": '0', "length": "2"}
    back_data = sock_power_switch.exec_command(send_data)
    if back_data is None:
        return {"error": "connection fail"}
    else:
        return {"master": 0 if back_data[0] else 1, "winch": 0 if back_data[1] else 1}
