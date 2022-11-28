# Fastapi接口 - 小管岛海洋牧场

## 程序打包exe过程
1. 终端执行第一次打包命令：pyinstaller -F -p 当前项目目录\venv\Lib\site-packages main.py
2. 修改生成的“main.spec”文件中“hiddenimports”内容：hiddenimports=["uvicorn.loops","uvicorn.loops.auto","uvicorn.protocols.http.auto","uvicorn.lifespan","uvicorn.lifespan.on","tortoise.backends.mysql"],
3. 对“main.spec”文件执行打包命令生成新的exe文件：pyinstaller .\huiyi_api.spec

## 程序打包exe后的注意事项
1. 生成的“main.exe”文件如果运行必须携带项目中的“static”目录


## 更新日志
1. 第一次提交。时间：2021/07/19 15:23:21