from fastapi import APIRouter
from fastapi.responses import FileResponse

from core import Enums
import pandas as pd
from schemas import historyData
from tortoise import Tortoise

router = APIRouter()


@router.post("/historyData", summary="获取历史数据")
async def history_data(item: historyData.GetHistoryData):
    """
    请求参数说明：
    - "pageName"：页面名（类型：str）【参数："SZ"(水质)、"SW"(水文)、"TYN"(太阳能)】
    - "startDate"：开始日期（类型：str）【参数格式："YYYY-MM-DD"】
    - "endDate"：结束日期（类型：str）【参数格式："YYYY-MM-DD"】
    - "excel"：是否下载excel（类型：int）【参数：0（不下载只要数据）、1（要下载）】
    """
    db = Tortoise.get_connection("default")
    page_name = item.pageName
    start_date = item.startDate
    end_date = item.endDate
    excel_flag = item.excel
    table_name = "xiaoguandao_shucai_tbl"
    # --------------------------------------------------查数据--------------------------------------------------
    if page_name == "SZ":
        param_names = Enums.sz_param_name_list
    elif page_name == "SW":
        param_names = Enums.sw_param_name_list
    elif page_name == "TYN":
        param_names = Enums.tyn_param_name_list
    else:
        return {"msg": "page_name error"}

    select_params = [f"ROUND({name},2)  {name}" for name in param_names]
    if start_date == end_date:
        sql = f"SELECT id,times,{','.join(select_params)} FROM `{table_name}` " \
              f"WHERE date_format(times,'%Y-%m-%d')='{start_date}' ORDER BY times DESC;"
    else:
        sql = f"SELECT id,times,{','.join(select_params)} FROM `{table_name}` " \
              f"WHERE times >= '{start_date} 00:00:00' AND times <= '{end_date} 23:59:59' ORDER BY times DESC;"
    result = await db.execute_query_dict(sql)
    for data in result:
        data['times'] = str(data['times'])
    # --------------------------------------------------返回excel--------------------------------------------------
    if excel_flag:
        df = pd.DataFrame(result)
        df.rename(columns=Enums.cnum2chinese, inplace=True)
        # print(df)
        # 生成excel文件
        df.to_excel('./static/excel.xlsx', sheet_name='Sheet1', index=False)  # index false为不写入索引
        headers = {'Content-Disposition': 'attachment; filename="excel.xlsx"'}
        return FileResponse('./static/excel.xlsx', headers=headers)
    else:
        return result
