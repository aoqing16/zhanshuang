import os

# 获取脚本运行路径
运行路径 = os.path.abspath(__file__)
上级目录 = os.path.dirname(运行路径)
项目根目录路径 = os.path.dirname(上级目录)
标识符文件夹路径=os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi')
配置文件路径=os.path.join(项目根目录路径, 'Python文件','config.py')
图片标识符清单={
    "普通剧情":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_26.png'),
    "普通剧情按钮":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_25.png'),
    "隐藏剧情按钮":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_27.png'),
    "作战失败":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_30.png'),
    "终点标识符":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_31.png'),
    "战斗标识符":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_18.png'),
    "副本-战斗对话页":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_32.png'),
    "副本-意识重启":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_34.png'),
    "副本-战斗交互":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_37.png'),

}
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
终点标识符hsv范围lower=[126,8,206]
终点标识符hsv范围upper=[179,39,255]
血条hsv范围lower=[0,0,254]
血条hsv范围upper=[179,1,255]
血条roi=[802,86,1763,117]
副本_战斗对话页hsv范围lower=[0,0,255]
副本_战斗对话页hsv范围upper=[179,3,255]
副本_战斗交互hsv范围lower=[0,0,165]
副本_战斗交互hsv范围upper=[51,6,234]
章节黑名单["随机章节-3174-img_33"] = os.path.join(项目根目录路径, "ziyuanwenjian", "biaoshi", "img_33.png")

章节黑名单["随机章节-6930-img_35"] = os.path.join(项目根目录路径, "ziyuanwenjian", "biaoshi", "img_35.png")

章节黑名单["随机章节-4687-img_36"] = os.path.join(项目根目录路径, "ziyuanwenjian", "biaoshi", "img_36.png")
