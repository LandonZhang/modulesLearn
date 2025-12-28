# Python argparse 模块完全教程

## 目录

- [简介](#简介)
- [基础用法](#基础用法)
- [参数类型](#参数类型)
- [高级功能](#高级功能)
- [自定义Action](#自定义action)
- [实用技巧](#实用技巧)
- [示例代码](#示例代码)

## 简介

`argparse` 是 Python 标准库中用于处理命令行参数的模块。它可以帮你轻松创建用户友好的命令行界面，自动生成帮助信息和错误消息。

## 基础用法

### 创建解析器

```python
from argparse import ArgumentParser, Namespace

# 初始化一个命令行解析器
parser = ArgumentParser()
# 添加描述信息
parser.description = "用于学习 python cli 的工具"
```

### 添加参数

#### 位置参数（必填参数）

```python
# 添加单个必填参数
parser.add_argument("param", type=int, help="请输入一个整数")

# 添加多个必填参数
parser.add_argument("param", type=int, help="请输入两个整数，第一个为底数，第二个为幂", nargs=2)
```

#### 可选参数

```python
# 基本可选参数
parser.add_argument("-v", "--verbose", help="输出更详细的执行内容", action="store_true")

# 带计数功能的参数
parser.add_argument("-v", "--verbose", help="输出更详细的执行内容", action="count")
```

## 参数类型

### nargs 参数个数控制

- `nargs=1`：捕获 1 个参数，返回列表
- `nargs=2`：捕获 2 个参数，返回列表
- `nargs='*'`：捕获 0 个或多个参数
- `nargs='+'`：捕获 1 个或多个参数
- `nargs='?'`：捕获 0 个或 1 个参数

```python
parser.add_argument("param", type=int, help="请输入两个个数，我将帮你相加", nargs=2)
```

### choices 限制参数选择

```python
parser.add_argument("param", type=int, help="请输入一个整数", choices=[32, 35])
```

### action 参数行为控制

- `store_true`：如果存在该参数，则设为 True
- `store_false`：如果存在该参数，则设为 False
- `count`：统计参数出现次数
- `store`：存储参数值（默认行为）

```python
# store_true 示例
parser.add_argument("-v", "--verbose", action="store_true")

# count 示例 - 支持 -v, -vv, -vvv
parser.add_argument("-v", "--verbose", action="count")
```

## 高级功能

### 互斥参数组

当有两个互斥的参数时，使用 `add_mutually_exclusive_group()`：

```python
# 创建互斥组
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true")
group.add_argument("-s", "--silence", action="store_true")
```

### 参数解析和使用

```python
# 解析命令行参数
args: Namespace = parser.parse_args()

# 使用解析后的参数
if args.silence:
    print("Silenced")
elif args.verbose:
    [a, b] = args.param
    print(f"{a}的{b}次方结果是:{a**b}")
else:
    [a, b] = args.param
    print(f"{a**b}")
```

## 自定义Action

### 创建自定义Action类

```python
from argparse import Action

class CustomAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # 自定义逻辑
        print(f"触发了自定义行为！参数值: {values}")
        # 处理值
        processed_value = values.upper() if isinstance(values, str) else values
        # 设置属性
        setattr(namespace, self.dest, processed_value)
```

### 累加器Action

```python
class AccumulateAction(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # 初始化列表
        if not hasattr(namespace, self.dest) or getattr(namespace, self.dest) is None:
            setattr(namespace, self.dest, [])
        # 添加新值
        getattr(namespace, self.dest).append(values)

# 使用自定义Action
parser.add_argument("--collect", action=AccumulateAction, help="收集多个值")
```

### 高级自定义Action

#### JSON解析Action

```python
class JsonAction(Action):
    """将输入的 JSON 字符串解析为 Python 对象"""
  
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            parsed_json = json.loads(values)
            setattr(namespace, self.dest, parsed_json)
        except json.JSONDecodeError as e:
            parser.error(f"无效的 JSON 格式: {e}")
```

#### 范围验证Action

```python
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
```

## 自定义类型处理函数

使用 `type` 参数指定自定义处理函数：

```python
def validate_and_process(value):
    """自定义处理函数"""
    try:
        num = int(value)
        if num < 0:
            raise ValueError("数字必须为正数")
        return num * 2  # 将输入值翻倍
    except ValueError as e:
        raise ValueError(f"无效输入: {e}")

parser.add_argument(
    "--number", 
    type=validate_and_process, 
    help="输入一个正整数，会自动翻倍"
)
```

## 实用技巧

### 1. 条件判断示例

```python
# store_true 示例
if args.verbose is True:
    print(f"{args.param} 的平方是: {args.param**2}")
else:
    print(args.param**2)

# count 示例 - 使用 match 语句
match args.verbose:
    case 1:
        print(f"平方结果是:{args.param**2}")
    case 2:
        print(f"{args.param} 的平方是: {args.param**2}")
    case _:
        print(args.param**2)
```

### 2. 列表参数处理

```python
# nargs=2 返回列表
print(args.param)        # [12, 21]
print(type(args.param))  # <class 'list'>

# 解构赋值
[a, b] = args.param
```

## 示例代码

项目中包含以下示例文件：

- `tutorial.py` - 基础教程和互斥参数组示例
- `custom_action_example.py` - 自定义Action类示例
- `advanced_action_example.py` - 高级自定义Action（JSON解析、范围验证）
- `function_action_example.py` - 自定义类型处理函数示例

### 运行示例

```bash
# 基础示例
python tutorial.py 2 3 -v

# 自定义Action示例  
python custom_action_example.py --custom hello --collect item1 --collect item2

# 高级Action示例
python advanced_action_example.py --json '{"name": "test"}' --score 85

# 函数处理示例
python function_action_example.py --number 5
```

## 总结

`argparse` 模块提供了强大而灵活的命令行参数解析功能：

1. **基础功能**：位置参数、可选参数、参数类型转换
2. **高级功能**：互斥参数组、参数个数控制、选择限制
3. **扩展性**：自定义Action类、自定义类型处理函数
4. **易用性**：自动生成帮助信息、友好的错误提示

通过学习这些功能，你可以创建功能丰富、用户友好的命令行工具。
