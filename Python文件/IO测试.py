import sys
import os

if hasattr(sys, '_MEIPASS'):
    # 如果进到这里，说明【当前是 EXE 运行状态】
    项目根目录路径 = sys._MEIPASS
else:
    # 如果进到这里，说明【当前是 LOCAL 本地运行状态】
    项目根目录路径 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(项目根目录路径)