import threading
import random
import time
from ultralytics import YOLO
import numpy as np
import uiautomator2 as u2
import cv2
import os
import sys
import 共享变量
import config
import importlib
print('模型加载中')
model = YOLO(r'C:\Users\ZhuanZ1\runs\detect\train-8\weights\best.pt')#目标检测模型
model_1 = YOLO(r"C:\Users\ZhuanZ1\runs\classify\train-9\weights\best.pt")#分类模型
# from Python文件.中央调度器 import 页面识别

# 1. 连接设备
d = u2.connect('127.0.0.1:16384')
# 💡 直接改对象的属性，底层会自动映射到 settings['post_delay']
def 截图():
    img = d.screenshot(format='opencv')
    return img


def 区域截图(x1=None, y1=None, x2=None, y2=None):
    """
    指定区域截图
    :param x1: 左上角横坐标
    :param y1: 左上角纵坐标
    :param x2: 右下角横坐标
    :param y2: 右下角纵坐标
    :return: OpenCV 格式的图片矩阵（BGR）
    """
    # 1. 依然先获取全屏的 OpenCV 图像
    img = d.screenshot(format='opencv')

    # 2. 只有当四个坐标都传了的时候，才进行区域裁剪
    if x1 is not None and y1 is not None and x2 is not None and y2 is not None:
        # ⚠️ 核心：把 X 和 Y 调换位置，因为 NumPy 切片是 [y轴范围, x轴范围]
        # 同时强转成 int，防止浮点数导致切片失败
        img = img[int(y1):int(y2), int(x1):int(x2)]

    return img

def 图像是否存在(img_name, threshold=0.8, gray_mode=False):
    """
    检测图像是否存在
    :param img_name: 模板相对路径
    :param threshold: 匹配阈值
    :param gray_mode: 是否开启灰度匹配模式
    :return: 存在返回 True, 不存在返回 False
    """
    # 拼接图片路径
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # TEMPLATE_PATH = os.path.join(BASE_DIR, img_name)
    TEMPLATE_PATH=路径向导(img_name)
    # 1. 读取模板
    # 如果开启灰度，直接读灰度；否则读彩色
    flag = cv2.IMREAD_GRAYSCALE if gray_mode else cv2.IMREAD_COLOR
    template = cv2.imread(TEMPLATE_PATH, flag)

    if template is None:
        print(f"错误：无法读取模板图片 {TEMPLATE_PATH}")
        return False

    # 1.1 获取并处理屏幕截图
    img_color = 截图()
    if gray_mode:
        img_source = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    else:
        img_source = img_color

    # 2. 执行模板匹配
    res = cv2.matchTemplate(img_source, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    # 3. 返回匹配结果
    # print(f"DEBUG: {img_name} 匹配度: {max_val:.4f}") # 调试用
    return max_val >= threshold


def 图像是否存在从配置文件中获取文件路径(key, threshold=0.8, gray_mode=False):
    """
    检测图像是否存在
    :param key: 模板在配置文件中图片标识符清单字典中的键名
    :param threshold: 匹配阈值
    :param gray_mode: 是否开启灰度匹配模式
    :return: 存在返回 True, 不存在返回 False
    """
    TEMPLATE_PATH = config.图片标识符清单.get(key)
    # 1. 读取模板
    # 如果开启灰度，直接读灰度；否则读彩色
    flag = cv2.IMREAD_GRAYSCALE if gray_mode else cv2.IMREAD_COLOR
    template = cv2.imread(TEMPLATE_PATH, flag)

    if template is None:
        print(f"错误：无法读取模板图片 {TEMPLATE_PATH}")
        return False

    # 1.1 获取并处理屏幕截图
    img_color = 截图()
    if gray_mode:
        img_source = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    else:
        img_source = img_color

    # 2. 执行模板匹配
    res = cv2.matchTemplate(img_source, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    # 3. 返回匹配结果
    # print(f"DEBUG: {img_name} 匹配度: {max_val:.4f}") # 调试用
    return max_val >= threshold
def 图像坐标获取灰度模式(img_name, threshold=0.7):
    # 拼接图片路径
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # TEMPLATE_PATH = os.path.join(BASE_DIR, f"{img_name}")
    TEMPLATE_PATH=路径向导(img_name)
    # 1. 读取模板图（以灰度模式读取）
    template_gray = cv2.imread(TEMPLATE_PATH, cv2.IMREAD_GRAYSCALE)
    if template_gray is None:
        print(f"错误：无法读取模板图片 {TEMPLATE_PATH}")
        return None

    # 1.1 截取屏幕并转换为灰度图
    img_color = 截图()
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    # 2. 获取模板尺寸
    h, w = template_gray.shape[:2]

    # 3. 执行模板匹配（使用灰度图）
    res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)

    # 4. 获取匹配度最高的坐标
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    # 5. 判断是否达到阈值
    print(max_val)
    if max_val >= threshold:
        # max_loc 是左上角坐标，计算中心点
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2

        return (center_x, center_y)

    return None
def 图像坐标获取(img_name, threshold=0.8):
    # 拼接图片路径
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # TEMPLATE_PATH = os.path.join(BASE_DIR, f"{img_name}")
    TEMPLATE_PATH=路径向导(img_name)
    # 1. 读取模板图
    template = cv2.imread(TEMPLATE_PATH, cv2.IMREAD_COLOR)
    if template is None:
        print(f"错误：无法读取模板图片 {TEMPLATE_PATH}")
        return None
    # 1.1截取屏幕

    img = 截图()

    # 2. 获取模板尺寸
    h, w = template.shape[:2]

    # 3. 执行模板匹配
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    # 4. 获取匹配度最高的坐标
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # 5. 判断是否达到阈值
    if max_val >= threshold:
        # max_loc 是左上角坐标，计算中心点
        center_x = max_loc[0] + w // 2
        center_y = max_loc[1] + h // 2

        # 调试：可以将匹配区域画出来看看（可选）
        # cv2.rectangle(screenshot, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)

        return (center_x, center_y)

    return None

def 图像随机位置点击(img_name, threshold=0.8, padding=0):
    """
    匹配模板并在匹配区域内返回一个随机坐标
    :param img_name: 模板图片相对路径ziyuanwenjian/biaoshi/img_24.png
    :param threshold: 匹配阈值
    :param padding: 内缩量，防止点到边缘（默认5像素）
    :return: (rand_x, rand_y) 或 None
    """
    # 拼接路径
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # TEMPLATE_PATH = os.path.join(BASE_DIR, img_name)
    TEMPLATE_PATH=路径向导(img_name)
    template = cv2.imread(TEMPLATE_PATH, cv2.IMREAD_COLOR)
    if template is None:
        print(f"错误：无法读取模板图片 {TEMPLATE_PATH}")
        return None
    img = d.screenshot(format='opencv')

    h, w = template.shape[:2]
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        # 获取匹配区域的左上角 (x, y)
        x1, y1 = max_loc

        # 计算随机范围，加入 padding 保护，确保点在按钮内侧
        # 确保 width 和 height 大于 2*padding，否则范围无效
        x_min = x1 + padding
        x_max = x1 + w - padding
        y_min = y1 + padding
        y_max = y1 + h - padding

        # 随机生成坐标
        rand_x = random.randint(x_min, x_max)
        rand_y = random.randint(y_min, y_max)
        d.click(rand_x,rand_y)

    return None


def 图像随机位置点击配置文件(key, threshold=0.8, padding=0):
    """
    匹配模板并在匹配区域内返回一个随机坐标
    :param img_name: 模板图片相对路径ziyuanwenjian/biaoshi/img_24.png
    :param threshold: 匹配阈值
    :param padding: 内缩量，防止点到边缘（默认5像素）
    :return: (rand_x, rand_y) 或 None
    """
    # 拼接路径
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # TEMPLATE_PATH = os.path.join(BASE_DIR, img_name)
    TEMPLATE_PATH = config.图片标识符清单.get(key)
    template = cv2.imread(TEMPLATE_PATH, cv2.IMREAD_COLOR)
    if template is None:
        print(f"错误：无法读取模板图片 {TEMPLATE_PATH}")
        return None
    img = d.screenshot(format='opencv')

    h, w = template.shape[:2]
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        # 获取匹配区域的左上角 (x, y)
        x1, y1 = max_loc

        # 计算随机范围，加入 padding 保护，确保点在按钮内侧
        # 确保 width 和 height 大于 2*padding，否则范围无效
        x_min = x1 + padding
        x_max = x1 + w - padding
        y_min = y1 + padding
        y_max = y1 + h - padding

        # 随机生成坐标
        rand_x = random.randint(x_min, x_max)
        rand_y = random.randint(y_min, y_max)
        d.click(rand_x, rand_y)

    return None


def 坐标随机(target_coord, left=200, right=200, up=150, down=0):
    if target_coord:
        target_x, target_y = target_coord

        # 在 [target - 负向范围, target + 正向范围] 之间生成
        rand_x = random.randint(target_x - left, target_x + right)
        rand_y = random.randint(target_y - up, target_y + down)

        return (rand_x, rand_y)
    else:
        return None


def adb_click(coord):
    if coord:
        x, y = coord
        d.shell(f"input tap {x} {y}")
    else:
        return

def 区域内随机坐标点击(x1, x2, y1, y2):
    '''
    在指定的矩形区域 (x1, y1) 到 (x2, y2) 内生成随机坐标并执行 ADB 点击
    :param x1: 区域左侧 X 坐标
    :param x2: 区域右侧 X 坐标
    :param y1: 区域顶部 Y 坐标
    :param y2: 区域底部 Y 坐标
    '''
    # 💡 健壮性处理：防止误传参数（比如把左和右写反了导致报错）
    min_x, max_x = min(x1, x2), max(x1, x2)
    min_y, max_y = min(y1, y2), max(y1, y2)

    # 在区间内随机生成一个整数坐标
    random_x = random.randint(min_x, max_x)
    random_y = random.randint(min_y, max_y)

    目标坐标 = (random_x, random_y)
    print(f"🎯 [区域防检测点击] 规划区域:({x1},{y1})->({x2},{y2})，实际随机落点: {目标坐标}")

    # 执行你原有的 adb 点击函数
    adb_click(目标坐标)

    # 顺手带个极其微小的随机等待（0.05~0.15秒），让点击频率也随机化，反作弊效果更佳
    time.sleep(random.uniform(0.05, 0.15))

TEMPLATE_MAP = {
    "战斗副本详情页": "img_13.png",
    "副本首页": "img_1.png",
    '上阵英雄': 'img_2.png',
    '编入队伍': 'img_8.png',
    '副本对话页': 'img_3.png',
    '剧情跳过提示': 'img_4.png',
    '战后结算': 'img_5.png',
    '播放剧情': 'img_6.png',
    # '战斗场景': 'img_9.png',
    '章节首页': 'img_17.png',
    # '战斗场景': 'img_10.png',


}

# 模板存放的基础路径
TEMPLATE_DIR = r"C:\Users\ZhuanZ1\Desktop\rpa\zhanshuangfuben\ziyuanwenjian\biaoshi"
def yolo页面识别():
    # 截图
    img = d.screenshot(format='opencv')
    start = time.time()

    # 3. 使用模型分类
    # verbose=False 去掉控制台冗余输出
    results = model_1(img, verbose=False)

    # 分类结果解析
    probs = results[0].probs
    top1_id = probs.top1
    top1_conf = probs.top1conf.item()
    label = results[0].names[top1_id]
    return label,top1_conf


过滤后识别结果 = '0'
count = 0
def yolo过滤器(result_tuple):
    global count, 过滤后识别结果

    # 1. 解包元组，获取标签和置信度
    label, conf = result_tuple

    # 2. 新增：置信度拦截门槛
    if conf < 0.85:
        # 置信度太低，说明结果不可靠，直接重置计数器
        print(f"⚠️ 过滤器拦截：[{label}] 置信度过低 ({conf:.4f} < 0.85)，重置计数")
        过滤后识别结果 = '0'
        count = 0
        return 0

    # 3. 走原有的连续次数判定逻辑
    if label == 过滤后识别结果:
        count += 1
    else:
        过滤后识别结果 = label
        count = 1

    # 4. 判断是否连续满足 2 次
    if count >= 3:
        return 过滤后识别结果
    else:
        return 0
def yolo页面检测主函数():
    ll=yolo页面识别()
    # print(f'yolo模型识别结果：【{ll[0]}】    置信度：{ll[1]}')
    过滤结果=yolo过滤器(ll)
    return 过滤结果

def 页面识别灰度模式(threshold=0.8):
    """
    遍历映射表，检测截图中存在的所有目标（灰度匹配模式）
    :param threshold: 匹配阈值
    :return: 一个列表，包含检测到的所有名称
    """
    detected_names = []
    # 获取彩色截图并转换为灰度图
    img_color = 截图()
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)

    for name, filename in TEMPLATE_MAP.items():
        template_path = os.path.join(TEMPLATE_DIR, filename)

        # 读取模板并直接以灰度模式加载 (cv2.IMREAD_GRAYSCALE)
        template_gray = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

        if template_gray is None:
            print(f"警告: 无法加载模板 {filename}")
            continue

        # 模板匹配 (现在输入都是单通道灰度图)
        res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        # 如果置信度高于阈值，认为存在
        if max_val >= threshold:
            detected_names.append(name)

    return detected_names


