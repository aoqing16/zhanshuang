import os
import sys
import json

项目根目录路径= os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ziyuanwenjian", "config.json")

def load_my_config():
    with open(json_path, "r", encoding="utf-8") as f:
        config_data = json.load(f)
    return config_data

json_data = load_my_config()
章节黑名单路径=json_data.get('章节黑名单')
章节黑名单绝对路径字典 = {
    key: os.path.join(项目根目录路径, value.replace("/", os.sep))
    for key, value in 章节黑名单路径.items()
}

# ==================== 🛠️ 测试输出 ====================
print(章节黑名单绝对路径字典)
