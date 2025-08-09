from argparse import ArgumentParser, Action
import json


class JsonAction(Action):
    """将输入的 JSON 字符串解析为 Python 对象"""

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            parsed_json = json.loads(values)
            setattr(namespace, self.dest, parsed_json)
        except json.JSONDecodeError as e:
            parser.error(f"无效的 JSON 格式: {e}")


class RangeAction(Action):
    """验证数字是否在指定范围内"""

    def __init__(self, option_strings, dest, min_val=None, max_val=None, **kwargs):
        self.min_val = min_val
        self.max_val = max_val
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        try:
            num = int(values)
            if self.min_val is not None and num < self.min_val:
                parser.error(f"值 {num} 小于最小值 {self.min_val}")
            if self.max_val is not None and num > self.max_val:
                parser.error(f"值 {num} 大于最大值 {self.max_val}")
            setattr(namespace, self.dest, num)
        except ValueError:
            parser.error(f"'{values}' 不是有效的整数")


parser = ArgumentParser()

parser.add_argument("--json", action=JsonAction, help="输入 JSON 字符串")
parser.add_argument(
    "--score", action=RangeAction, min_val=0, max_val=100, help="输入 0-100 之间的分数"
)

args = parser.parse_args()

if args.json:
    print(f"解析的 JSON: {args.json}")
    print(f"类型: {type(args.json)}")

if args.score is not None:
    print(f"分数: {args.score}")