import cv2
import numpy as np


def 血条检测(roi=config.血条roi, pixel_threshold=50):
    """
    检测屏幕指定 ROI 区域内符合 HSV 范围的像素数量
    :param img: 传入的当前最新 OpenCV 格式截图 (BGR)
    :param roi: 检查区域 [x1, y1, x2, y2]
    :param pixel_threshold: 触发判定的像素点数门槛（默认 50）
    :return: True (达到阈值) 或 False (未达到)
    """
    img=截图()
    if img is None:
        print("❌ [血条检测] 传入的图片为空！")
        return False

    # 1. 解析坐标
    x1, y1, x2, y2 = roi
    img_h, img_w = img.shape[:2]

    # 💡 健壮性处理：防止越界导致 cv2 裁剪报错
    x1_safe = max(0, min(x1, img_w))
    x2_safe = max(0, min(x2, img_w))
    y1_safe = max(0, min(y1, img_h))
    y2_safe = max(0, min(y2, img_h))

    if x1_safe >= x2_safe or y1_safe >= y2_safe:
        print(f"⚠️ [血条检测] ROI 区域坐标非法: ({x1},{y1})->({x2},{y2})")
        return False

    # 2. 裁剪血条区域 ROI
    roi_img = img[y1_safe:y2_safe, x1_safe:x2_safe]

    # 3. 色彩空间转换 BGR -> HSV
    hsv_roi = cv2.cvtColor(roi_img, cv2.COLOR_BGR2HSV)

    # 4. 定义你给出的高亮白/特定血条颜色范围
    # 💡 注意：numpy 数组中通常使用 np.uint8 确保数据类型正确
    lower_hsv = np.array(config.血条hsv范围lower, dtype=np.uint8)
    upper_hsv = np.array(config.血条hsv范围upper, dtype=np.uint8)

    # 5. 二值化遮罩抠图
    mask = cv2.inRange(hsv_roi, lower_hsv, upper_hsv)

    # 6. 计算亮色像素点数量
    matching_pixels = cv2.countNonZero(mask)

    # 7. 打印详细调试信息，方便你调参
    # print(f"📊 [血条检测调试] 目标区域符合条件的像素数: {matching_pixels} (目标阈值: {pixel_threshold})")

    if matching_pixels > pixel_threshold:
        return True,matching_pixels
    else:
        return False,matching_pixels


# 💡 初始化全局变量，用于记住上一次的血条像素值
_上次的像素值 = None

def 寻敌状态检测(状态参数):
    """
    根据血条的存在状态与像素变化幅度，判定是否需要报警或保持当前状态
    :param 状态参数: 格式为 (是否有血条_bool, 像素数量_int) 的元组或列表
    :return:
        - True: 没有血条或有血条但血条未变动，需执行寻敌。
        - False: 有血条，血条大幅变动中
    """
    global _上次的像素值

    # 1. 解包参数
    是否有血条, 当前像素值 = 状态参数

    # 2. 条件一：如果第一个值就为 False（没血条），立刻返回 True（视为正常转场或寻敌中）
    if not 是否有血条:
        # 💡 注意：没怪的时候，把记忆重置为 None，防止下一波怪刷出来时，跟上一波怪的死前残余像素做对比
        _上次的像素值 = None
        return True

    # 3. 条件二：第一个值为 True，进一步判断第二个数值的变化幅度
    # 💡 健壮性处理：如果是刚看到血条的第一帧，还没有“上一次的数值”可以对比
    if _上次的像素值 is None:
        _上次的像素值 = 当前像素值
        return True  # 第一帧默认视为正常，先存下数据

    # 计算绝对变化幅度（拿当前值和上一次记录的值做减法）
    变化幅度 = abs(当前像素值 - _上次的像素值)

    print(f"📊 [变化率雷达] 当前像素:{当前像素值} | 上次像素:{_上次的像素值} | 差值:{变化幅度}")

    # 💡 核心校验：把当前值覆盖存入记忆，供下一次循环对比
    _上次的像素值 = 当前像素值

    # 4. 根据变化幅度返回结果
    if 变化幅度 > 1000:
        return False  # 变化幅度大，说明血条在剧烈变动（可能是怪在疯狂回血/大掉血/闪烁），返回 False
    else:
        return True  # 变化幅度小于 1000，说明血条稳如老狗（伤害没打上去/空挥），返回 True


