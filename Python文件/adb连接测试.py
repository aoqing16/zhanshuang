import subprocess
import re


def auto_find_mumu_device():
    # MuMu 12 经常使用的 ADB 端口就是 16384
    # 我们可以通过查找这个端口是否被占用，来确认模拟器是否在线
    cmd = "netstat -ano | findstr 16384"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if "LISTENING" in result.stdout:
        print("发现 MuMu 模拟器正在监听 16384 端口")
        return "127.0.0.1:16384"
    else:
        print("未发现模拟器运行，请先启动 MuMu")
        return None


# 连接时直接调用
device_addr = auto_find_mumu_device()
if device_addr:
    import uiautomator2 as u2

    d = u2.connect(device_addr)
    print(d.info)