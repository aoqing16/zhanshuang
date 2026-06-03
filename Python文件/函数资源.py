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
print('模型加载中')
model = YOLO(r'C:\Users\ZhuanZ1\runs\detect\train-8\weights\best.pt')
model_1 = YOLO(r"C:\Users\ZhuanZ1\runs\classify\train-5\weights\best.pt")
# from Python文件.中央调度器 import 页面识别

# 1. 连接设备
d = u2.connect('127.0.0.1:16384')


def 截图():
    img = d.screenshot(format='opencv')
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


def 图像存在判断(img,img_name, threshold=0.8, ):
    """
    匹配模板并在匹配区域内返回一个随机坐标
    :param img:
    :param img_name: 模板图片文件名
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
    h, w = template.shape[:2]
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val >= threshold:
        # 获取匹配区域的左上角 (x, y)
        return 1
    return None
def 图像随机位置点击(img_name, threshold=0.8, padding=0):
    """
    匹配模板并在匹配区域内返回一个随机坐标
    :param img_name: 模板图片文件名
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
        d.click(x, y)
    else:
        return



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
    results = model_1(img, conf=0.8, verbose=False)

    # 分类结果解析
    probs = results[0].probs
    top1_id = probs.top1
    top1_conf = probs.top1conf.item()
    label = results[0].names[top1_id]
    print(f'yolo检测函数返回结果{label}置信度：{top1_conf: 2f}')
    # 打印结果和耗时
    # print(f"当前页面: {label} | 置信度: {top1_conf:.2f} | 耗时: {time.time() - start:.4f}s")
    return label
过滤后识别结果='0'
count=0
def yolo过滤器(label):
    global count,过滤后识别结果
    if label==过滤后识别结果:
        count += 1
    else:
        过滤后识别结果=label
        count=1
    if count>=2:
        return 过滤后识别结果
    else:
        return 0

def yolo页面检测主函数():
    ll=yolo页面识别()
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
def ui变化检测(标识符,timeout=2,interval=0.1):
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


def hsv模板匹配(template_path, hsv_lower, hsv_upper, threshold=0.85):
    """
    复合检测函数：先 HSV 掩膜过滤，再进行模板匹配
    :param template_path: 模板图片路径
    :param hsv_lower: HSV下限 (np.array)
    :param hsv_upper: HSV上限 (np.array)
    :param threshold: 匹配置信度阈值
    :return: 匹配成功返回 True, 否则返回 False
    """
    # 1. 加载模板
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"警告：无法加载模板 {template_path}")
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
    # print(f"DEBUG: 匹配度 {max_val:.4f}")

    return max_val >= threshold
def 战斗场景检测():
    battle_hsv_min = np.array([0, 0, 244])  # 根据你的实际场景设置
    battle_hsv_max = np.array([179, 8, 255])
    战斗场景检测=hsv模板匹配(r'C:\Users\ZhuanZ1\Desktop\rpa\zhanshuangfuben\ziyuanwenjian\biaoshi\img_18.png',battle_hsv_min,battle_hsv_max)
    if 战斗场景检测:
        return True
    else:
        return False