# ==========================================
# 💡 独立的防抖工具全局变量
# ==========================================
上一次结果 = None
连续出现次数 = 0
def 连续性检测(检测数据,连续次数):
    """
    通用连续性防抖检测器
    :param 检测数据: 当前帧计算出来的单次状态 (True 或 False)
    :return:
        - 当连续 3 次相同时，返回该结果 (True 或 False)
        - 未满 3 次或发生状态突变时，返回 None 保持观察
    """
    global 上一次结果, 连续出现次数

    # 1. 启动时的第一帧初始化
    if 上一次结果 is None:
        上一次结果 = 检测数据
        连续出现次数 = 1
        # print('上一次结果为空，返回空')
        return None  # 第一帧作为基准，继续观察

    # 2. 如果当前数据与上一次完全相同，计数器累加
    if 检测数据 == 上一次结果:
        连续出现次数 += 1
    else:
        # 3. 💡 突变发生！一旦不同，说明状态不稳定，立刻重置基准和计数
        上一次结果 = 检测数据
        连续出现次数 = 1
        # print('与上一次结果不同，返回空')
        return None  # 突变帧不可信，返回 None 重新观察

    # 4. 只有当连续次数达到 3 次时，才给主流程扔出最终裁决
    if 连续出现次数 >= 连续次数:
        连续出现次数 = 1
        return 上一次结果
    # print('最后的空')
    return None  # 刚满 2 次，还在通往 3 次的路上，返回 None

def 寻敌检测主函数():
    寻敌=连续性检测(寻敌状态检测(血条检测()),25)
    return 寻敌
def 寻敌操作函数():
    if 寻敌检测主函数():
        print('执行寻敌操作')
        寻敌()
        time.sleep(5)
def 前推摇杆(时长=8):
    print("  -> 摇杆前推...")

    d.touch.down(371, 1062)
    time.sleep(0.05)
    d.touch.move(371, 848)
    time.sleep(时长)
    d.touch.up(371, 848)
def 非阻塞式前移摇杆(最大时长=1):
    d.touch.down(371, 1062)
    time.sleep(0.05)
    d.touch.move(371, 848)
    start_time=time.time()
    print('已开始移动，开始计时')
    try:
        while time.time()-start_time<最大时长:
            if hsv模板匹配('副本-战斗对话页', config.副本_战斗对话页hsv范围lower, config.副本_战斗对话页hsv范围upper):
                区域内随机坐标点击(1567, 1721, 1200, 1247)
                time.sleep(0.1)
                区域内随机坐标点击(2206, 2312, 1071, 1183)
                print('检测到触发战斗对话页，寻路结束')
                break
            if hsv模板匹配('副本-战斗交互', config.副本_战斗交互hsv范围lower, config.副本_战斗交互hsv范围upper):
                print('检测到交互按钮，默认已实现寻路效果')
                区域内随机坐标点击(2294, 2418, 966, 1086)
                time.sleep(1.5)
                break
    finally:
        d.touch.up(371, 848)

屏幕中心x=1278
终点标识符检测结果全局=False
防遮挡 = 0
def 终点标识符检测():
    """
    检测画面是否存在终点标识符，如果存在则会将视角对准，如果不存在则会转动视角
    :return: 对准标识符时，返回Ture
    """
    global 终点标识符检测结果全局,防遮挡
    终点标识符检测结果 = hsv模板匹配获取坐标('终点标识符', config.终点标识符hsv范围lower, config.终点标识符hsv范围upper,0.35)
    布尔值=False
    if 终点标识符检测结果:
        布尔值=True
    print(f'终点标识符检测结果{终点标识符检测结果}')
    连续性过滤 = 连续性检测(布尔值, 1)
    # print(f'连续性过滤后结果{连续性过滤}')
    if 连续性过滤:
        防遮挡=1
        print(f'终点标识符坐标为：{终点标识符检测结果}')
        终点标识符检测结果全局=True
        target_x, target_y = 终点标识符检测结果

        # 计算标识符偏离屏幕中心的距离
        偏差值 = target_x - 屏幕中心x

        if 偏差值 > 80:
            随机小幅度划屏((1278,692),'right',20)
            print("➡️ 标识符偏右，控制摇杆往右前方推，或者向右微调视角")
            # 你的摇杆控制逻辑...
        elif 偏差值 < -80:
            随机小幅度划屏((1278, 692),'left',20)
            print("⬅️ 标识符偏左，控制摇杆往左前方推，或者向左微调视角")
            # 你的摇杆控制逻辑...
        else:
            print("⬆️ 已经对准目标！返回True")
            # 寻路操作()
            return True
    elif 连续性过滤 is False:
        if 防遮挡==1:
            防遮挡=0
            print('检测到标识符出现后又消失，默认已对准')
            return True
        print('未检测到终点标识符，正在滑动视角')
        随机小幅度划屏((1278, 692),'left',100)
    # elif 连续性过滤 is None:
    #     防遮挡+=1
    #     print('连续性检测结果为空')

def 寻路主函数():
    global 终点标识符检测结果全局
    """
    重复检测画面，如果检测到标识符会执行移动，如果没有会重试，最大重试次数为20次
    :return:
    """
    for i in range(1,21):
        if hsv模板匹配('副本-战斗对话页', config.副本_战斗对话页hsv范围lower, config.副本_战斗对话页hsv范围upper):
            区域内随机坐标点击(1567, 1721, 1200, 1247)
            time.sleep(0.1)
            区域内随机坐标点击(2206, 2312, 1071, 1183)
            print('检测到触发战斗对话页，寻路结束')
            break
        if hsv模板匹配('副本-战斗交互',config.副本_战斗交互hsv范围lower,config.副本_战斗交互hsv范围upper):
            print('检测到交互按钮，默认已实现寻路效果')
            区域内随机坐标点击(2294,2418,966,1086)
            time.sleep(1.5)
            break
        if hsv模板匹配('副本-剧情对话页跳过', config.副本_剧情对话页跳过hsv范围lower, config.副本_剧情对话页跳过hsv范围upper):
            print('检测到剧情对话页，正在退出寻路')
            break
        if hsv模板匹配('副本-战斗结算', config.副本_战斗结算hsv范围lower, config.副本_战斗结算hsv范围upper):
            print('检测到战斗结算页，正在退出寻路')
            break
        if 图像是否存在从配置文件中获取文件路径('副本-战斗结算',gray_mode=True):
            print('检测到意识重启页，正在退出寻路')
            break
        if 终点标识符检测():
            防卡墙移动()
            break
    else:
        防卡墙移动()
    print('正在初始化终点标识符全局变量')
    终点标识符检测结果全局=False
def 卡墙时操作():
    随机小幅度划屏((1278, 692), 'right', 200)
    非阻塞式前移摇杆(1)
    if 终点标识符检测结果全局:
        print('卡墙，正在二次校验标识符方向')
        for i in range(1,21):
            if 终点标识符检测():
                print('已重新校验方向')
                break
        else:
            print('已超过最大重试次数，仍未检测到标识符')



