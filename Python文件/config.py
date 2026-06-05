import os

# 获取脚本运行路径
运行路径 = os.path.abspath(__file__)
上级目录 = os.path.dirname(运行路径)
# print(上级目录)
项目根目录路径 = os.path.dirname(上级目录)
# print(f'项目根目录路径：{项目根目录路径}')
# ziyuanwenjian/biaoshi/img_20.png
章节标签黑名单 = {
    "升格": os.path.join(项目根目录路径, "ziyuanwenjian",'biaoshi','img_21.png'),
}
章节标签roi=[0,694,404,760]
章节黑名单 = {
    "升格-苦行之旅": os.path.join(项目根目录路径, "ziyuanwenjian",'biaoshi','img_20.png'),
    "升格-终末预览": os.path.join(项目根目录路径, "ziyuanwenjian",'biaoshi','img_22.png'),
}
章节roi = [556, 956, 1943, 1158]
# print(章节标签黑名单)
血条hsv范围lower=[0,0,254]
血条hsv范围upper=[179,1,255]
血条roi=[802,86,1763,117]