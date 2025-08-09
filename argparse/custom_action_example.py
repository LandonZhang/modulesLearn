from argparse import ArgumentParser, Action


# 自定义 Action 类
class CustomAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # 这里可以写你的自定义逻辑
        print(f"触发了自定义行为！参数值: {values}")
        # 可以对值进行处理
        processed_value = values.upper() if isinstance(values, str) else values
        # parser 的关键: 将输入值设为属性，使 python 运行 . 的形式访问属性
        setattr(namespace, self.dest, processed_value)  # self.dist 设定目标是谁


# 另一个例子：累加器
class AccumulateAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # 如果属性不存在，初始化为空列表
        if not hasattr(namespace, self.dest) or getattr(namespace, self.dest) is None:
            setattr(namespace, self.dest, [])
        # 将新值添加到列表中
        getattr(namespace, self.dest).append(values)


parser = ArgumentParser()

# 使用自定义 Action
parser.add_argument("--custom", action=CustomAction, help="使用自定义行为")
parser.add_argument("--collect", action=AccumulateAction, help="收集多个值")

args = parser.parse_args()

print(f"Custom 参数结果: {args.custom}")
print(f"Collect 参数结果: {args.collect}")
