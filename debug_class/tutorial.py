"""
1. 断点表达式允许在参数满足一定条件的时候才触发这个断点
2. 断点命中次数允许设置当且仅当这个代码第 n 次执行的时候才触发这个断点
3. 日志消息允许在这个断点的时候输出消息到 “调试控制台”
4. 等待断点允许一个断点在另一个断点生效后才生效，否则一直沉寂

以上四种断点类型只能选择其中一种。
"""


class Language:
    def __init__(self, name: str) -> None:
        self.name = name

    def say_hi(self):
        print(f"Hello, I'm {self.name}")


languages: list[Language] = [Language("Python"), Language("Java"), Language("C++")]

for language in languages:
    language.say_hi()
