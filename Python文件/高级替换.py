import os
import re


def quick_replace_coordinates(file_path, context_lines=3):
    """
    context_lines: 向上和向下延伸的行数。设置为 3 代表一共展示 7 行代码
    """
    if not os.path.exists(file_path):
        print(f"错误：找不到文件 {file_path}")
        return

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    # 正则表达式：匹配 2 到 4 位数的独立数字
    pattern = re.compile(r"\b\d{2,4}\b")

    # 找出所有匹配的数字及其实际所在的行索引 (0-based)
    matches_with_index = []
    seen = set()

    for m in pattern.finditer(content):
        num = m.group()
        # 找出该字符在第几行
        line_no = content[:m.start()].count("\n")

        # 为了高效，同一行里相同的数字不要重复询问
        key = (num, line_no)
        if key not in seen:
            seen.add(key)
            matches_with_index.append((num, line_no))

    if not matches_with_index:
        print("未在文件中找到符合条件的 2-4 位数字。")
        return

    print(f"🎯 扫描完毕！共找到 {len(matches_with_index)} 处待处理的数字。")
    print("-" * 60)

    # 用来记录每一行最终被修改成什么样
    # key: 行号, value: 该行代码的内容
    modified_lines = list(lines)

    for index, (num, target_line_idx) in enumerate(matches_with_index, 1):
        print("\n" + "=" * 60)
        print(f"[{index}/{len(matches_with_index)}] 正在处理数字: \033[1;31m{num}\033[0m (第 {target_line_idx + 1} 行)")
        print("-" * 60)

        # --- 计算长上下文的范围 ---
        start_idx = max(0, target_line_idx - context_lines)
        end_idx = min(len(lines), target_line_idx + context_lines + 1)

        # 打印长上下文
        for i in range(start_idx, end_idx):
            # 获取最新的代码行内容（包含之前已经替换好的部分）
            current_line_content = modified_lines[i]

            # 如果是当前正在处理的目标行，加一根特征箭头并高亮数字
            if i == target_line_idx:
                # 仅高亮独立的数字词，防止把含有该数字的其他代码也错染成红色
                highlighted_line = re.sub(r"\b" + num + r"\b", f"\033[1;31m{num}\033[0m", current_line_content)
                print(f"\033[1;33m👉 {i + 1:<4}\033[0m | {highlighted_line}")
            else:
                # 其他上下文行弱化显示
                print(f"   {i + 1:<4} | {current_line_content}")

        print("-" * 60)
        print("请选择替换选项:")
        print(f"  [1] -> x相对坐标({num})")
        print(f"  [2] -> y相对坐标({num})")
        print("  [3] -> 跳过此数字 (直接回车也是跳过)")

        choice = input("请输入编号 (1/2/3): ").strip()

        if choice == "1":
            # 仅替换当前行中符合独立边界的数字
            old_line = modified_lines[target_line_idx]
            new_line = re.sub(r"\b" + num + r"\b", f"x相对坐标({num})", old_line)
            modified_lines[target_line_idx] = new_line
            print(f"✅ 已替换第 {target_line_idx + 1} 行的 {num}")
        elif choice == "2":
            old_line = modified_lines[target_line_idx]
            new_line = re.sub(r"\b" + num + r"\b", f"y相对坐标({num})", old_line)
            modified_lines[target_line_idx] = new_line
            print(f"✅ 已替换第 {target_line_idx + 1} 行的 {num}")
        else:
            print(f"⏭️ 已跳过该处数字")

    # 拼接最终修改后的代码
    final_content = "\n".join(modified_lines)

    # 自动备份原文件
    backup_path = file_path + ".bak"
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(content)

    # 写入新文件
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_content)

    print("\n" + "=" * 60)
    print("🎉 替换大功告成！")
    print(f"📦 原文件已安全备份至: {backup_path}")
    print(f"🚀 修改后的长上下文代码已写入: {file_path}")


# --- 运行测试 ---
if __name__ == "__main__":
    # ⚠️ 填入你脚本的路径
    目标文件 = r"C:\Users\ZhuanZ1\Desktop\rpa\zhanshuangfuben\Python文件\函数资源.py"

    # context_lines=4 代表目标数字的上面打印4行，下面打印4行，总共显示9行
    quick_replace_coordinates(目标文件, context_lines=4)