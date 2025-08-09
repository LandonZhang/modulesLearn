from argparse import ArgumentParser, Namespace

# 初始化一个终端解释器
parser = ArgumentParser()

# 对这个 cli 进行说明
parser.description = "用于学习 python cli 的 cli"

# 加入一个必填参数
"""
nagrs 可以设置捕捉到 param 后面的几个输入放入 param 中
"""
# parser.add_argument("param", type=int, help="请输入一个整数", nargs=1, choices=[32, 35])

# 加入一个选填参数以及它的简化形式
"""
action 可以指定对这个参数不输入值将执行什么行为 (否则不允许单独 -v 出现)
- store_true -> 如果存在这个参数，则将参数设定为 true 值
- count -> 如果输入了多个同样的参数，返回数量 (-vv, --verbose --verbose)
"""
# parser.add_argument("-v", "--verbose", help="输出更详细的执行内容", action="store_true")
# parser.add_argument("-v", "--verbose", help="输出更详细的执行内容", action="count")

# 可以指定参数个数
# parser.add_argument("param", type=int, help="请输入两个个数，我将帮你相加", nargs=2)

# 如果有两个互斥的参数 (--verbose 和 --silence) 我们该怎么办呢
# 创建一个互斥组
group = parser.add_mutually_exclusive_group()

parser.add_argument(
    "param", type=int, help="请输入两个整数，第一个为底数，第二个为幂", nargs=2
)
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-s", "--silence", action="store_true")

# 解析到 python 中
args: Namespace = parser.parse_args()

# store_true 示例
# if args.verbose is True:
#     print(f"{args.param} 的平方是: {args.param**2}")
# else:
#     print(args.param**2)

# count 示例
# match args.verbose:
#     case 1:
#         print(f"平方结果是:{args.param**2}")
#     case 2:
#         print(f"{args.param} 的平方是: {args.param**2}")
#     case _:
#         print(args.param**2)

# args 示例
# print(args.param)  # [12, 21]
# print(type(args.param))  # list

# group 示例
if args.silence:
    print("Silenced")
elif args.verbose:
    [a, b] = args.param
    print(f"{a}的{b}次方结果是:{a**b}")
else:
    [a, b] = args.param
    print(f"{a**b}")
