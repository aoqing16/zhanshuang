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
                log.debug(f'更新页面检测结果：{共享变量.latest_result}')

            time.sleep(0.1)  # 适当休息，避免识别线程跑得太快把CPU吃满
def 截图子线程():
    监听按键截图()
线程初始化=0
章节进入=False
页面匹配_异常页面计数器=0
def 页面匹配():
    global 线程初始化,章节进入,页面匹配_异常页面计数器
    战斗标识符=战斗场景检测()
    if 战斗标识符:
        共享变量.停止寻敌信号=False
        if 线程初始化==0:
            t = threading.Thread(target=寻敌子线程, daemon=True)
            t.start()
            线程初始化+=1
        处于副本内()

        log.info('已退出副本内状态')
    log.info(f'最新页面检测结果：{共享变量.latest_result}')

    if 共享变量.latest_result == '副本首页':
        副本首页()
        ui变化检测('副本首页')
        页面匹配_异常页面计数器 = 0

    elif 共享变量.latest_result=='副本-战斗副本弹窗':
        战斗副本详情页()
        ui变化检测('副本-战斗副本弹窗')
        页面匹配_异常页面计数器 = 0

    elif 共享变量.latest_result=='上阵英雄':
        上阵英雄()
        ui变化检测('上阵英雄')
        页面匹配_异常页面计数器 = 0

    elif 共享变量.latest_result=='编入队伍':
        编入队伍()
        ui变化检测('编入队伍')
        页面匹配_异常页面计数器 = 0

    elif 共享变量.latest_result == '副本-剧情对话页':
        副本对话页()
        ui变化检测('副本-剧情对话页')
        页面匹配_异常页面计数器 = 0

    elif 共享变量.latest_result == '副本-意识重启':
        副本_意识重启()
        ui变化检测('副本-意识重启')
        页面匹配_异常页面计数器 = 0

    elif 共享变量.latest_result=='剧情跳过提示':
        剧情跳过提示()
        ui变化检测('剧情跳过提示')
        页面匹配_异常页面计数器 = 0

    elif 共享变量.latest_result=='副本-战斗结算':
        战后结算()
        ui变化检测('副本-战斗结算')
        页面匹配_异常页面计数器 = 0

    elif 共享变量.latest_result=='副本-剧情副本弹窗':
        副本_剧情副本弹窗()
        ui变化检测('副本-剧情副本弹窗')
        页面匹配_异常页面计数器 = 0

    elif 共享变量.latest_result=='章节首页':
        章节首页()
        ui变化检测('章节首页')
        页面匹配_异常页面计数器 = 0

    elif 共享变量.latest_result == '副本-战斗对话页':
        副本战斗对话页()
        ui变化检测('副本-战斗对话页')
        页面匹配_异常页面计数器 = 0
    elif 共享变量.latest_result == '主页':
        主页()
        ui变化检测('主页')
        页面匹配_异常页面计数器 = 0

    elif 共享变量.latest_result == "other":
        log.info('正常负样本，进入等待')
        页面匹配_异常页面计数器=0
        time.sleep(0.1)
    else:
        if 页面匹配_异常页面计数器==60:
            log.warning('异常页面计数器达到60，执行异常处理')
            异常捕获截图()
            异常时操作()
            页面匹配_异常页面计数器=0
        log.info('异常页面，计数器加一')
        页面匹配_异常页面计数器+=1
        time.sleep(0.1) 

##################################################

if __name__ == '__main__':
    try:
        t = threading.Thread(target=yolo页面检测子线程, daemon=True)
        t.start()
        if hasattr(sys, '_MEIPASS'):
            pass
        else:
            t = threading.Thread(target=截图子线程, daemon=True)
            t.start()

        while True:
            页面匹配()
    except KeyboardInterrupt:
        log.info('脚本主动结束')
    except Exception as e:
        log.error("\n❌ 脚本崩溃！报错信息已自动记录至本地 [崩溃日志.txt]")

        # 自动把报错塞进本地文件，哪怕窗口关了，账本还在！
        with open("崩溃日志-中央调度器py.txt", "a", encoding="utf-8") as f:
            import datetime

            f.write(f"\n\n⏰ 崩溃时间: {datetime.datetime.now()}\n")
            traceback.print_exc(file=f)  # 把报错堆栈写进文件

        traceback.print_exc()
        input("\n👉 按回车键退出程序...")
