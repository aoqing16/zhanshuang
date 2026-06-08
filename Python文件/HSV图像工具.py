import cv2
import numpy as np
from Python文件.函数资源 import 截图

def nothing(x):
    pass

def hsv实时预览():
    """
    实时过滤并预览图像
    :param capture_func: 一个返回当前截图（numpy array, BGR格式）的函数
    """
    window_name = 'HSV Filter Preview'
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)  # 可调大小窗口

    # 创建滑动条 (Hue: 0-179, Saturation: 0-255, Value: 0-255)
    cv2.createTrackbar('Low H', window_name, 0, 179, lambda x: None)
    cv2.createTrackbar('Low S', window_name, 0, 255, lambda x: None)
    cv2.createTrackbar('Low V', window_name, 0, 255, lambda x: None)
    cv2.createTrackbar('High H', window_name, 179, 179, lambda x: None)
    cv2.createTrackbar('High S', window_name, 255, 255, lambda x: None)
    cv2.createTrackbar('High V', window_name, 255, 255, lambda x: None)

    print("按 'q' 键退出程序")

    while True:
        # 1. 获取截图
        frame = 截图()
        if frame is None: continue

        # 2. 读取滑动条位置
        lh = cv2.getTrackbarPos('Low H', window_name)
        ls = cv2.getTrackbarPos('Low S', window_name)
        lv = cv2.getTrackbarPos('Low V', window_name)
        hh = cv2.getTrackbarPos('High H', window_name)
        hs = cv2.getTrackbarPos('High S', window_name)
        hv = cv2.getTrackbarPos('High V', window_name)

        # 3. 转换色彩空间并进行掩膜处理
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_bound = np.array([lh, ls, lv])
        upper_bound = np.array([hh, hs, hv])
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        # 将掩膜结果与原图结合
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # 4. 显示预览
        cv2.imshow(window_name, result)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

def hsv过滤():
    # 1. 读取图片
    img_path = r"C:\Users\ZhuanZ1\Desktop\rpa\dataset\yolo图像分类模型数据集\train\副本-意识重启\20260607_175209_d604aa - 副本.png"  # 请确保图片文件路径正确
    image = cv2.imread(img_path)
    # image=截图()
    if image is None:
        print(f"错误：无法找到图片 {img_path}，请检查路径。")
        exit()

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 2. 创建窗口，设置可缩放
    cv2.namedWindow('HSV Detector', cv2.WINDOW_NORMAL)
    cv2.namedWindow('Result', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('HSV Detector', 640, 480)
    cv2.resizeWindow('Result', 640, 480)

    # 3. 创建滑动条
    cv2.createTrackbar('H Min', 'HSV Detector', 0, 179, nothing)
    cv2.createTrackbar('H Max', 'HSV Detector', 179, 179, nothing)
    cv2.createTrackbar('S Min', 'HSV Detector', 0, 255, nothing)
    cv2.createTrackbar('S Max', 'HSV Detector', 255, 255, nothing)
    cv2.createTrackbar('V Min', 'HSV Detector', 0, 255, nothing)
    cv2.createTrackbar('V Max', 'HSV Detector', 255, 255, nothing)

    print("--- 调试器已启动 ---")
    print("1. 调整滑动条以选取颜色。")
    print("2. 窗口支持鼠标拖动缩放。")
    print("3. 按 'q' 键退出程序并查看最终参数。")

    while True:
        # 获取当前滑动条数值
        h_min = cv2.getTrackbarPos('H Min', 'HSV Detector')
        h_max = cv2.getTrackbarPos('H Max', 'HSV Detector')
        s_min = cv2.getTrackbarPos('S Min', 'HSV Detector')
        s_max = cv2.getTrackbarPos('S Max', 'HSV Detector')
        v_min = cv2.getTrackbarPos('V Min', 'HSV Detector')
        v_max = cv2.getTrackbarPos('V Max', 'HSV Detector')

        # 定义范围
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])

        # 颜色掩膜计算
        mask = cv2.inRange(hsv, lower, upper)

        # 将掩膜应用到原图
        result = cv2.bitwise_and(image, image, mask=mask)

        # 显示图像
        cv2.imshow('HSV Detector', mask)
        cv2.imshow('Result', result)

        # 按 q 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("\n--- 最终参数 ---")
            print(f"Lower Bound: {list(lower)}")
            print(f"Upper Bound: {list(upper)}")
            break

    cv2.destroyAllWindows()
if __name__ == '__main__':
    hsv过滤()