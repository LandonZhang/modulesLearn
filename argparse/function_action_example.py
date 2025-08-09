from argparse import ArgumentParser


def validate_and_process(value):
    """自定义处理函数"""
    try:
        num = int(value)
        if num < 0:
            raise ValueError("数字必须为正数")
        return num * 2  # 将输入值翻倍
    except ValueError as e:
        raise ValueError(f"无效输入: {e}")


parser = ArgumentParser()

# 使用 type 参数指定自定义处理函数
parser.add_argument(
    "--number", type=validate_and_process, help="输入一个正整数，会自动翻倍"
)

args = parser.parse_args()

if args.number:
    print(f"处理后的数字: {args.number}")
