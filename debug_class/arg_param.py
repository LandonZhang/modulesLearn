"""
传统的直接调试无法传入控制台参数, 使用 args 参数可以解决此问题
1. 默认调式输出: 这是简略信息 (因为没法接收参数)
"""

from argparse import ArgumentParser, Namespace

parser = ArgumentParser()

parser.description = "测试 launch.json 中的 arg 参数添加"

parser.add_argument("-v", "--verbose", action="store_true", help="是否需要详细输出")
parser.add_argument("-num", "--numbers", help="将输入的三个数加和", nargs=3)

args = parser.parse_args()

if args.verbose:
    print("这是详细信息")
else:
    print("这是简略信息")

if args.numbers:
    numbers = [int(num) for num in args.numbers]
    print(f"三个数加和为: {sum(numbers)}")
