import threading
from adb截图 import 监听按键截图
from 页面操作函数 import *
import 共享变量
# 定义一个锁，防止主线程读取时，后台线程正在写入，造成数据错乱

data_lock = threading.Lock()
def yolo页面检测子线程():
    # try:
        while True:
            result = yolo页面检测主函数()
            with data_lock:
                共享变量.latest_result = result
                # print(f'更新页面检测结果：{共享变量.latest_result}')

            time.sleep(0.1)  # 适当休息，避免识别线程跑得太快把CPU吃满
    # except KeyboardInterrupt:
    #     print('关闭子线程')
def 截图子线程():
    监听按键截图()
线程初始化=0
章节进入=False
def 页面匹配():
    global 线程初始化,章节进入
    战斗标识符=战斗场景检测()
    if 战斗标识符:
        共享变量.停止寻敌信号=False
        if 线程初始化==0:
            t = threading.Thread(target=寻敌子线程, daemon=True)
            t.start()
            线程初始化+=1
        战斗主函数()
        ui变化检测(['战斗加载页'])
        print('战斗函数已退出')
    # page_name=页面识别灰度模式()
    print(共享变量.latest_result)

    if 共享变量.latest_result == '副本首页':
        副本首页()
        ui变化检测('副本首页')
    elif 共享变量.latest_result=='副本-战斗副本弹窗':
        战斗副本详情页()
        ui变化检测('副本-战斗副本弹窗')
    elif 共享变量.latest_result=='上阵英雄':
        上阵英雄()
        ui变化检测('上阵英雄')
    elif 共享变量.latest_result=='编入队伍':
        编入队伍()
        ui变化检测('编入队伍')
    elif 共享变量.latest_result == '副本-剧情对话页':
        副本对话页()
        ui变化检测('副本-剧情对话页')
    elif 共享变量.latest_result == '副本-意识重启':
        副本_意识重启()
        ui变化检测('副本-意识重启')
    elif 共享变量.latest_result=='剧情跳过提示':
        剧情跳过提示()
        ui变化检测('剧情跳过提示')
    elif 共享变量.latest_result=='副本-战斗结算':
        战后结算()
        ui变化检测('副本-战斗结算')
    elif 共享变量.latest_result=='副本-剧情副本弹窗':
        副本_剧情副本弹窗()
        ui变化检测('副本-剧情副本弹窗')
    elif 共享变量.latest_result=='章节首页':
        章节首页()
        ui变化检测('章节首页')
    elif 共享变量.latest_result == '副本-战斗对话页':
        副本战斗对话页()
        ui变化检测('副本-战斗对话页')
    else:
        print('没有触发任何动作，进入0.1秒等待')
        time.sleep(0.1) 

##################################################

if __name__ == '__main__':
    try:
        t = threading.Thread(target=yolo页面检测子线程, daemon=True)
        t.start()
        t = threading.Thread(target=截图子线程, daemon=True)
        t.start()
        # time.sleep(1000)
        while True:
            页面匹配()
    except KeyboardInterrupt:
        print('脚本主动结束')
    except Exception as e:
        print(f'脚本出错了,错误信息:【{e}】')
