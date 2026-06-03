from 页面操作函数 import *
# 定义映射表：名称 -> 文件名
import 共享变量
# 定义一个锁，防止主线程读取时，后台线程正在写入，造成数据错乱
data_lock = threading.Lock()
def 页面识别灰度模式子线程():

    while True:
        # 这里模拟你的识别过程
        # 注意：这里如果太快会占满CPU，建议加个微小的 sleep
        # start_time=time.time()

        result = 页面识别灰度模式()
        # print(f'子线程获取的数据: {result}')
        # 锁定，更新数据
        # print(f'子线程更新数据耗时{time.time() - start_time}')
        with data_lock:
            共享变量.latest_result = result

        time.sleep(0.05)  # 适当休息，避免识别线程跑得太快把CPU吃满
def 页面匹配():
    战斗标识符=战斗场景检测()
    if 战斗标识符:
        战斗主函数()
        ui变化检测(['战斗加载页'])
    # page_name=页面识别灰度模式()
    print(共享变量.latest_result)

    if 共享变量.latest_result == ['副本首页']:
        副本首页()
        ui变化检测(['副本首页'])
    elif 共享变量.latest_result== ['战斗副本详情页', '副本首页']:
        战斗副本详情页()
        ui变化检测(['战斗副本详情页', '副本首页'])
    elif 共享变量.latest_result==['上阵英雄']:
        上阵英雄()
        ui变化检测(['上阵英雄'])
    elif 共享变量.latest_result==['编入队伍']:
        编入队伍()
        ui变化检测(['编入队伍'])
    elif '副本对话页'in 共享变量.latest_result:#page_name==['副本对话页']:
        副本对话页()
        ui变化检测(['副本对话页'])
    elif 共享变量.latest_result==['剧情跳过提示']:
        剧情跳过提示()
        ui变化检测(['剧情跳过提示'])
    elif 共享变量.latest_result==['战后结算']:
        战后结算()
        ui变化检测(['战后结算'])
    elif 共享变量.latest_result== ['副本首页', '播放剧情']:
        播放剧情()
        ui变化检测(['副本首页', '播放剧情'])
    elif 共享变量.latest_result==['章节首页']:
        章节首页()
        ui变化检测(['章节首页'])

##################################################

if __name__ == '__main__':
    t = threading.Thread(target=页面识别灰度模式子线程, daemon=True)
    t.start()
    time.sleep(1.5)
    while True:
        页面匹配()