import os
import sys

# 获取脚本运行路径

if hasattr(sys, '_MEIPASS'):
    # 如果进到这里，说明【当前是 EXE 运行状态】
    项目根目录路径 = sys._MEIPASS
    # 示例："C:\Users\ZhuanZ1\Desktop\rpa\zhanshuangfuben\dist\文件夹测试名\_internal"
else:
    # 如果进到这里，说明【当前是 LOCAL 本地运行状态】
    项目根目录路径 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     示例：C:\Users\ZhuanZ1\Desktop\rpa\zhanshuangfuben
print(项目根目录路径)
标识符文件夹路径=os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi')
json配置文件路径=os.path.join(项目根目录路径, "ziyuanwenjian", "config.json")
yolo模型路径={"分类模型": os.path.join(项目根目录路径, "model", '分类模型.pt'),
            "目标检测模型": os.path.join(项目根目录路径, "model", '目标检测模型.pt'),
            "地标检测模型": os.path.join(项目根目录路径, "model", '1.pt'),

}
# print(yolo模型路径)
图片标识符清单={
    "普通剧情":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_26.png'),
    "战斗副本弹窗_速通模式按键":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img.png'),
    "章节_通关标志":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_16.png'),
    "青绿标识符":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_11.png'),
    "红色标识符":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_19.png'),
    "首个章节标签":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_15.png'),
    "普通剧情按钮":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_25.png'),
    "隐藏剧情按钮":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_27.png'),
    "作战失败":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_30.png'),
    "终点标识符":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_31.png'),
    "战斗标识符":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_18.png'),
    "副本-战斗对话页":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_32.png'),
    "副本-意识重启":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_34.png'),
    "副本-战斗交互":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_37.png'),
    "副本-剧情对话页跳过":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_49.png'),
    "副本-战斗结算":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_50.png'),
    "副本-战斗副本弹窗后期副本":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_58.png'),
    "副本-战斗副本弹窗前期副本":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_13.png'),
    "战后结算":os.path.join(项目根目录路径, "ziyuanwenjian", 'UI','img_6.png'),
    "副本-剧情副本弹窗_前期":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_6.png'),
    "副本-剧情副本弹窗_后期":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_59.png'),
    "上阵英雄":os.path.join(项目根目录路径, "ziyuanwenjian", 'UI','img_2.png'),
    "副本_返回":os.path.join(项目根目录路径, "ziyuanwenjian", 'UI','img_10.png'),
    "上阵英雄的+号":os.path.join(项目根目录路径, "ziyuanwenjian", 'UI','img_2.png'),
    "编入队伍":os.path.join(项目根目录路径, "ziyuanwenjian", 'UI','img_9.png'),
    "作战开始":os.path.join(项目根目录路径, "ziyuanwenjian", 'UI','img_3.png'),
    "剧情跳过提示":os.path.join(项目根目录路径, "ziyuanwenjian", 'UI','img_5.png'),
    "战斗副本弹窗_速通开关":os.path.join(项目根目录路径, "ziyuanwenjian", 'UI','img_1.png'),
    "撤退":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_23.png'),
    "撤退_确定":os.path.join(项目根目录路径, "ziyuanwenjian", 'biaoshi','img_24.png'),

}

章节标签roi=[0,694,404,760]
章节roi = [556, 956, 1943, 1158]
# print(章节黑名单)
终点标识符hsv范围lower=[126,8,206]
终点标识符hsv范围upper=[179,39,255]
血条hsv范围lower=[0,0,254]
血条hsv范围upper=[179,1,255]
血条roi=[802,86,1763,117]
怪物名hsv范围lower = [0, 0, 243]
怪物名hsv范围upper = [179, 4, 255]
怪物名roi=[827,24,1752,92]
副本_战斗对话页hsv范围lower=[0,0,255]
副本_战斗对话页hsv范围upper=[179,3,255]
副本_战斗交互hsv范围lower=[0,0,165]
副本_战斗交互hsv范围upper=[51,6,234]
副本_剧情对话页跳过hsv范围lower=[0,0,251]
副本_剧情对话页跳过hsv范围upper=[179,27,255]
副本_战斗结算hsv范围lower = [0, 0, 251]
副本_战斗结算hsv范围upper = [179, 27, 255]