def 获取可用关卡坐标(img, boxes, threshold=0.85):
    """
    遍历每个 box，如果该区域在所有 STATUS_CONFIG 中都匹配不到，则认为是目标坐标
    """
    print(f'检测到的关卡数量{len(boxes)}')
    for box in boxes:
        x1, y1, x2, y2 = map(int, box)
        roi = img[max(0, y1):min(img.shape[0], y2), max(0, x1):min(img.shape[1], x2)]
        if roi.size == 0: continue

        roi_hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

        is_occupied = False  # 标记该区域是否被占用（即匹配到了某种已知状态）

        # 遍历所有已知状态进行排查
        for state, data in LOADED_TEMPLATES.items():
            hsv_lower, hsv_upper = data['hsv_range']
            template_gray = data['gray']

            # 1. 颜色过滤
            mask = cv2.inRange(roi_hsv, hsv_lower, hsv_upper)

            # 2. 只有当 mask 中有一定数量的像素（避免掩码为空导致模板匹配失效）才进行匹配
            if cv2.countNonZero(mask) > 100:
                masked_roi = cv2.bitwise_and(roi_gray, roi_gray, mask=mask)
                res = cv2.matchTemplate(masked_roi, template_gray, cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                print(f'关卡通关标识符匹配度{max_val}')
                if max_val >= threshold:
                    is_occupied = True
                    break  # 匹配到了一个状态，直接跳出该区域的检测

        # 如果遍历完所有状态都没有匹配到，说明该区域是“空的”或者“可挑战的”
        if not is_occupied:
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            return (center_x, center_y)

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
            if cv2.countNonZero(mask) > 100:
                masked_roi = cv2.bitwise_and(roi_gray, roi_gray, mask=mask)
                res = cv2.matchTemplate(masked_roi, data['gray'], cv2.TM_CCOEFF_NORMED)
                _, max_val, _, _ = cv2.minMaxLoc(res)
                if max_val >= threshold:
                    is_occupied = True
                    break

        # 将未被匹配到的（未通关）存入候选
        if not is_occupied:
            uncompleted_candidates.append({
                'center': ((x1 + x2) // 2, (y1 + y2) // 2),
                'x2': x2
            })

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


def 未通关章节定位():
    '''
    遍历判断，直到定位到没有通关标识的章节
    '''
    滑动次数 = 0  # 初始化计数器

    while True:
        通关标志 = 图像是否存在('ziyuanwenjian/biaoshi/img_16.png')

        if 通关标志:
            # 执行左滑
            d.swipe_ext("left", scale=0.2)
            滑动次数 += 1  # 计数加 1
            print(f"检测到通关标志，已累计向左滑动 {滑动次数} 次")
            time.sleep(1)

            # 当滑动满 7 次时触发
            if 滑动次数 == 7:
                print("已满 7 次，执行点击动作...")

                # 执行点击（请替换为你的实际目标坐标）
                下一章ui = (138, 963)
                下一章ui = 坐标随机(下一章ui, left=120, right=120, up=15, down=15)
                adb_click(下一章ui)
                time.sleep(0.6)

                # 【核心修改】：重置计数器，不退出，让 while 循环继续重复执行
                滑动次数 = 0
                print("点击完成，重置计数，继续当前函数循环...")

        else:
            # 如果没检测到通关标志，说明找到了未通关章节，退出循环
            print("未检测到通关标志，已定位到未通关章节。")
            break


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


def 消球检测(img):
    BALL_COLORS = {
        # "红黄": {"lower": np.array([0, 165, 175]), "upper": np.array([179, 191, 236])},
        # "蓝色": {"lower": np.array([107, 92, 144]), "upper": np.array([119, 203, 232])},
        "红黄蓝": {"lower": np.array([0, 0, 210]), "upper": np.array([179, 38, 255])}
    }
    dict_a = [(2447, 1013), (2228, 1013)]

    # img = cv2.imread('adbxi.png')
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for index, (pt_x, pt_y) in enumerate(dict_a):
        # 截取采样区域 (±65像素)
        sample = hsv_img[pt_y - 20:pt_y + 20, pt_x - 20:pt_x + 20]

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


def 战斗主函数():
    empty_count = 0
    while True:
        start_time = time.perf_counter()
        img = 截图()
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        # print(f'截图耗时：【{elapsed_time}】')
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
            # print('普攻')
            # 控制全局节奏，防止操作过快导致卡顿
            time.sleep(0.1)
            # end_time = time.perf_counter()
            # elapsed_time = end_time - start_time
            # print(f'循环一次耗时：【{elapsed_time}】')
        except Exception as e:
            print(f"战斗发生异常: {e}")
            time.sleep(1)


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



if __name__ == '__main__':
    未通关章节定位()