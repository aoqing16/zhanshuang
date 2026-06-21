import os
import sys
import time
import shutil
import subprocess
import uiautomator2 as u2


def 获取ADB可执行路径():
    """（就是你刚刚测试成功的函数）"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, '_internal', 'adbutils', 'binaries', 'adb.exe')
    else:
        try:
            import adbutils
            if hasattr(adbutils, 'adb_path'):
                return adbutils.adb_path()
        except Exception:
            pass
        return shutil.which("adb") or "adb"


# 🧱【核心核心】拿到路径后，用它来实现傻瓜式连接
def 自动连接战双模拟器():
    # 1. 成功接住你刚刚获取到的 adb 路径
    adb_cmd = 获取ADB可执行路径()
    print(f"📡 成功锁定 ADB 核心组件，路径: {adb_cmd}")

    print("🔄 正在初始化 ADB 后台服务...")
    # 2. 强行启动 ADB 服务（用双引号把路径包起来，防止路径里有空格报错）
    subprocess.run(f'"{adb_cmd}" start-server', shell=True, capture_output=True)

    # 3. 🎯 盲撞唤醒：把市面上最常见的几个默认端口全部 connect 一遍
    # 这一步能把那些“隐身/没反应”的模拟器强行拉上线
    常见端口 = [5554, 5555, 16384, 21503, 62001]
    print("🕵️ 正在全盘扫描并唤醒本地模拟器通道...")
    for port in 常见端口:
        subprocess.run(f'"{adb_cmd}" connect 127.0.0.1:{port}', shell=True, capture_output=True)

    # 给系统和模拟器 0.5 秒的反应时间
    time.sleep(0.5)

    # 4. 精准收网：抓取当前所有真正连接成功的设备列表
    try:
        result = subprocess.run(f'"{adb_cmd}" devices', shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')
    except Exception as e:
        print(f"❌ 读取设备列表失败: {e}")
        return None

    # 5. 解析设备列表，把真正合法的地址挑出来
    活跃设备清单 = []
    for line in lines[1:]:  # 跳过第一行 "List of devices attached"
        if 'device' in line and 'unauthorized' not in line:
            地址 = line.split()[0]
            活跃设备清单.append(地址)

    # 6. 🧠 智能分流决策
    设备数量 = len(活跃设备清单)

    if 设备数量 == 0:
        print("\n❌ [错误] 翻遍了电脑，没发现任何运行中的模拟器！")
        print("💡 解决方案：请先打开你的雷电或MuMu模拟器，然后再运行本测试。")
        return None

    elif 设备数量 == 1:
        # ✨ 针对 95% 的情况：单开无感秒连
        目标地址 = 活跃设备清单[0]
        print(f"\n🎉 [唯一匹配] 成功锁定模拟器通道: {目标地址}")
        print("🚀 正在为您建立 `uiautomator2` 战斗连接...")
        try:
            # 🌟【大结局】拿着抓到的地址，直接塞给 u2 连上！
            d = u2.connect(目标地址)
            return d
        except Exception as e:
            print(f"❌ 建立连接失败: {e}")
            return None

    else:
        # ✨ 针对多开党：交出选择权，做个清晰直观的菜单
        print("\n⚠️ [多开检测] 侦测到您的电脑同时运行了多个模拟器窗口：")
        print("-" * 45)
        for 序号, 地址 in enumerate(活跃设备清单):
            类型 = "雷电默认" if "5554" in 地址 else ("网易MuMu" if "16384" in 地址 else "其他多开")
            print(f" 🌟 [{序号}]  地址: {地址}  ({类型})")
        print("-" * 45)

        while True:
            选择 = input("👉 请输入前方方括号内的数字选择你要挂战双的窗口: ").strip()
            if 选择.isdigit() and int(选择) < 设备数量:
                目标地址 = 活跃设备清单[int(选择)]
                break
            print("❌ 输入有误，请确认输入数字是否正确！")

        print(f"\n🚀 正在对接您选定的模拟器: {目标地址} ...")
        return u2.connect(目标地址)


# ==================== 🎬 开始运行测试 ====================
if __name__ == "__main__":
    # 执行连接并用变量 d 接住它
    d = 自动连接战双模拟器()

    if d:
        print('已成功连接到模拟器，正在启动脚本')

        # 接下来你就可以像以前一样，用这个 d 去做任何事了，比如：
        # d(text="战双帕弥什").click()