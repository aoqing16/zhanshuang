import uiautomator2 as u2
import cv2
import numpy as np
import os
import uuid
import keyboard
import time
# 1. 连接设备
d = u2.connect('127.0.0.1:16384')
def 截图():
    img = d.screenshot(format='opencv')
    return img


def 单次截图并保存固定名():
    img = d.screenshot(format='opencv')
    cv2.imwrite('adb.png', img)
def hsv过滤截图():


    # 1. 获取截图
    img = 截图()

    # 2. 定义 HSV 范围 (示例，请根据实际调试结果调整)
    hsv_lower = np.array([0, 0, 251])
    hsv_upper = np.array([179, 27, 255])

    # 3. 进行 HSV 过滤
    # 转换到 HSV 色彩空间
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 创建掩码 (符合范围的像素为 255，否则为 0)
    mask = cv2.inRange(hsv_img, hsv_lower, hsv_upper)

    # 4. 使用掩码进行过滤
    # bitwise_and 将原图与掩码重叠，只有 mask 中白色 (255) 对应的区域保留原色彩，其余变为黑色
    filtered_img = cv2.bitwise_and(img, img, mask=mask)

    # 5. 写入过滤后的图片
    cv2.imwrite('adbxi.png', filtered_img)


def 单次截屏并保存随机名():
    save_dir = "screenshots"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    img = 截图()
    random_filename = f"{uuid.uuid4()}.png"

    # 3. 拼接完整路径
    save_path = os.path.join(save_dir, random_filename)
    cv2.imwrite(save_path, img)
    print(f'已保存：: {save_path}')

 
def setup_manual_screenshot(capture_func, save_dir="screenshots"):
    # hh
    """
    配置手动截图功能
    :param capture_func: 你原本的截图函数 (例如 d.screenshot)
    :param save_dir: 保存路径
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    def _trigger():
        # 执行截图
        img = capture_func()
        if img is None:
            print("截图失败：未获取到图像")
            return

        # 生成唯一文件名
        filename = f"{time.strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}.png"
        save_path = os.path.join(save_dir, filename)

        cv2.imwrite(save_path, img)
        print(f"[{time.strftime('%H:%M:%S')}] 已保存截图: {save_path}")

    # 绑定空格键
    keyboard.add_hotkey('space', _trigger)
    print(f"[*] 手动截图功能已启动 (保存目录: {save_dir})")
    print("[*] 按下 [空格键] 进行截屏")

def 监听按键截图():
    setup_manual_screenshot(截图)

    # 保持主程序运行
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        keyboard.unhook_all()
if __name__ == '__main__':
    hsv过滤截图()
    # keyboard.add_hotkey('space', 截图触发逻辑)
    # pass
