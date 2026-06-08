import os
import random
import cv2
import numpy as np


def 原尺寸灰度底图色彩叠加合成(bg_path, target_path, save_dir, index):
    """读取彩色背景图转为灰度，

    然后保持目标图（Alpha通道）的原始像素尺寸，1:1随机位置叠加上去。
    """
    try:
        # 1. 以二进制流读取，兼容中文路径
        bg_rgb = cv2.imdecode(
            np.fromfile(bg_path, dtype=np.uint8), cv2.IMREAD_COLOR
        )
        target_rgba = cv2.imdecode(
            np.fromfile(target_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED
        )

        if bg_rgb is None or target_rgba is None:
            print(f"❌ 图片读取失败，请检查路径")
            return

        # 2. 将底图转为灰度
        bg_gray_single = cv2.cvtColor(bg_rgb, cv2.COLOR_BGR2GRAY)
        bg_gray_3channel = cv2.cvtColor(bg_gray_single, cv2.COLOR_GRAY2BGR)

        bg_h, bg_w = bg_gray_3channel.shape[:2]

        # 3. 🌟 关键修改：直接获取抠图的原始宽高，绝不进行 resize 缩放
        t_h, t_w = target_rgba.shape[:2]

        # 防御性代码：如果贴图比背景还大（通常不会），进行安全拦截
        if t_h > bg_h or t_w > bg_w:
            print(
                f"⚠️ 警告：贴图尺寸({t_w}x{t_h})大于背景尺寸({bg_w}x{bg_h})，跳过此张。"
            )
            return

        # 4. 随机生成放置坐标（确保原尺寸目标完全在背景内部）
        x = random.randint(0, bg_w - t_w)
        y = random.randint(0, bg_h - t_h)

        # 5. Alpha 通道彩色与灰度矩阵无损融合
        target_bgr = target_rgba[:, :, :3]
        alpha = target_rgba[:, :, 3] / 255.0

        roi = bg_gray_3channel[y: y + t_h, x: x + t_w]

        for c in range(0, 3):
            roi[:, :, c] = (
                    target_bgr[:, :, c] * alpha + roi[:, :, c] * (1.0 - alpha)
            ).astype(np.uint8)

        bg_gray_3channel[y: y + t_h, x: x + t_w] = roi

        # 6. 保存最终合成图
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        save_path = os.path.join(save_dir, f"gray_bg_synth_{index:05d}.jpg")

        _, img_encode = cv2.imencode(".jpg", bg_gray_3channel)
        img_encode.tofile(save_path)
        print(f"🟩 [原尺寸成功] 已生成: {save_path}")

    except Exception as e:
        print(f"❌ 第 {index} 张图合成异常: {e}")
TEST_BG = r"C:\Users\ZhuanZ1\Desktop\rpa\zhanshuangfuben\ziyuanwenjian\biaoshi\20260604_164511_92b84f.png"  # 你的彩色副本截图
TEST_TARGET = r"C:\Users\ZhuanZ1\Downloads\20260607_175434_d122f8.png"  # 你刚抠出来的透明底神图
OUTPUT_FOLDER = "./train_data/class_endpoint"
原尺寸灰度底图色彩叠加合成(TEST_BG, TEST_TARGET, OUTPUT_FOLDER,index=1)