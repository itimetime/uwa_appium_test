import os
import platform

from tools.logger import logger

def run_appium_server():
    try:
        kill_appium_server()
        logger.info("命令行启动appium")
        print("""[Appium] Welcome to Appium v1.17.1
[Appium] Non-default server args:
[Appium]   loglevel: error:debug
[Appium] Appium REST http interface listener started on 0.0.0.0:4723""")
        os.system("appium --log-level error:debug")
    except Exception as e:
        print(f"appium命令行启动失败，如已手动启动请忽略此消息{e}")



#获取系统的名称，使用对应的指令
def get_system():
    system=platform.system()
    if system=='Windows':
        find_manage='findstr'
    else:
        find_manage='grep'
    return  [system,find_manage]

def kill_appium_server(port=4723):
    # 查找对应端口的pid

        cmd = 'netstat -aon | findstr ' + str("0.0.0.0:4723")
        result = os.popen(cmd).read()
        print(result)
        if str(result) != "":
            pid = str(result)[-6:]
            # 执行被占用端口的pid
            cmd_kill = 'taskkill -f -pid ' + str(pid)
            # logger.info(cmd_kill)
            os.popen(cmd_kill)
            print("apppium-server killed")
        else:
            print("The appium-server port is not occupied and is available")


if __name__ == '__main__':
    # run_appium_server()
    kill_appium_server()
