import os

运行路径 = os.path.abspath(__file__)
print(运行路径)
文件根目录路径 = os.path.dirname(运行路径)
print(文件根目录路径)
文件根目录路径 = os.path.dirname(文件根目录路径)
print(文件根目录路径)
文件根目录路径 = os.path.dirname(文件根目录路径)
print(文件根目录路径)
拼接路径=os.path.join(文件根目录路径,'Python文件','adbxixixixi.png','可以拼无数个吗？')
print(拼接路径)