def 防卡墙移动():
    移动次数=0
    最大重试次数=10
    while 移动次数<=7 and 最大重试次数>0:
        if hsv模板匹配('副本-战斗对话页',config.副本_战斗对话页hsv范围lower,config.副本_战斗对话页hsv范围upper):
            区域内随机坐标点击(1567, 1721, 1200, 1247)
            time.sleep(0.1)
            区域内随机坐标点击(2206, 2312, 1071, 1183)
            print('检测到触发战斗对话页，寻路结束')

            break
        if hsv模板匹配('副本-战斗交互', config.副本_战斗交互hsv范围lower, config.副本_战斗交互hsv范围upper):
            print('检测到交互按钮，默认已实现寻路效果')
            区域内随机坐标点击(2294, 2418, 966, 1086)
            time.sleep(1.5)
            break
        if hsv模板匹配('副本-剧情对话页跳过', config.副本_剧情对话页跳过hsv范围lower,
                       config.副本_剧情对话页跳过hsv范围upper):
            print('检测到剧情对话页，正在退出寻路')
            break
        if hsv模板匹配('副本-战斗结算', config.副本_战斗结算hsv范围lower, config.副本_战斗结算hsv范围upper):
            print('检测到战斗结算页，正在退出寻路')
            break
        if 图像是否存在从配置文件中获取文件路径('副本-战斗结算', gray_mode=True):
            print('检测到意识重启页，正在退出寻路')
            break
        if 卡墙检测():
            卡墙时操作()
            print('已执行卡墙时操作')
            最大重试次数-=1
        else:
            if 终点标识符检测结果全局:
                print('非卡墙，正在二次校验标识符方向')
                for i in range(1, 21):
                    if 终点标识符检测():
                        print('已重新校验方向')
                        break
            移动次数+=1
    print('已退出移动')


def 卡墙检测(x1=657, y1=190, x2=2158, y2=494, threshold_ratio=0.1):
    """通过对比指定区域(x1, y1, x2, y2)内的像素流变，检测角色是否卡墙

    :param x1: 裁剪区域左上角 X 坐标
    :param y1: 裁剪区域左上角 Y 坐标
    :param x2: 裁剪区域右下角 X 坐标
    :param y2: 裁剪区域右下角 Y 坐标
    :param check_duration: 两次截图的时间间隔（秒），通常 0.3 ~ 0.5 秒
    :param threshold_ratio: 判定为“画面有在动”的最小变化像素比例（默认 1.5%）
    :return: 卡墙返回 True，正常移动返回 False
    """
    # 1. 抓取第一帧画面
    img1 = 截图()
    if img1 is None:
        return False

    # 🌟 核心修改：利用 NumPy 切片直接裁剪出你指定的任意矩形区域
    # 注意：NumPy 矩阵的切片顺序是 [行, 列]，即 [y1:y2, x1:x2]
    crop1 = img1[y1:y2, x1:x2]
    gray1 = cv2.cvtColor(crop1, cv2.COLOR_BGR2GRAY)

    # 2. ⏳ 等待角色移动一小会儿
    非阻塞式前移摇杆(1)

    # 3. 抓取第二帧画面并用相同的坐标裁剪
    img2 = 截图()
    if img2 is None:
        return False

    crop2 = img2[y1:y2, x1:x2]
    gray2 = cv2.cvtColor(crop2, cv2.COLOR_BGR2GRAY)

    # 4. 🧮 计算这两块指定区域的绝对差值
    diff = cv2.absdiff(gray1, gray2)

    # 5. 二值化处理（过滤细微的环境光影变化）
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

    # 6. 统计该指定区域内发生改变的像素点数量
    changed_pixels = cv2.countNonZero(thresh)
    total_pixels = gray1.size  # 当前指定剪裁区域的总像素点数

    # 计算变化比例
    change_rate = changed_pixels / total_pixels

    # 🔍 调试日志，方便你精准校准不同区域的动态阈值
    print(f"DEBUG: 区域({x1},{y1})->({x2},{y2}) 流变比例: {change_rate * 100:.2f}%")

    # 7. ⚖️ 判定
    if change_rate < threshold_ratio:
        print(f"🚨 [卡墙判定] 指定区域静态重合率过高！流变仅 {change_rate * 100:.2f}%，判定为卡墙！")
        return True

    return False
寻敌次数=0
def 寻路寻敌检测():
    global 寻敌次数

    寻敌检测结果=寻敌检测主函数()
    if 寻敌检测结果:
        寻敌次数+=1

        寻敌()
        print('执行寻敌操作')
        print('寻敌次数加1')
    # elif 寻敌检测结果 is False:
    #     print('不需要寻敌，重置寻敌次数')
    #     寻敌次数 = 0
    if 寻敌次数>=5:
        print('寻敌无效，执行寻路中……')
        print('执行寻路操作,重置寻敌次数')
        寻敌次数=0
        with 共享变量.寻路和战斗锁:
            寻路主函数()
        print('寻路操作执行完毕,正在初始化变量')

def 寻敌子线程():
    print('子线程运行中')
    while True:
        while not 共享变量.停止寻敌信号:
            print('寻敌寻路中')
            寻路寻敌检测()
        time.sleep(0.5)
    print('寻敌子线程已结束')

def 页面识别(threshold=0.8):
    """
    遍历映射表，检测截图中存在的所有目标
    :param screenshot: 当前截图的 numpy 数组
    :param threshold: 匹配阈值
    :return: 一个列表，包含检测到的所有名称
    """
    detected_names = []
    img = 截图()
    for name, filename in TEMPLATE_MAP.items():
        template_path = os.path.join(TEMPLATE_DIR, filename)

        # 读取模板
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        if template is None:
            print(f"警告: 无法加载模板 {filename}")
            continue

        # 模板匹配
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        # 如果置信度高于阈值，认为存在
        if max_val >= threshold:
            detected_names.append(name)

    return detected_names
def ui变化检测(标识符,timeout=5,interval=0.1):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if 共享变量.latest_result!=标识符:
            print('合理合理退出合理退出合理退出合理退出合理退出合理退出退出')
            end_time=time.time()
            time_time = end_time - start_time
            print(f'合理退出合理退出合理退出合理退出合理退出时间{time_time}')
            return True
        time.sleep(interval)
    print('硬等待硬等待硬等待硬等待硬等待硬等待硬等待硬等待硬等待硬等待硬等待硬等待')
    return False


def yolo检测(img, conf_threshold=0.03):
    """
    执行单次检测并返回识别到的目标坐标
    :param conf_threshold: 置信度阈值
    :return: 包含所有检测框坐标的列表，每个元素为 [x1, y1, x2, y2]
    """
    # 1. 截图
    if img is None:
        return []

    # 2. 推理
    results = model(img, conf=conf_threshold, verbose=False)

    # 3. 提取坐标 (boxes.xyxy 返回的是 Tensor)
    boxes = results[0].boxes.xyxy.cpu().numpy().tolist()

    # 4. 可视化（返回绘制好的图片，用于调试）
    # annotated_frame = results[0].plot()
    # cv2.imshow("AI Monitor - Detection", annotated_frame)

    return boxes
# 配置字典（保持不变，方便后续增加新状态）
STATUS_CONFIG = {
    '青绿标识符': {
        'hsv_range': (np.array([44, 147, 88]), np.array([96, 255, 255])),
        'template': r'C:\Users\ZhuanZ1\Desktop\rpa\zhanshuangfuben\ziyuanwenjian\biaoshi\img_11.png'
    },
    '红色标识符': {
        'hsv_range': (np.array([0, 156, 151]), np.array([179, 255, 255])),
        'template': r'C:\Users\ZhuanZ1\Desktop\rpa\zhanshuangfuben\ziyuanwenjian\biaoshi\img_19.png'
    }
}

# 预先加载所有模板，避免在循环中重复读取 IO
LOADED_TEMPLATES = {
    key: {
        'gray': cv2.cvtColor(cv2.imread(config['template'], cv2.IMREAD_COLOR), cv2.COLOR_BGR2GRAY),
        'hsv_range': config['hsv_range']
    }
    for key, config in STATUS_CONFIG.items()
    if cv2.imread(config['template']) is not None
}


def hsv模板匹配获取坐标(key, hsv_lower, hsv_upper, threshold=0.85):
    """
    复合检测函数：先 HSV 掩膜过滤，再进行模板匹配
    :param key: 模板图片键名
    :param hsv_lower: HSV下限
    :param hsv_upper: HSV上限
    :param threshold: 匹配置信度阈值
    :return: 匹配成功返回中心点坐标 (center_x, center_y), 否则返回 False
    """
    # 1. 加载模板
    hsv_lower = np.array(hsv_lower)
    hsv_upper = np.array(hsv_upper)
    template = cv2.imread(config.图片标识符清单.get(key), cv2.IMREAD_COLOR)
    if template is None:
        print(f"警告：无法加载模板 {key}")
        return False

    # 🌟 获取原模板的宽度(w)和高度(h)，用于后续计算中心点
    h, w = template.shape[:2]
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # 2. 获取实时画面
    img = 截图()
    if img is None:
        return False

    # 3. HSV 过滤
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, hsv_lower, hsv_upper)

    # 4. 灰度处理与位运算（抠图）
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    masked_img = cv2.bitwise_and(img_gray, img_gray, mask=mask)

    # 5. 模板匹配
    res = cv2.matchTemplate(masked_img, template_gray, cv2.TM_CCOEFF_NORMED)
    # 🌟 将第四个参数 max_loc（匹配区域的左上角坐标）接住
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    # 打印日志以便调试
    # print(f"DEBUG: 匹配度 {max_val:.4f}")

    # 6. 判断并返回中心坐标
    if max_val >= threshold:
        # 🌟 左上角 X, Y 坐标分别加上模板自身宽高的一半，得到几何中心点
        center_x = int(max_loc[0] + w / 2)
        center_y = int(max_loc[1] + h / 2)
        return (center_x, center_y)

    return False
