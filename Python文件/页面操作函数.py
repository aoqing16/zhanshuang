from 函数资源 import *
import time

def 副本首页():
    count=0
    if 共享变量.超时信号:
        图像随机位置点击(路径向导('ziyuanwenjian/UI/img_10.png'))
        print('副本超时退出，正在退出副本首页')
        return
    while True:
        img = 截图()
        n = yolo检测(img)
        m = 获取最右侧未通关关卡调试版(img,n)
        print(f'未通过关卡中心坐标{m}')
        if count<=2:
            if m == 0:
                d.swipe_ext("left", scale=0.4)
                time.sleep(1)
                count += 1
            else:
                clink = 坐标随机(m, left=30, right=30, up=30, down=30)
                print(f'副本首页点击坐标{clink}')
                start_time=time.time()
                adb_click(clink)
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
                图像随机位置点击(路径向导('ziyuanwenjian/UI/img_10.png'))
                print('正在退出副本首页')
                break

def 副本详情页():
    zuobiao = 图像坐标获取(路径向导('ziyuanwenjian/UI/img_1.png'))
    if zuobiao:
        print(zuobiao)
        suijizuobiao = 坐标随机(zuobiao, left=96, right=40, up=20, down=20)
        print(suijizuobiao)
        adb_click(suijizuobiao)
    else:
        print('已开启速通模式')
    # 执行鼠标点击（准备战斗）
    zhandoukaishi_zuobiao = (2246, 1310)
    clink = 坐标随机(zhandoukaishi_zuobiao, left=200, right=200, up=40, down=40)
    adb_click(clink)
def 战斗副本详情页():
    速通模式按键=图像是否存在(路径向导('ziyuanwenjian/biaoshi/img.png'))
    速通_关=图像是否存在(路径向导('ziyuanwenjian/UI/img_1.png'))
    print(f'速通按键是否存在：【{速通模式按键}】')
    if 速通模式按键:
        if 速通_关:
            图像随机位置点击(路径向导('ziyuanwenjian/UI/img_1.png'))
        else:
            print('当前已是速通模式')
    zhandoukaishi_zuobiao = (2246, 1310)
    clink = 坐标随机(zhandoukaishi_zuobiao, left=200, right=200, up=40, down=40)
    adb_click(clink)
def 章节首页():
    章节标签位置初始化()
    章节位置初始化()
    print(f'重载前章节黑名单：{config.章节黑名单}')
    importlib.reload(config)
    print(f'重载后章节黑名单：{config.章节黑名单}')
    未通关章节定位()
    共享变量.章节名截图=区域截图(650,1037,951,1108)
    共享变量.超时信号=False
    坐标=(1710,707)
    坐标=坐标随机(坐标,left=500,right=500,up=300,down=300)
    adb_click(坐标)
def 上阵英雄():
    zuobiao = 图像坐标获取(路径向导('ziyuanwenjian/UI/img_2.png'))
    if zuobiao:  # 图像存在说明当前没有上阵英雄
        图像随机位置点击(路径向导('ziyuanwenjian/UI/img_2.png'))
    else:
        图像随机位置点击(路径向导('ziyuanwenjian/UI/img_3.png'))
def 编入队伍():
    图像随机位置点击(路径向导('ziyuanwenjian/UI/img_9.png'))
def 副本对话页():
    zuobiao = 图像坐标获取灰度模式(路径向导('ziyuanwenjian/UI/img_4.png'))
    print(f'副本对话页标识坐标{zuobiao}')
    n = 坐标随机(zuobiao, left=-375, right=615, up=25, down=25)
    adb_click(n)
def 剧情跳过提示():
    图像随机位置点击(路径向导('ziyuanwenjian/UI/img_5.png'))
def 战后结算():
    图像随机位置点击(路径向导('ziyuanwenjian/UI/img_6.png'))
def 播放剧情():
    图像随机位置点击(路径向导('ziyuanwenjian/UI/img_7.png'))
def 副本战斗对话页():
    区域内随机坐标点击(1567,1721,1200,1247)
    time.sleep(0.1)
    区域内随机坐标点击(2206,2312,1071,1183)
if __name__ == '__main__':
    # while True:
    副本首页()
