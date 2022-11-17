"""
@File  : other_methods.py
@Author: djw
@CreateDate  : 2022/11/8 15:20:30
@Description  : 此文件为其他功能函数
"""
from datetime import datetime
from datetime import timedelta
from modbus_tk import modbus_rtu_over_tcp
import time
import json


class ModbusRtuConnector:
    """ModbusRtu连接器"""
    def __init__(self, ip, port):
        self.__ip = ip
        self.__port = port
        self.__size = 1024
        self._master = None
        self.__connected = False
        self.connect()

    def connect(self):
        try:
            self._master = modbus_rtu_over_tcp.RtuOverTcpMaster(host=self.__ip, port=self.__port)
            print(f"{self.__ip}:{self.__port} connect success!")
        except Exception as e:
            print(f'Error in modbus_tcp_connector.__connect: {repr(e)}')
            self.__connected = False
            # self.reconnect()

    def reconnect(self):
        while True:
            try:
                self._master = modbus_rtu_over_tcp.RtuOverTcpMaster(host=self.__ip, port=self.__port)
                print('client start connect to host/port:{}'.format(self.__port))
                break
            except ConnectionRefusedError:
                print('modbus server refused or not started, reconnect to server in 5s .... host/port:{}'.format(
                    self.__port))
                time.sleep(5)
            except Exception as e:
                print('do connect error:{}'.format(str(e)))
                time.sleep(5)

    def exec_command(self, dic_data):
        """发送数据"""
        if isinstance(dic_data, str):
            command = json.loads(dic_data)
        else:
            command = dic_data
        device_id = int(command['device_id'])
        function_code = int(command['function_code'])
        start_addr = int(command['start_addr'])
        if function_code in (1, 2, 3, 4):
            # 读寄存器
            length = int(command['length'])
            try:
                self._master.set_timeout(3.0)  # modbus读取数据超时时间设置
                self._master.set_verbose(True)
                # print(device_id, ' ', function_code, " ", start_addr, " ", length)
                receive_data = self._master.execute(device_id, function_code, start_addr, length)
                # print("receive_data:", receive_data)

                # datadict = {}
                # for i in range(len(receive_data)):
                #     addr = start_addr + i
                #     datadict[addr] = receive_data[i]
                # result = [device_id, datadict]
                return receive_data
            except Exception as e:
                print(f'An error occurred while executing the read register command:{e}')
                # self._reconnect()
                return None

        elif function_code in (5, 6, 15, 16):
            # 写寄存器
            output_value = command['output_value']
            try:
                self._master.set_timeout(10.0)
                self._master.set_verbose(True)
                data = self._master.execute(device_id, function_code, start_addr, output_value=output_value)
                # print("data = ", data)
                # data = (0, 65280) or (0, 0)

                # result = False
                # if function_code == 5 and "res" in command.keys():
                #     res = command["res"]
                #     if start_addr == data[0] and res == data[1]:
                #         result = True
                return data
            except Exception as e:
                print(f'An error occurred while executing the write register command:{e}')
        else:
            print(f'Unsupported function_code.')


def get_time_range(days):
    """获取从几天前的时间点"""
    times = datetime.now() + timedelta(days=-days)
    return times.strftime('%Y-%m-%d %H:%M:%S')


def get_ais_track(data):
    """获取船只历史轨迹"""
    lon_lat = []
    for his_data in data:
        # 格式化
        temp = [round(his_data["lon"], 5), round(his_data["lat"], 5)]
        # 字典转列表
        lon_lat.append(temp)
    # 去重
    result = []
    for l1 in lon_lat:
        if l1 not in result:
            result.append(l1)
    return result


def cnum2chinese(cnum):
    dic = {
        "c1": "压力(kpa)",
        "c3": "潮位压力(kpa)",
        "c4": "潮位(m)",
        "c5": "有效波高(m)",
        "c6": "最大波高(m)",
        "c7": "平均周期(s)",
        "c8": "峰值波周期(s)",
        "c9": "能量周期(s)",
        "c10": "平均跨零周期(s)",
        "c11": "坡陡",
        "c12": "不规则度",
        "c13": "截断频率(HZ)",
        "c14": "逆变器电压(V)",
        "c15": "逆变器电流(A)",
        "c16": "逆变器有功功率(W)",
        "c17": "蓄电池剩余电量(%)",
        "c18": "蓄电池电压(V)",
        "c19": "蓄电池电流(A)",
        "c20": "太阳能电压(V)",
        "c21": "太阳能电流(A)",
        "c22": "雷达液位计(cm)",
        "c24": "温度(℃)",
        "c25": "盐度(psu)",
        "c28": "深度(m)",
        "c23": "溶解氧(mg/L)",
        "c27": "叶绿素(μg/L)",
        "c29": "浊度(NTU)",
        "c26": "PH值",
    }
    return dic[cnum]
