from 函数资源 import *
import time

章节进入 = False
def 副本首页():
    count=0
    if 共享变量.超时信号:
        图像随机位置点击(路径向导('ziyuanwenjian/UI/img_10.png'))
        print('副本超时退出，正在退出副本首页')
        return
    while True:
        img = 缩放图片至基准尺寸(截图())
        n = yolo检测(img)
        m = 获取最右侧未通关关卡反向排除版(img, n)
        print(f'未通过关卡中心坐标{m}')
        if count<=2:
            if m == 0:
                d.swipe_ext("left", scale=0.4)
                time.sleep(1)
                count += 1
            else:
                clink = 坐标随机(m, left=x相对坐标(30), right=x相对坐标(30), up=y相对坐标(30), down=y相对坐标(30))
                print(f'副本首页点击坐标{clink}')
                adb_click(clink)
                start_time = time.time()
                while time.time() - start_time < 3:
                    if 共享变量.latest_result== '副本-战斗副本弹窗'or 共享变量.latest_result=='副本-剧情副本弹窗':
                        break
                    else:
                        print('副本页点击无效，正在尝试滑动')
                        d.swipe_ext("left", scale=0.4)
                        time.sleep(1)
                print(f'adb点击耗时为：{time.time() - start_time}')
                break
        else:#滑动三次后仍未发现新关卡，执行退出副本首页
            if 图像是否存在从配置文件中获取文件路径('普通剧情'):
                图像随机位置点击配置文件('普通剧情按钮')
                time.sleep(0.5)
                图像随机位置点击配置文件('隐藏剧情按钮')
                count=0
                time.sleep(0.5)
            else:
                if 章节进入:
                    黑名单更新(共享变量.章节名截图)
                图像随机位置点击(路径向导('ziyuanwenjian/UI/img_10.png'))
                print('正在退出副本首页')
                break
#
# def 副本详情页():
#     zuobiao = 图像坐标获取(路径向导('ziyuanwenjian/UI/img_1.png'))
#     if zuobiao:
#         print(zuobiao)
#         suijizuobiao = 坐标随机(zuobiao, left=x相对坐标(96), right=x相对坐标(40), up=y相对坐标(20), down=y相对坐标(20))
#         print(suijizuobiao)
#         adb_click(suijizuobiao)
#     else:
#         print('已开启速通模式')
#     # 执行鼠标点击（准备战斗）
#     # 分流
#     if 图像是否存在从配置文件中获取文件路径('副本-战斗副本弹窗后期副本'):
#         print('检测到副本为后期副本')
#         区域内随机坐标点击(x相对坐标(2018),2325,1105,1172)
#     if 图像是否存在从配置文件中获取文件路径('副本-战斗副本弹窗前期副本'):
#         print('检测到副本为前期副本')
#         区域内随机坐标点击(2021,2356,1274,1331)
def 战斗副本详情页():
    速通模式按键=图像是否存在(路径向导('ziyuanwenjian/biaoshi/img.png'))
    速通_关=图像是否存在(路径向导('ziyuanwenjian/UI/img_1.png'))
    print(f'速通按键是否存在：【{速通模式按键}】')
    if 速通模式按键:
        if 速通_关:
            图像随机位置点击(路径向导('ziyuanwenjian/UI/img_1.png'))
        else:
            print('当前已是速通模式')
    if 图像是否存在从配置文件中获取文件路径('副本-战斗副本弹窗后期副本'):
        print('检测到副本为后期副本')
        区域内随机坐标点击(x相对坐标(2018), x相对坐标(2325), y相对坐标(1105), y相对坐标(1172))
    if 图像是否存在从配置文件中获取文件路径('副本-战斗副本弹窗前期副本'):
        print('检测到副本为前期副本')
        区域内随机坐标点击(x相对坐标(2021), x相对坐标(2356), y相对坐标(1274), y相对坐标(1331))
def 章节首页():
    global 章节进入
    章节标签位置初始化()
    章节位置初始化()
    print(f'重载前章节黑名单：{config.章节黑名单}')
    importlib.reload(config)
    print(f'重载后章节黑名单：{config.章节黑名单}')
    未通关章节定位()
    共享变量.章节名截图=区域截图(x相对坐标(650),y相对坐标(1037),x相对坐标(951),y相对坐标(1108))
    共享变量.超时信号=False
    坐标=(x相对坐标(1710),y相对坐标(707))
    坐标=坐标随机(坐标,left=x相对坐标(500),right=x相对坐标(500),up=y相对坐标(300),down=y相对坐标(300))
    adb_click(坐标)
    章节进入=True
def 上阵英雄():
    zuobiao = 图像是否存在从配置文件中获取文件路径('上阵英雄')
    if zuobiao:  # 图像存在说明当前没有上阵英雄
        图像随机位置点击(路径向导('ziyuanwenjian/UI/img_2.png'))
    else:
        图像随机位置点击(路径向导('ziyuanwenjian/UI/img_3.png'))
def 编入队伍():
    图像随机位置点击(路径向导('ziyuanwenjian/UI/img_9.png'))
def 副本对话页():
    # zuobiao = 图像坐标获取灰度模式(路径向导('ziyuanwenjian/UI/img_4.png'))
    # print(f'副本对话页标识坐标{zuobiao}')
    # time.sleep(0.7)
    # n = 坐标随机(zuobiao, left=-x相对坐标(375), right=x相对坐标(615), up=y相对坐标(25), down=y相对坐标(25))
    # adb_click(n)
    time.sleep(1.3)
    区域内随机坐标点击(x相对坐标(2237),x相对坐标(2480),y相对坐标(54),y相对坐标(112))
    time.sleep(0.1)
def 剧情跳过提示():
    time.sleep(0.7)
    图像随机位置点击(路径向导('ziyuanwenjian/UI/img_5.png'))
def 战后结算():
    if 图像是否存在从配置文件中获取文件路径('战后结算'):
        图像随机位置点击(路径向导('ziyuanwenjian/UI/img_6.png'))
    else:
        区域内随机坐标点击(x相对坐标(1677),x相对坐标(2145),y相对坐标(1180),y相对坐标(1316))

def 播放剧情():
    图像随机位置点击配置文件('副本-剧情副本弹窗')
def 副本战斗对话页():
    区域内随机坐标点击(x相对坐标(1567),x相对坐标(1721),y相对坐标(1200),y相对坐标(1247))
    time.sleep(0.1)
    区域内随机坐标点击(x相对坐标(2206),x相对坐标(2312),y相对坐标(1071),y相对坐标(1183))
def 副本_意识重启():
    图像随机位置点击配置文件('副本-意识重启')
    time.sleep(3)
    for _ in range(3):  # 等待作战失败文字出现
        if 图像是否存在从配置文件中获取文件路径('作战失败'):
            break
        else:
            time.sleep(1)
    for i in range(1, 4):  # 循环点击，直至作战失败消失
        print(f'作战失败标识符检测：第{i}次')
        if 图像是否存在从配置文件中获取文件路径('作战失败'):
            print(f'检测到作战失败标识符，正在执行点击')
            区域内随机坐标点击(x相对坐标(607), x相对坐标(1955), y相对坐标(494), y相对坐标(1220))
            time.sleep(0.8)
        else:
            break
        time.sleep(1)
    print('副本内死亡，正在更新黑名单')
    黑名单更新(共享变量.章节名截图)
if __name__ == '__main__':
    上阵英雄()