def hsv模板匹配(key, hsv_lower, hsv_upper, threshold=0.85):
    """
    复合检测函数：先 HSV 掩膜过滤，再进行模板匹配
    :param key: 模板图片键名
    :param hsv_lower: HSV下限
    :param hsv_upper: HSV上限
    :param threshold: 匹配置信度阈值
    :return: 匹配成功返回 True, 否则返回 False
    """
    # 1. 加载模板
    hsv_lower=np.array(hsv_lower)
    hsv_upper=np.array(hsv_upper)
    template = cv2.imread(config.图片标识符清单.get(key), cv2.IMREAD_COLOR)
    if template is None:
        print(f"警告：无法加载模板 {key}")
        return False

    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # 2. 获取实时画面
    img = 截图()
    if img is None:
        return False

    # 3. HSV 过滤
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, hsv_lower, hsv_upper)

    # 4. 灰度处理与位运算（抠图）
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    masked_img = cv2.bitwise_and(img_gray, img_gray, mask=mask)

    # 5. 模板匹配
    res = cv2.matchTemplate(masked_img, template_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    # 打印日志以便调试
    print(f"DEBUG: 匹配度 {max_val:.4f}")

    return max_val >= threshold
def 战斗场景检测():
    battle_hsv_min =[0, 0, 244] # 根据你的实际场景设置
    battle_hsv_max =[179, 8, 255]
    战斗场景检测=hsv模板匹配('战斗标识符',battle_hsv_min,battle_hsv_max)
    print(f'战斗场景检测{战斗场景检测}')
    if 战斗场景检测:
        return True
    else:
        return False


def 获取最右侧未通关关卡调试版(img, boxes, threshold=0.7):
    """
    最严格进度筛选逻辑（全面加强调试日志版）
    """
    try:
        if not boxes:
            print("\n[🔍 调试-异常] ❌ 未检测到任何关卡区域 (boxes为空)")
            return 0

        print(f"\n================ 🔍 关卡筛选雷达启动 ================")
        print(f"[🔍 调试-输入] 屏幕当前检测到 {len(boxes)} 个关卡目标。")

        # ———————— 第一步：获取全局最右边界 (x2) ————————
        # 增加排序日志，让你看到所有关卡的右边界排布
        all_x2s = [int(box[2]) for box in boxes]
        max_x2_overall = max(all_x2s)
        print(f"[🔍 调试-全局] 所有关卡右边界坐标列表: {sorted(all_x2s)}")
        print(f"[🔍 调试-全局] 🎯 认定当前屏幕【全局最右侧边界】 max_x2_overall = {max_x2_overall}")

        # ———————— 第二步：排除已通关区域，找出候选者 ————————
        uncompleted_candidates = []

        # 💡 引入 enumerate 给关卡编个号 (从1开始)，方便在日志里追踪具体是哪一个
        for idx, box in enumerate(boxes, start=1):
            x1, y1, x2, y2 = map(int, box)
            center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2

            print(f"\n--- 📦 正在排查 编号#{idx} 关卡 ---")
            print(f" 坐标范围: ({x1}, {y1}) -> ({x2}, {y2}) | 中心点: ({center_x}, {center_y})")

            # 获取 ROI 并检查有效性
            roi = img[max(0, y1):min(img.shape[0], y2), max(0, x1):min(img.shape[1], x2)]
            if roi.size == 0:
                print(f" ⚠️ [警告] 编号#{idx} 关卡的 ROI 裁剪区域大小为 0，跳过处理。")
                continue

            is_occupied = False
            roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

            for state, data in LOADED_TEMPLATES.items():
                mask = cv2.inRange(roi_hsv, data['hsv_range'][0], data['hsv_range'][1])
                pixel_count = cv2.countNonZero(mask)

                # 💡 详细打印当前状态模板的匹配过程
                if pixel_count > 100:
                    masked_roi = cv2.bitwise_and(roi_gray, roi_gray, mask=mask)
                    roi_h, roi_w = masked_roi.shape[:2]
                    tpl_h, tpl_w = data['gray'].shape[:2]
                    if roi_h < tpl_h or roi_w < tpl_w:
                        print(
                            f" ⏭️ [防崩拦截] 编号#{idx} 区域尺寸({roi_w}x{roi_h})小于模板尺寸({tpl_w}x{tpl_h})，放弃匹配。")
                        continue
                    res = cv2.matchTemplate(masked_roi, data['gray'], cv2.TM_CCOEFF_NORMED)
                    _, max_val, _, _ = cv2.minMaxLoc(res)

                    print(
                        f" 🔍 [匹配中] 匹配模板:[{state}] | 遮罩像素数:{pixel_count} | 匹配置信度:{max_val:.4f} (阈值:{threshold})")

                    if max_val >= threshold:
                        print(f" 🛑 [结果] 编号#{idx} 匹配成功！判定为：【已通关/已被占领】")
                        is_occupied = True
                        break
                else:
                    # 记录一下为什么连模板匹配都没进（经常因为色彩范围不对导致像素不够）
                    print(f" ⏭️ [跳过] 匹配模板:[{state}] | 遮罩绿色/特定色像素仅有 {pixel_count} (未达100门槛)")

            # 将未被匹配到的（未通关）存入候选
            if not is_occupied:
                print(f" ✨ [结果] 编号#{idx} 未检测到任何通关标识 -> 【加入未通关候选队列】")
                uncompleted_candidates.append({
                    'id': idx,
                    'center': (center_x, center_y),
                    'x2': x2
                })

        # ———————— 第三步 & 第四步：找出候选中的最右，并与全局做比较 ————————
        print(f"\n================ ⚖️ 最终校验决策阶段 ================")
        if not uncompleted_candidates:
            print("[🔍 调试-决策] 😭 候选队列为空：屏幕上所有关卡均已被通关，脚本无操作。")
            return 0

        print(f"[🔍 调试-决策] 候选队列中共有 {len(uncompleted_candidates)} 个未通关关卡：")
        for cand in uncompleted_candidates:
            print(f"  -> 候选 编号#{cand['id']} | 右边界 x2 = {cand['x2']} | 中心点 = {cand['center']}")

        # 找出剩余未通关关卡中，最靠右的那一个
        best_candidate = max(uncompleted_candidates, key=lambda c: c['x2'])
        candidate_max_x2 = best_candidate['x2']

        # 计算差距，防止因为 1~2 个像素的微小变动错失点击机会
        pixel_diff = abs(candidate_max_x2 - max_x2_overall)
        print(f"\n[🔍 调试-对比] 候选最右边界 x2 = {candidate_max_x2} (来自编号#{best_candidate['id']})")
        print(f"[🔍 调试-对比] 全局最右边界 x2 = {max_x2_overall}")
        print(f"[🔍 调试-对比] 两者像素绝对差距: {pixel_diff} 像素")

        # 【最终核心逻辑校验】
        # 💡 考虑实际运行中可能有 1-2 像素的微小波动，这里我依然维持你绝对相等的严格逻辑，但打印极度清晰
        if candidate_max_x2 == max_x2_overall:
            print(f" 🟩 [校验通过] ✅ 最新的关卡 (编号#{best_candidate['id']}) 尚未通关！准备返回中心点进行点击。")
            print(f"====================================================\n")
            return best_candidate['center']
        else:
            print(f" 🟥 [校验失败] ❌ 物理位置最靠右的图标已经是 '已通关' 状态。")
            print(f" 提示信息: 左侧虽然存在未通关关卡 (编号#{best_candidate['id']}), 但为了避免回头打旧关卡，执行安全拦截。")
            print(f"====================================================\n")
            return 0
    except Exception as  e:
        print('获取最右侧关卡函数出现错误，返回0')
        print(f'错误信息：{e}')
        return 0
def 获取最右侧未通关关卡(img, boxes, threshold=0.85):
    """
    最严格进度筛选逻辑：
    1. 计算屏幕上所有区域的 x2 最大值 (全局最右边界)。
    2. 遍历所有区域，通过模板匹配排除已通关区域，找出所有“未通关”候选者。
    3. 如果存在候选者，找出候选者中 x2 最大的那个 (候选最右边界)。
    4. 【最终校验】：只有当 (候选最右边界 == 全局最右边界) 时，才返回该候选中心。
    """
    if not boxes:
        print("未检测到任何关卡区域")
        return 0
    print(f'当前检测到 {len(boxes)} 个关卡')

    # ———————— 第一步：获取全局最右边界 (x2) ————————
    # 我们认为，这个坐标代表了当前屏幕上最新的关卡所在位置
    all_x2s = [int(box[2]) for box in boxes]
    max_x2_overall = max(all_x2s)
    print(f"当前屏幕最右侧图标边界 x2 = {max_x2_overall}")

    # ———————— 第二步：排除已通关区域，找出候选者 ————————
    uncompleted_candidates = []

    for box in boxes:
        x1, y1, x2, y2 = map(int, box)
        # 获取 ROI 并检查有效性
        roi = img[max(0, y1):min(img.shape[0], y2), max(0, x1):min(img.shape[1], x2)]
        if roi.size == 0: continue

        # 模板匹配状态排查 (逻辑同你原有的，此处不赘述细节)
        is_occupied = False
        roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        for state, data in LOADED_TEMPLATES.items():
            mask = cv2.inRange(roi_hsv, data['hsv_range'][0], data['hsv_range'][1])
            print(f'副本首页标识符像素数量：{cv2.countNonZero(mask)}')
            if cv2.countNonZero(mask) > 100:
                masked_roi = cv2.bitwise_and(roi_gray, roi_gray, mask=mask)
                res = cv2.matchTemplate(masked_roi, data['gray'], cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                print(f'副本标识符模板匹配置信度{max_val}')
                if max_val >= threshold:
                    is_occupied = True
                    break

        # 将未被匹配到的（未通关）存入候选
        if not is_occupied:
            print(f'存在关卡未被检测到通关标识符')
            uncompleted_candidates.append({
                'center': ((x1 + x2) // 2, (y1 + y2) // 2),
                'x2': x2
            })
            print(uncompleted_candidates)

    # ———————— 第三步 & 第四步：找出候选中的最右，并与全局做比较 ————————

    if not uncompleted_candidates:
        print("屏幕上所有关卡均已通关 (或未匹配到)，无操作。")
        return 0

    # 找出剩余未通关关卡中，最靠右的那一个
    best_candidate = max(uncompleted_candidates, key=lambda c: c['x2'])
    candidate_max_x2 = best_candidate['x2']

    print(f"剩余未通关关卡中最靠右的边界 x2 = {candidate_max_x2}")

    # 【最终核心逻辑校验】
    # 只有当：最右边的未通关关卡的 x2，等于全局最右图标的 x2
    # 这意味着：最新的关卡还没打，可以打。
    if candidate_max_x2 == max_x2_overall:
        print(f"校验通过！最新的关卡 (x2={candidate_max_x2}) 尚未通关，准备点击。")
        return best_candidate['center']
    else:
        # 如果 candidate_max_x2 < max_x2_overall，
        # 说明物理位置最靠右的那个已经是"已通关"状态了。
        print(f"校验失败：最靠右的图标已被通关 (全局x2={max_x2_overall})。")
        print(f"左侧存在未通关关卡 (x2={candidate_max_x2})，但按逻辑跳过，避免点旧关卡。")
        return 0
hsv_min=np.array([0,0,246])
hsv_max=np.array([74, 3, 255])
def 战斗标识检测(image, roi=(2065, 1219, 68, 81)):
    """
     检测指定区域内符合HSV区间的像素点数量。

     参数:
     - image: 输入的BGR格式图像
     - hsv_min: HSV下限 (例如: np.array([0, 0, 0]))
     - hsv_max: HSV上限 (例如: np.array([180, 255, 255]))
     - roi: 感兴趣区域 (x, y, width, height)

     返回:
     - 1: 如果数量 > 200
     - 0: 否则
     """
    # 1. 解包ROI坐标
    x, y, w, h = roi

    # 2. 截取感兴趣区域 (注意：OpenCV中图像矩阵是[y:y+h, x:x+w])
    crop_img = image[y:y + h, x:x + w]

    # 3. 将图像转换为HSV色彩空间
    hsv_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)

    # 4. 创建掩膜，查找在区间内的像素
    mask = cv2.inRange(hsv_img, hsv_min, hsv_max)

    # 5. 统计像素数量 (mask中白色像素值为255，非白色为0)
    pixel_count = cv2.countNonZero(mask)

    # 6. 判断并返回
    print(f'战斗标识符像素点{pixel_count}')
    return 1 if pixel_count > 500 else None


def 章节标签位置初始化():
    while True:
        首个章节标签 = 图像是否存在('ziyuanwenjian/biaoshi/img_15.png')
        if 首个章节标签:
            break
        else:
            d.swipe(150, 345, 160, 1215, steps=10)
            time.sleep(1.5)
def 章节位置初始化():
    for i in range(6):
        print(f"正在进行第 {i + 1} 次向右滑动...")
        d.swipe_ext("right", scale=0.2)
        time.sleep(0.8)


def 检查区域是否命中章节标签黑名单(blacklist_dict=config.章节标签黑名单, roi=config.章节标签roi, threshold=0.85):
    """
    检测屏幕上指定区域内是否存在字典里的模板图片

    :param current_img: 通过 d.screenshot(format='opencv') 拿到的三维 numpy 数组
    :param blacklist_dict: 你的黑名单字典（包含标签名和对应的图片绝对路径）
    :param roi: 指定区域的坐标，格式为 [x1, y1, x2, y2]。如果为 None，则全屏检测
    :param threshold: 匹配度阈值，超过这个值认为“存在”
    :return: 只要匹配到任何一个模板就返回 True，全都没匹配到返回 False
    """
    # 1. 裁剪指定区域 (ROI)
    current_img=截图()
    if roi:
        x1, y1, x2, y2 = roi
        # 记得做边界防御，防止切图超出屏幕范围
        h, w = current_img.shape[:2]
        crop_img = current_img[max(0, y1):min(h, y2), max(0, x1):min(w, x2)]
        if crop_img.size == 0:
            print("⚠️ 传入的 ROI 区域大小为 0，跳过检测。")
            return False
    else:
        crop_img = current_img

    # 2. 将目标区域转换为灰度图（加速匹配）
    gray_crop = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # 3. 遍历黑名单字典进行匹配
    for name, path in blacklist_dict.items():
        # 防御性编程：确保文件路径存在
        if not os.path.exists(path):
            print(f"⚠️ 警告：黑名单文件不存在，已跳过：{path}")
            continue

        # 读取模板并转为灰度图
        template = cv2.imread(path, 0)
        if template is None:
            print(f"⚠️ 错误：无法读取图片（可能格式损坏）：{path}")
            continue

        # 检查模板图是否比裁剪后的目标图还要大，如果大则无法匹配
        if template.shape[0] > gray_crop.shape[0] or template.shape[1] > gray_crop.shape[1]:
            # print(f"ℹ️ 模板 [{name}] 比指定检测区域还大，无法匹配，跳过。")
            continue

        # 执行模板匹配
        res = cv2.matchTemplate(gray_crop, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        print(f"🔍 正在比对黑名单标签 [{name}] ... 当前最高匹配度: {max_val:.4f}")

        # 4. 只要有一个匹配成功，立刻返回 True
        if max_val >= threshold:
            print(f"🚫 命中黑名单！成功检测到标签：[{name}]，匹配度({max_val:.4f}) >= 阈值({threshold})")
            return True

    # 5. 循环结束，一个都没对上，返回 False
    return False


def 是否命中章节黑名单(blacklist_dict=config.章节黑名单, roi=config.章节roi, threshold=0.85):
    """
    检测屏幕上指定区域内是否存在字典里的模板图片
    :param blacklist_dict: 你的黑名单字典（包含标签名和对应的图片绝对路径）
    :param roi: 指定区域的坐标，格式为 [x1, y1, x2, y2]。如果为 None，则全屏检测
    :param threshold: 匹配度阈值，超过这个值认为“存在”
    :return: 只要匹配到任何一个模板就返回 True，全都没匹配到返回 False
    """
    # 1. 裁剪指定区域 (ROI)
    current_img = 截图()
    if roi:
        x1, y1, x2, y2 = roi
        # 记得做边界防御，防止切图超出屏幕范围
        h, w = current_img.shape[:2]
        crop_img = current_img[max(0, y1):min(h, y2), max(0, x1):min(w, x2)]
        if crop_img.size == 0:
            print("⚠️ 传入的 ROI 区域大小为 0，跳过检测。")
            return False
    else:
        crop_img = current_img

    # 2. 将目标区域转换为灰度图（加速匹配）
    gray_crop = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

    # 3. 遍历黑名单字典进行匹配
    for name, path in blacklist_dict.items():
        # 防御性编程：确保文件路径存在
        if not os.path.exists(path):
            print(f"⚠️ 警告：黑名单文件不存在，已跳过：{path}")
            continue

        # 读取模板并转为灰度图
        template = cv2.imread(path, 0)
        if template is None:
            print(f"⚠️ 错误：无法读取图片（可能格式损坏）：{path}")
            continue

        # 检查模板图是否比裁剪后的目标图还要大，如果大则无法匹配
        if template.shape[0] > gray_crop.shape[0] or template.shape[1] > gray_crop.shape[1]:
            # print(f"ℹ️ 模板 [{name}] 比指定检测区域还大，无法匹配，跳过。")
            continue

        # 执行模板匹配
        res = cv2.matchTemplate(gray_crop, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        print(f"🔍 正在比对黑名单标签 [{name}] ... 当前最高匹配度: {max_val:.4f}")

        # 4. 只要有一个匹配成功，立刻返回 True
        if max_val >= threshold:
            print(f"🚫 命中黑名单！成功检测到标签：[{name}]，匹配度({max_val:.4f}) >= 阈值({threshold})")
            return True

    # 5. 循环结束，一个都没对上，返回 False
    return False
def 未通关章节定位():
    '''
    遍历判断，直到定位到没有通关标识的章节
    '''
    章节滑动次数 = 0  # 初始化计数器
    # 最大挑战/切换次数限制为 8 次
    for 尝试次数 in range(1, 9):
        print(f"正在进行第 {尝试次数} 次章节标签黑名单检测...")

        章节标签黑名单结果 = 检查区域是否命中章节标签黑名单(blacklist_dict=config.章节标签黑名单)

        if 章节标签黑名单结果:
            print(f"🚫 第 {尝试次数} 次检测：命中黑名单！正在执行切换动作...")

            下一章ui = (138, 963)
            下一章ui = 坐标随机(下一章ui, left=120, right=120, up=15, down=15)
            adb_click(下一章ui)

            # 适当增加一点等待动画的时间，防止连续点击过快导致游戏 UI 没刷新过来
            time.sleep(1.0)
        else:
            print("🎉 检测通过：当前章节标签不在黑名单中，退出拦截循环。")
            break
    else:
        # 💡 这是一个高级语法：当 for 循环完整跑满 8 次且没有触发 break 时，会走到这里
        print("⚠️ 警告：已经连续切换了 8 次章节，依然处于黑名单中！脚本可能已迷路，建议触发兜底策略。")
        # 这里可以写你的兜底逻辑，比如 return 退出函数，或者报错截图
    while True:
        通关标志 = 图像是否存在('ziyuanwenjian/biaoshi/img_16.png')

        if 通关标志:
            # 执行左滑
            d.swipe_ext("left", scale=0.2)
            章节滑动次数 += 1  # 计数加 1
            print(f"检测到通关标志，已累计向左滑动 {章节滑动次数} 次")
            time.sleep(1)

            # 当滑动满 7 次时触发
        else:
            章节黑名单结果=是否命中章节黑名单(blacklist_dict=config.章节黑名单)
            if 章节黑名单结果:
                d.swipe_ext("left", scale=0.2)
                章节滑动次数 += 1  # 计数加 1
                time.sleep(1)
            else:
                print("未检测到通关标志且当前章节未在黑名单中，已定位到未通关章节。")
                break
        if 章节滑动次数 == 7:
            print("已满 7 次，执行点击动作...")

            # 执行点击（请替换为你的实际目标坐标）
            下一章ui = (138, 963)
            下一章ui = 坐标随机(下一章ui, left=120, right=120, up=15, down=15)
            adb_click(下一章ui)
            time.sleep(0.6)

            # 【核心修改】：重置计数器，不退出，让 while 循环继续重复执行
            章节滑动次数 = 0
            print("点击完成，重置计数，继续当前函数循环...")




def 普攻():
    普攻坐标 = (2388, 1261)
    clink_zuobiao = 坐标随机(普攻坐标, left=80, right=80, up=70, down=70)
    adb_click(clink_zuobiao)


def 闪避():
    闪避坐标 = (2107, 1266)
    clink_zuobiao = 坐标随机(闪避坐标, left=80, right=80, up=80, down=80)
    adb_click(clink_zuobiao)


def 必杀():
    必杀坐标 = (1826, 1267)
    clink_zuobiao = 坐标随机(必杀坐标, left=80, right=80, up=80, down=80)
    adb_click(clink_zuobiao)


def 消球():
    球1 = (2432, 1032)
    球2 = (2218, 1028)
    球1_x = 坐标随机(球1, left=50, right=50, up=40, down=40)
    球2_x = 坐标随机(球2, left=60, right=60, up=60, down=60)
    adb_click(球1_x)
    adb_click(球2_x)


def 寻敌():
    zuo = (2223, 771)
    xy = 坐标随机(zuo, left=40, right=40, up=40, down=40)
    adb_click(xy)
def 消球检测(img):
    BALL_COLORS = {
        "红黄蓝": {"lower": np.array([0, 0, 210]), "upper": np.array([179, 38, 255])}
    }
    dict_a = [(2447, 1013), (2228, 1013)]

    # img = cv2.imread('adbxi.png')
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for index, (pt_x, pt_y) in enumerate(dict_a):
        # 截取采样区域 (±65像素)
        sample = hsv_img[pt_y - 50:pt_y + 50, pt_x - 50:pt_x + 50]

        # 对该区域遍历每种颜色配置
        for name, bounds in BALL_COLORS.items():
            mask = cv2.inRange(sample, bounds["lower"], bounds["upper"])
            # 如果符合条件的像素超过 1500 个，视为发现目标
            # print(f'颜色名：{name}像素点：{cv2.countNonZero(mask)}')
            if cv2.countNonZero(mask) > 240:
                return name

    return None


def 必杀检测(image):
    """
    检测图片中指定区域内符合 HSV 范围的像素点数量

    :param lower_hsv: np.array([h_min, s_min, v_min])
    :param upper_hsv: np.array([h_max, s_max, v_max])
    :param roi: 区域坐标元组 (x, y, w, h)
    :return: 区域内符合条件的像素总数
    """
    lower_hsv = np.array([40, 0, 248])
    upper_hsv = np.array([110, 71, 255])
    roi = (57, 123, 423, 8)
    # 1. 转换颜色空间
    # image=截图()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 2. 生成掩膜 (符合范围的显示为白色)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # 3. 提取 ROI (截取感兴趣区域)
    x, y, w, h = roi
    # 确保 ROI 不会超出图片边界
    roi_mask = mask[y:y + h, x:x + w]

    # 4. 统计白色像素数量
    # countNonZero 统计非零像素，即 mask 中白色部分的数量
    count = cv2.countNonZero(roi_mask)
    if count > 150:
        return 1
    return 0


def 闪避检测(image):
    """
      检测图片中指定区域内符合 HSV 范围的像素点数量

      :param image: 输入的图片对象 (BGR格式)
      :param lower_hsv: np.array([h_min, s_min, v_min])
      :param upper_hsv: np.array([h_max, s_max, v_max])
      :param roi: 区域坐标元组 (x, y, w, h)
      :return: 区域内符合条件的像素总数
      """
    lower_hsv = np.array([0, 205, 197])
    upper_hsv = np.array([29, 255, 255])
    # roi: 区域坐标元组 (x, y, w, h)
    roi = (739, 562, 900, 542)
    # 1. 转换颜色空间
    # image=截图()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 2. 生成掩膜 (符合范围的显示为白色)
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)

    # 3. 提取 ROI (截取感兴趣区域)
    x, y, w, h = roi
    # 确保 ROI 不会超出图片边界
    roi_mask = mask[y:y + h, x:x + w]

    # 4. 统计白色像素数量
    # countNonZero 统计非零像素，即 mask 中白色部分的数量
    count = cv2.countNonZero(roi_mask)
    print(count)
    if count > 1800:
        return 1
    return 0

def 战斗退出():
    区域内随机坐标点击(2390,2490,55,141)
    time.sleep(1)
    图像随机位置点击('ziyuanwenjian/biaoshi/img_23.png')
    time.sleep(0.8)
    图像随机位置点击('ziyuanwenjian/biaoshi/img_24.png')
    time.sleep(3)
    for _ in range(3):#等待作战失败文字出现
        if 图像是否存在从配置文件中获取文件路径('作战失败'):
            break
        else:
            time.sleep(1)
    for i in range(1,4):#循环点击，直至作战失败消失
        print(f'作战失败标识符检测：第{i}次')
        if 图像是否存在从配置文件中获取文件路径('作战失败'):
            print(f'检测到作战失败标识符，正在执行点击')
            区域内随机坐标点击(607, 1955, 494, 1220)
            time.sleep(0.8)
        else:
            break
        time.sleep(1)

def 战斗主函数():
    empty_count = 0
    start_time_1 = time.time()
    print('开始战斗计时')
    while not 共享变量.超时信号:
        print(f'当前已运行时间:{time.time() - start_time_1}')
        if time.time() - start_time_1 > 240:
            共享变量.超时信号 = True
            print('副本已超时，正在执行退出')
            print('正在同步时间')
            break
        with 共享变量.寻路和战斗锁:
            img = 截图()
            try:
                # 1. 优先级最高：闪避检测
                n = 战斗标识检测(img)

                print(f'战斗标识物持续未出现次数{empty_count}')
                if n is None:
                    empty_count += 1
                    if empty_count >= 12:
                        print('退出战斗循环')
                        break
                else:
                    print('存在标志物')
                    empty_count = 0

                if 闪避检测(img) == 1:
                    print("触发闪避")
                    闪避()
                    time.sleep(0.5)  # 闪避后给予短暂空隙，防止连点
                    continue  # 跳过本次循环剩余部分，重新检测

                # 2. 优先级次之：必杀检测
                if 必杀检测(img) == 1:
                    print("触发必杀")
                    必杀()
                    time.sleep(1.0)  # 必杀动画时间
                    continue

                # 3. 优先级第三：消球检测
                # 注意：这里需要根据你的消球逻辑处理返回值
                球颜色 = 消球检测(img)
                if 球颜色 is not None:
                    print(f"触发消球: {球颜色}")
                    消球()
                    time.sleep(0.3)
                    continue

                # 4. 最低优先级：普攻 (如果上面都没触发，则执行普攻)
                普攻()
                print('普攻')
                # 控制全局节奏，防止操作过快导致卡顿
                time.sleep(0.1)
                # end_time = time.perf_counter()
                # elapsed_time = end_time - start_time
                # print(f'循环一次耗时：【{elapsed_time}】')
            except Exception as e:
                print(f"战斗发生异常: {e}")
                time.sleep(1)
        time.sleep(0.05)
    print('退出战斗循环，正在结束子线程')
    共享变量.停止寻敌信号 = True
    print("🎉 子线程已经彻底凉透，主线程可以安心继续推进了。")
    if 共享变量.超时信号:
        print('副本超时，正在执行退出并更新黑名单')
        战斗退出()
        黑名单更新(共享变量.章节名截图)
    print('已退出战斗主函数')


def 黑名单更新(img):
    """
        自动随机生成章节名，保存图片，并直接写入 config.py 源代码实现永久记忆
        :param img: OpenCV 格式的图片矩阵
        """
    # 1. 防御性创建资源文件夹
    if not os.path.exists(config.标识符文件夹路径):
        os.makedirs(config.标识符文件夹路径)

    # 2. 自动检测序号，避免文件名冲突
    序号 = 0
    while True:
        图片名称 = f"img_{序号}.png"
        全路径 = os.path.join(config.标识符文件夹路径, 图片名称)
        if not os.path.exists(全路径):
            break
        序号 += 1

    # 3. 🎲 自动随机生成一个唯一的章节名
    随机四位数字 = random.randint(1000, 9999)
    随机章节名 = f"随机章节-{随机四位数字}-img_{序号}"

    # 4. 写入图片到硬盘（兼容中文路径）
    try:
        _, img_encode = cv2.imencode('.png', img)
        with open(全路径, 'wb') as f:
            f.write(img_encode.tobytes())
        print(f"💾 局部截图已保存 -> {全路径}")
    except Exception as e:
        print(f"❌ 图片写入硬盘失败: {e}")
        return

    # 6. 🚀【核心：直接往 config.py 源码里追加写入新黑名单数据】实现长期记忆
    # 构造一行标准的 Python 字典追加代码
    code_line = f'\n章节黑名单["{随机章节名}"] = os.path.join(项目根目录路径, "ziyuanwenjian", "biaoshi", "{图片名称}")\n'

    try:
        # 使用 'a' 模式（追加模式），直接在 config.py 的文件末尾塞入这行代码
        with open(config.配置文件路径, 'a', encoding='utf-8') as f:
            f.write(code_line)
        print(f"🔮 [长期记忆] 成功将黑名单代码刻入 config.py 源码！")
    except Exception as e:
        print(f"❌ 写入 config.py 失败: {e}")
def 路径向导(relative_path):
    """
    自动补全目录深度，并统一路径格式
    """
    # 1. 强制统一将反斜杠 \ 替换为正斜杠 /，防止系统兼容性问题
    relative_path = relative_path.replace('\\', '/')

    # 2. 如果你是从“Python文件”目录中运行的，需要回退一级到根目录
    # 我们在这里直接自动帮你拼接 '../'
    formatted_path = os.path.join("..", relative_path)

    if getattr(sys, 'frozen', False):
        # 打包环境：临时目录
        base_path = sys._MEIPASS
    else:
        # 开发环境：当前代码所在目录的上一级
        base_path = os.path.abspath("..")

    # 最终拼接出来的结果就是正确的路径
    return os.path.join(base_path, relative_path)


def 随机小幅度划屏(起止点,滑动方向, 滑动距离=40, 持续时间=0.1):
    """在屏幕中心随机区域内，执行指定方向的小幅度平滑滑动（适用于视角微调）
    :param 起止点：坐标元组
    :param d: uiautomator2 的连接对象实例 (例如 d = u2.connect())
    :param 滑动方向: 滑动方向，可选字符串: 'left' / 'right' / 'up' / 'down'
    :param 滑动距离: 滑动的像素跨度，默认 80（对应你之前的 1040-960）
    :param 持续时间: 滑动动作持续时间（秒），默认 0.1 秒以保持平滑转视角
    """
    # 1. 在屏幕中心 (960, 540) 附近生成一个随机起点，避免每次点位完全一致
    # 这样可以模拟真实手指按在屏幕上的微小位置差异
    x,y=起止点
    start_x = x + random.randint(-30, 30)
    start_y = y + random.randint(-15, 15)

    # 给滑动的像素距离也加一点点随机抖动，让轨迹更拟真
    real_distance = 滑动距离 + random.randint(-5, 5)

    # 2. 根据方向计算对应的终点坐标
    if 滑动方向 == "left":
        end_x = start_x - real_distance
        end_y = start_y + random.randint(-10, 10)  # Y轴允许有极微小的手抖偏差
    elif 滑动方向 == "right":
        end_x = start_x + real_distance
        end_y = start_y + random.randint(-10, 10)
    elif 滑动方向 == "up":
        end_x = start_x + random.randint(-10, 10)  # X轴允许有极微小的手抖偏差
        end_y = start_y - real_distance
    elif 滑动方向 == "down":
        end_x = start_x + random.randint(-10, 10)
        end_y = start_y + real_distance
    else:
        print(f"❌ 错误：不支持的滑动方向 [{滑动方向}]")
        return False

    # 3. 打印 DEBUG 日志，方便你在控制台观察视角控制是否频繁触发
    # print(f"🔄 视角微调: 方向 [{direction}], 轨迹 ({start_x}, {start_y}) -> ({end_x}, {end_y}), 耗时: {duration}s")

    # 4. 调用 u2 执行物理滑动
    try:
        d.swipe(start_x, start_y, end_x, end_y, duration=持续时间)
        return True
    except Exception as e:
        print(f"⚠️ 滑动操作异常: {e}")
        return False

if __name__ == '__main__':
    防卡墙移动()