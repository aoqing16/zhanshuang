import os

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

def 图像_hsv过滤并保存(输入图片, 输出图片, file_name="hsv_filtered.png", mode="mask"):
    """
    对指定图片进行 HSV 颜色过滤并保存结果。 (全面兼容 Windows 中文路径)

    参数:
    ----------
    img_path : str
        原彩色图片路径
    hsv_lower : list 或 np.array
        HSV 三通道下限, 例如 [35, 43, 46] (绿色的下限)
    hsv_upper : list 或 np.array
        HSV 三通道上限, 例如 [77, 255, 255] (绿色的上限)
    save_dir : str
        保存结果的文件夹路径
    file_name : str
        保存的文件名，默认 'hsv_filtered.png'
    mode : str
        "mask" : 只保存黑白掩膜图 (符合条件的区域为纯白，其余为纯黑)
        "res"  : 保存过滤后的彩色提取图 (保留符合条件的彩色区域，其余变纯黑)
    """
    try:
        # 1. 采用二进制流方式读取图片，完美解决 Windows 中文路径 Bug
        img_bgr = cv2.imdecode(np.fromfile(输入图片, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img_bgr is None:
            print(f"❌ 图片读取失败，请检查路径是否存在: {输入图片}")
            return False

        # 2. 转换颜色空间到 HSV
        img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

        # 3. 确保 lower 和 upper 是符合 OpenCV 要求的 numpy 数组
        my_lower = [35, 43, 46]
        my_upper = [77, 255, 255]
        lower_arr = np.array(my_lower, dtype=np.uint8)
        upper_arr = np.array(my_upper, dtype=np.uint8)

        # 4. 创建二值化掩膜 (Mask)
        mask = cv2.inRange(img_hsv, lower_arr, upper_arr)

        # 5. 根据模式决定输出画面
        if mode == "mask":
            # 纯黑白轮廓，用于直接观察像素点是否达到 100 门槛
            output_img = mask
        elif mode == "res":
            # 扣出原图色彩，方便肉眼分辨是否把多余的杂色也扣进来了
            output_img = cv2.bitwise_and(img_bgr, img_bgr, mask=mask)
        else:
            print("❌ 未知的保存模式，请选择 'mask' 或 'res'")
            return False

        # 6. 安全创建输出文件夹并以二进制流保存，防止中文路径报错
        if not os.path.exists(输出图片):
            os.makedirs(输出图片)

        save_path = os.path.join(输出图片, file_name)
        ext = os.path.splitext(file_name)[1]  # 自动提取扩展名 (.png 或 .jpg)

        _, img_encode = cv2.imencode(ext, output_img)
        img_encode.tofile(save_path)

        print(f"🟩 [HSV过滤完成] 模式: {mode} | 成功保存至: {save_path}")
        return True

    except Exception as e:
        print(f"❌ HSV 过滤执行期间发生异常: {e}")
        return False


# ====== 🔍 快速调试运行 ======
if __name__ == "__main__":
    # 替换成你真实的图片路径和想存放的路径
    IMAGE_PATH = r"C:\Users\ZhuanZ1\Desktop\rpa\dataset\yolo图像分类模型数据集\train\副本-战斗页\20260604_164511_92b84f.png"
    OUTPUT_DIR = r"C:\Users\ZhuanZ1\Desktop\rpa\dataset\hsv_debug_out"
    # 运行测试 1：保存彩色提取结果
    图像_hsv过滤并保存(IMAGE_PATH,OUTPUT_DIR, "green_result.png")
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
    hsv实时预览()